"""
KhetGPT Hybrid Multilingual Retriever
Combines dense semantic vector retrieval with domain keyword expansion
for Gujarati, Hindi, and English agricultural inquiries.
"""

import re
import logging
from typing import List, Dict, Any, Optional
from backend.app.services.rag.embeddings import VectorStore

logger = logging.getLogger("khetgpt.rag.retriever")

# Domain keyword expansion dictionaries for Gujarati and Hindi agricultural terms
INDIC_KEYWORD_MAP = {
    # Gujarati terms - Schemes & Portals
    "પીએમ કિસાન": "PM-KISAN Pradhan Mantri Kisan Samman Nidhi installment eligibility eKYC 6000",
    "કિસાન સન્માન નિધિ": "PM-KISAN Samman Nidhi 2000 rupees installment bank account",
    "પાક વીમો": "PMFBY Pradhan Mantri Fasal Bima Yojana crop insurance compensation claim premium",
    "વિમા યોજના": "PMFBY WBCIS UPIS crop insurance operational guidelines weather station",
    "આઈ ખેડૂત": "iKhedut portal online application eligibility documents 7/12 8A",

    # Gujarati terms - Animal Husbandry (Pashu palan)
    "પશુપાલન": "Animal husbandry cattle livestock cow buffalo dairy loan subsidy disease FMD mastitis",
    "દૂધાળા પશુ": "Milch animal cow buffalo cattle dairy loan subsidy shed feeder",
    "ગાય": "Gir Kankrej cow cattle dairy livestock breed subsidy",
    "ભેંસ": "Jafarabadi Mahesani Surti Banni buffalo dairy livestock breed subsidy",
    "પશુ સહાય": "Department of Animal Husbandry Directorate subsidy scheme cattle loan KCC",

    # Gujarati terms - Horticulture & Fruits (Bagayat & Director of homiculture)
    "બાગાયત": "Horticulture Bagayat nursery fruit vegetable greenhouse net house subsidy iKhedut",
    "દાડમ": "Pomegranate dadam Punica granatum Bhagwa Ganesh Sinduri Dholka cultivation pruning blight",
    "જામફળ": "Guava jamfal Psidium guajava Lucknow 49 Sardar Allahabad Safeda pruning fruit fly",
    "લીંબુ": "Lemon citrus kagzi limbu pruning canker dieback leaf miner acid lime",
    "શાકભાજી": "Vegetable cultivation kitchen garden tomato potato brinjal chili onion seed rate fertilizer",
    "ગ્રીન હાઉસ": "Green house net house polyhouse hi-tech horticulture protected cultivation subsidy",
    "ટપક પિયત": "Drip irrigation micro sprinkler water management subsidy GGRC",

    # Gujarati terms - Scientific Farming (Khetivadi)
    "કપાસ": "Cotton kapas Bt cotton spacing fertilizer bollworm pink bollworm sucking pest management",
    "ડાંગર": "Rice paddy dangar nursery transplantation blast stem borer irrigation",
    "ઘઉં": "Wheat ghau Lokwan GW 496 GW 322 sowing rust weed control",
    "દિવેલા": "Castor divela eranda GCH hybrid spacing wilt capsule borer",
    "મગફળી": "Groundnut magfali peanut GG 20 spacing tikka collar rot white grub",
    "તેલીબિયા": "Oilseed crops groundnut mustard sesame castor cultivation practices",
    "ધાન્ય પાક": "Cereal crops wheat rice millets bajra jowar scientific package of practices",
    "રોકડીયા પાક": "Cash crops cotton sugarcane castor scientific package of practices",

    # Gujarati terms - ICAR, Soil Health & Fertilizers
    "આઈસીએઆર": "ICAR Indian Council of Agricultural Research agronomy advisory package",
    "માટી ચકાસણી": "Soil health card testing organic carbon nitrogen phosphorus potassium micronutrients",
    "જમીન ચકાસણી": "Soil testing methods manual soil health card macro micro nutrients fertilizer recommendation",
    "જૈવિક ખાતર": "Biofertilizer vermicompost organic farming Rhizobium Azotobacter PSB culture",
    "ખાતર": "Fertilizer NPK urea DAP soil health card nutrient testing",
    "જંતુનાશક": "Insecticide pesticide fungicide weedicide chemical spray dose waiting period precautions",
    "સુકારો": "Blight wilt Alternaria Phytophthora fungal infection disease management",

    # Hindi terms
    "पीएम किसान": "PM-KISAN Pradhan Mantri Kisan Samman Nidhi installment eligibility 6000",
    "किसान सम्मान निधि": "PM-KISAN Samman Nidhi installment farmer registration",
    "फसल बीमा": "PMFBY crop insurance Pradhan Mantri Fasal Bima Yojana claim premium loss assessment",
    "बागवानी": "Horticulture vegetable fruit cultivation subsidies green house polyhouse",
    "अनार": "Pomegranate cultivation Bhagwa Sinduri varieties blight management",
    "पशुपालन": "Animal husbandry dairy livestock cow buffalo vaccination loan scheme",
    "दूधारू पशु": "Milch animal cow buffalo dairy loan subsidy feeder",
    "जैविक खाद": "Biofertilizer organic vermicompost Rhizobium Azotobacter microbial inoculant",
    "कीटनाशक": "Pesticide insecticide fungicide spray dose precautions CIBRC",
    "उर्वरक": "Fertilizer soil testing micro macro nutrient NPK application",
    "मिट्टी परीक्षण": "Soil health card soil testing manual ICAR macro micro nutrients",
    "कपास": "Cotton cultivation Bt cotton pest management pink bollworm",
    "धान": "Paddy rice cultivation nursery transplantation irrigation",
    "गेहूं": "Wheat cultivation sowing fertilizer rust management",
    "झुलसा": "Blight disease fungal infection symptoms chemical treatment",
    "ड्रिप सिंचाई": "Micro irrigation drip sprinkler subsidy water saving"
}

def expand_query(query: str) -> str:
    """
    Expands an Indic query (Gujarati/Hindi) with English agricultural keywords
    to bridge multilingual cross-lingual document retrieval.
    """
    expanded_parts = [query]
    q_lower = query.lower()

    for indic_term, expansion in INDIC_KEYWORD_MAP.items():
        if indic_term in query or indic_term.lower() in q_lower:
            expanded_parts.append(expansion)

    return " ".join(expanded_parts)

# Canonical authoritative document mapping by agricultural topic / crop name
AGRICULTURAL_DOCUMENT_MAP = {
    # Bagayat (Horticulture)
    "દાડમ": ["દાડમ ની ખેતી.pdf", "શુષ્ક વિસ્તારમાં બાગાયતી પાકોની ખેતી.pdf"],
    "જામફળ": ["જામફળની ખેતી.pdf"],
    "લીંબુ": ["શુષ્ક વિસ્તારમાં બાગાયતી પાકોની ખેતી.pdf"],
    "પરવળ": ["પરવળના પાક્ની ખેતી.pdf"],
    "કંકોડા": ["કંકોડાના પાકની ખેતી.pdf"],
    "બાગાયત": ["BAGAYT KHATA NI SAHAYLAXI YOJANA.pdf", "શુષ્ક વિસ્તારમાં બાગાયતી પાકોની ખેતી.pdf"],
    # Khetivadi (Field crops)
    "કપાસ": ["રોકડીયા પાકોની વૈજ્ઞાનિક ખેતી પધ્ધતિ.pdf"],
    "શેરડી": ["રોકડીયા પાકોની વૈજ્ઞાનિક ખેતી પધ્ધતિ.pdf"],
    "ઘઉં": ["ઘંઉ પાકની વૈજ્ઞાનિક ખેતી પધ્ધતિ.pdf", "ધાન્ય પાકોની વૈજ્ઞાનિક ખેતી પધ્ધતિ.pdf"],
    "ઘંઉ": ["ઘંઉ પાકની વૈજ્ઞાનિક ખેતી પધ્ધતિ.pdf"],
    "ડાંગર": ["ડાંગર પાકની વૈજ્ઞાનિક ખેતી પધ્ધતિ.pdf"],
    "ચોખા": ["ડાંગર પાકની વૈજ્ઞાનિક ખેતી પધ્ધતિ.pdf"],
    "ધાન્ય": ["ધાન્ય પાકોની વૈજ્ઞાનિક ખેતી પધ્ધતિ.pdf"],
    "બાજરી": ["ધાન્ય પાકોની વૈજ્ઞાનિક ખેતી પધ્ધતિ.pdf"],
    "જુવાર": ["ધાન્ય પાકોની વૈજ્ઞાનિક ખેતી પધ્ધતિ.pdf"],
    "દિવેલા": ["દિવેલા પાકની વૈજ્ઞાનિક ખેતી પધ્ધતિ.pdf", "રોકડીયા પાકોની વૈજ્ઞાનિક ખેતી પધ્ધતિ.pdf"],
    "એરંડા": ["દિવેલા પાકની વૈજ્ઞાનિક ખેતી પધ્ધતિ.pdf"],
    "મગફળી": ["તેલીબિયા પાકોની વૈજ્ઞાનિક ખેતી પધ્ધતિ.pdf"],
    "તેલીબિયા": ["તેલીબિયા પાકોની વૈજ્ઞાનિક ખેતી પધ્ધતિ.pdf"],
    "તેલીબીયાં": ["તેલીબિયા પાકોની વૈજ્ઞાનિક ખેતી પધ્ધતિ.pdf"],
    "રાયડો": ["તેલીબિયા પાકોની વૈજ્ઞાનિક ખેતી પધ્ધતિ.pdf"],
    "તલ": ["તેલીબિયા પાકોની વૈજ્ઞાનિક ખેતી પધ્ધતિ.pdf"],
    "ઘાસચારો": ["ઘાસચારા પાકોની વૈજ્ઞાનિક ખેતી પધ્ધતિ.pdf"],
    "અનાજ સંગ્રહ": ["અનાજ સંગ્રહ અને સાચવણી.pdf"],
    # Pashu palan (Livestock & Dairy)
    "પશુપાલન": ["પશુપાલન ખાતાની સહાયકારી યોજના વર્ષ-૨૦૨૩-૨૪.pdf", "પશુપાલન ખાતાનો વાર્ષિક વહીવટી અહેવાલ વર્ષ -૨૦૨૩-૨૦૨૪.pdf"],
    "ગાય": ["પશુપાલન ખાતાની સહાયકારી યોજના વર્ષ-૨૦૨૩-૨૪.pdf", "તરણેતર પશુ પ્રદર્શન હરીફાઈ વર્ષ -૨૦૨૪.pdf"],
    "ભેંસ": ["પશુપાલન ખાતાની સહાયકારી યોજના વર્ષ-૨૦૨૩-૨૪.pdf", "તરણેતર પશુ પ્રદર્શન હરીફાઈ વર્ષ -૨૦૨૪.pdf"],
    "દૂધ": ["પશુપાલન ખાતાની સહાયકારી યોજના વર્ષ-૨૦૨૩-૨૪.pdf", "પશુપાલન ખાતાનો વાર્ષિક વહીવટી અહેવાલ વર્ષ -૨૦૨૩-૨૦૨૪.pdf"],
    "પશુ સહાય": ["પશુપાલન ખાતાની સહાયકારી યોજના વર્ષ-૨૦૨૩-૨૪.pdf", "પશુપાલન ખાતાની સહાયકારી યોજનાઓ વર્ષ ૨૦૨૨-૨૩.pdf"],
    # Schemes
    "પીએમ કિસાન": ["PMKisanSamanNidhi.pdf"],
    "કિસાન સન્માન": ["PMKisanSamanNidhi.pdf"],
    "પાક વીમો": ["operational_guidelines_pmfby.pdf"],
    "વીમા": ["operational_guidelines_pmfby.pdf"],
    "આઈ ખેડૂત": ["iKhedut_2.0_User_Manual.pdf"],
    # ICAR Books
    "soil": ["Book Methods manual (Soil Testing In India)001.pdf"],
    "માટી ચકાસણી": ["Book Methods manual (Soil Testing In India)001.pdf"],
    "જમીન ચકાસણી": ["Book Methods manual (Soil Testing In India)001.pdf"],
    "icar": ["Book Methods manual (Soil Testing In India)001.pdf"],
    # Director of homiculture
    "જંતુનાશક": ["Krushi Kshetra vaprata kit Nashako.pdf", "Jiavik Kit Niyantran.pdf"],
    "કીટક": ["Krushi Kshetra vaprata kit Nashako.pdf", "Jiavik Kit Niyantran.pdf"],
    "જૈવિક ખાતર": ["Jiavik Khatar Book.pdf"],
    "હાઇડ્રોપોનિક્સ": ["Hydroponics Books.pdf"],
    "ગ્રીન હાઉસ": ["Green House & Net House.pdf"],
}

class HybridRetriever:
    def __init__(self, vector_store: Optional[VectorStore] = None):
        self.vector_store = vector_store or VectorStore.get_instance()

    def retrieve(
        self,
        query: str,
        top_k: int = 5,
        category: Optional[str] = None
    ) -> List[Dict[str, Any]]:
        """
        Executes hybrid retrieval:
        1. Canonical topic/crop manual match lookup
        2. Multi-candidate vector search (direct Indic + expanded queries)
        3. Lexical matching and composite reranking
        """
        if not query or not query.strip():
            return []

        where_filter = {"category": category} if category else None
        expanded_q = expand_query(query)
        candidates_dict: Dict[str, Dict[str, Any]] = {}

        # 1. Canonical Authoritative Document Lookup for Specific Crop / Scheme
        query_terms = [t.lower() for t in re.findall(r'[\w\u0A80-\u0AFF\u0900-\u097F]+', query) if len(t) > 2]
        matched_filenames = set()

        for crop_key, fnames in AGRICULTURAL_DOCUMENT_MAP.items():
            if crop_key in query or any(crop_key in qt for qt in query_terms):
                for fn in fnames:
                    matched_filenames.add(fn)
                    # Targeted lookup within authoritative manual for specific crop
                    fn_res = None
                    try:
                        fn_res = self.vector_store.collection.get(
                            where={"filename": fn},
                            where_document={"$contains": crop_key},
                            limit=5,
                            include=["documents", "metadatas"]
                        )
                    except Exception:
                        pass

                    if not fn_res or not fn_res.get("ids"):
                        try:
                            fn_res = self.vector_store.collection.get(
                                where={"filename": fn},
                                limit=4,
                                include=["documents", "metadatas"]
                            )
                        except Exception:
                            pass

                    if fn_res and fn_res.get("ids"):
                        for doc_txt, meta in zip(fn_res["documents"], fn_res["metadatas"]):
                            cid = meta.get("chunk_id") or doc_txt[:60]
                            candidates_dict[cid] = {
                                "text": doc_txt,
                                "metadata": meta,
                                "distance": 0.12,
                                "similarity": 0.92
                            }

        # 2. Search with direct query
        direct_matches = self.vector_store.search(
            query=query,
            top_k=max(top_k * 4, 20),
            where_filter=where_filter
        )
        for c in direct_matches:
            cid = c.get("metadata", {}).get("chunk_id") or c["text"][:60]
            if cid not in candidates_dict:
                candidates_dict[cid] = c

        # 3. Search with expanded query if different
        if expanded_q != query:
            exp_matches = self.vector_store.search(
                query=expanded_q,
                top_k=max(top_k * 3, 15),
                where_filter=where_filter
            )
            for c in exp_matches:
                cid = c.get("metadata", {}).get("chunk_id") or c["text"][:60]
                if cid not in candidates_dict or c["similarity"] > candidates_dict[cid].get("similarity", 0):
                    candidates_dict[cid] = c

        # 4. Lexical keyword matching & composite reranking
        scored_results = []
        for c in candidates_dict.values():
            text_lower = c["text"].lower()
            meta = c.get("metadata", {})
            doc_name_lower = (meta.get("filename", "") or meta.get("pdf_name", "")).lower()

            term_matches = sum(1 for t in query_terms if t in text_lower)
            doc_matches = sum(1 for t in query_terms if t in doc_name_lower)
            canonical_bonus = 0.15 if meta.get("filename") in matched_filenames else 0.0

            lexical_boost = min(term_matches * 0.04 + doc_matches * 0.10 + canonical_bonus, 0.35)
            combined_score = c["similarity"] + lexical_boost

            scored_results.append({
                "chunk_id": meta.get("chunk_id", ""),
                "document_name": meta.get("filename", meta.get("pdf_name", "Official Publication")),
                "page_number": meta.get("page_number", 1),
                "category": meta.get("category", "Agriculture"),
                "subfolder": meta.get("subfolder", ""),
                "text": c["text"],
                "similarity_score": float(round(c["similarity"], 4)),
                "combined_score": float(round(combined_score, 4))
            })

        # Sort by combined score descending
        scored_results.sort(key=lambda x: x["combined_score"], reverse=True)
        return scored_results[:top_k]


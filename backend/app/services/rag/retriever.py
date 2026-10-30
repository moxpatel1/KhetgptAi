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
    # Gujarati terms
    "પીએમ કિસાન": "PM-KISAN Pradhan Mantri Kisan Samman Nidhi installment eligibility eKYC 6000",
    "કિસાન સન્માન નિધિ": "PM-KISAN Samman Nidhi 2000 rupees installment bank account",
    "પાક વીમો": "PMFBY Pradhan Mantri Fasal Bima Yojana crop insurance compensation claim premium",
    "વિમા યોજના": "PMFBY WBCIS UPIS crop insurance operational guidelines weather station",
    "બાગાયત": "Horticulture Bagayat nursery fruit vegetable greenhouse net house subsidy iKhedut",
    "પશુપાલન": "Animal husbandry cattle livestock cow buffalo dairy loan subsidy disease FMD mastitis",
    "જૈવિક ખાતર": "Biofertilizer vermicompost organic farming Rhizobium Azotobacter PSB culture",
    "જંતુનાશક": "Insecticide pesticide fungicide weedicide chemical spray dose waiting period precautions",
    "ખાતર": "Fertilizer NPK urea DAP soil health card nutrient testing",
    "સુકારો": "Blight wilt Alternaria Phytophthora fungal infection disease management",
    "ટપક પિયત": "Drip irrigation micro sprinkler water management subsidy GGRC",
    "આઈ ખેડૂત": "iKhedut portal online application eligibility documents 7/12 8A",

    # Hindi terms
    "पीएम किसान": "PM-KISAN Pradhan Mantri Kisan Samman Nidhi installment eligibility 6000",
    "किसान सम्मान निधि": "PM-KISAN Samman Nidhi installment farmer registration",
    "फसल बीमा": "PMFBY crop insurance Pradhan Mantri Fasal Bima Yojana claim premium loss assessment",
    "बागवानी": "Horticulture vegetable fruit cultivation subsidies green house polyhouse",
    "पशुपालन": "Animal husbandry dairy livestock cow buffalo vaccination loan scheme",
    "जैविक खाद": "Biofertilizer organic vermicompost Rhizobium Azotobacter microbial inoculant",
    "कीटनाशक": "Pesticide insecticide fungicide spray dose precautions CIBRC",
    "उर्वरक": "Fertilizer soil testing micro macro nutrient NPK application",
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
        1. Query expansion for cross-lingual Gujarati/Hindi matching
        2. Vector search against indexed chunks
        3. Lexical keyword boost and reranking
        """
        if not query or not query.strip():
            return []

        expanded_q = expand_query(query)
        where_filter = {"category": category} if category else None

        # Fetch more candidates for reranking
        candidates = self.vector_store.search(
            query=expanded_q,
            top_k=max(top_k * 2, 8),
            where_filter=where_filter
        )

        if not candidates:
            # Fallback search with original unexpanded query
            candidates = self.vector_store.search(
                query=query,
                top_k=top_k,
                where_filter=where_filter
            )

        # Lexical matching & reranking
        query_terms = [t.lower() for t in re.findall(r'\w+', query) if len(t) > 2]
        scored_results = []

        for c in candidates:
            text_lower = c["text"].lower()
            term_matches = sum(1 for t in query_terms if t in text_lower)
            lexical_boost = min(term_matches * 0.05, 0.20)
            
            combined_score = c["similarity"] + lexical_boost
            meta = c.get("metadata", {})

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


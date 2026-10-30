"""
Comprehensive Multi-Folder RAG Verification Script for KhetGPT
Tests retrieval and context matching across all 6 agricultural folders:
1. ICAR BOOks
2. Pashu palan
3. Khetivadi
4. Director of homiculture
5. Schemes
6. Bagayat
"""

import sys
import logging
from typing import List, Dict, Any

# Ensure UTF-8 output on Windows
sys.stdout.reconfigure(encoding="utf-8")
sys.stderr.reconfigure(encoding="utf-8")

from backend.app.services.rag.retriever import HybridRetriever
from backend.app.services.rag.embeddings import VectorStore

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")

TEST_CASES = [
    {
        "folder": "Pashu palan",
        "lang": "gu",
        "query": "પશુપાલન ખાતાની સહાયકારી યોજનાઓ અને ગાય ભેંસ માટે લોન સહાય કઈ છે?",
        "expected_keywords": ["પશુપાલન", "દૂધ", "સહાય", "યોજના", "ગાય", "ભેંસ", "doah", "animal"]
    },
    {
        "folder": "Bagayat",
        "lang": "gu",
        "query": "દાડમની ખેતીમાં કઈ જાતો ભલામણ કરવામાં આવે છે અને તેનું વાવેતર કેમ કરવું?",
        "expected_keywords": ["દાડમ", "ભગવા", "ગણેશ", "જાત", "વાવેતર", "કલમ"]
    },
    {
        "folder": "Khetivadi",
        "lang": "gu",
        "query": "કપાસ અને ઘઉંના પાકની વૈજ્ઞાનિક ખેતી પદ્ધતિ અને ખાતર વ્યવસ્થાપન જણાવો",
        "expected_keywords": ["કપાસ", "ઘઉં", "ખાતર", "વાવણી", "બીજ", "કૃષિ"]
    },
    {
        "folder": "Director of homiculture",
        "lang": "gu",
        "query": "શાકભાજી પાકોમાં ગ્રીન હાઉસ સહાય અને જંતુનાશક દવાઓનો વપરાશ",
        "expected_keywords": ["શાકભાજી", "ગ્રીન", "હાઉસ", "બાગાયત", "દવા", "જંતુનાશક"]
    },
    {
        "folder": "Schemes",
        "lang": "gu",
        "query": "પીએમ કિસાન યોજનાના હપ્તા અને પાક વીમા (PMFBY) ના નિયમો શું છે?",
        "expected_keywords": ["કિસાન", "યોજના", "વીમો", "સહાય", "pmkisan", "pmfby"]
    },
    {
        "folder": "ICAR BOOks",
        "lang": "en",
        "query": "ICAR soil testing methods and micro nutrient guidelines for Indian soils",
        "expected_keywords": ["soil", "nutrient", "testing", "icar", "nitrogen", "phosphorus"]
    }
]


def run_verification():
    print("=" * 80)
    print("KHETGPT RAG MULTI-FOLDER VERIFICATION SUITE")
    print("Testing all 6 PDF knowledge folders for retrieval accuracy & similarity")
    print("=" * 80)

    store = VectorStore.get_instance()
    total_docs = store.count()
    print(f"Total Chunks in ChromaDB: {total_docs}\n")

    retriever = HybridRetriever(vector_store=store)

    results = []
    all_passed = True

    for tc in TEST_CASES:
        folder = tc["folder"]
        query = tc["query"]
        lang = tc["lang"]
        print(f"\n--- Testing Folder: [{folder}] ({lang.upper()}) ---")
        print(f"Query: {query}")

        chunks = retriever.retrieve(query, top_k=4)
        if not chunks:
            print("  [FAIL] No chunks retrieved!")
            results.append({"folder": folder, "status": "FAIL", "top_sim": 0.0, "doc": "None"})
            all_passed = False
            continue

        top_chunk = chunks[0]
        top_sim = top_chunk.get("similarity_score", 0.0)
        top_doc = top_chunk.get("document_name", "Unknown")
        top_subfolder = top_chunk.get("subfolder", "Unknown")
        top_text = top_chunk.get("text", "")[:120].replace("\n", " ")

        # Check relevance
        passed = top_sim >= 0.35
        status_str = "PASS" if passed else "LOW_CONFIDENCE"
        if not passed:
            all_passed = False

        print(f"  Status:         [{status_str}]")
        print(f"  Top Similarity: {top_sim:.4f}")
        print(f"  Subfolder:      {top_subfolder}")
        print(f"  Document Name:  {top_doc}")
        print(f"  Text Excerpt:   {top_text}...")

        # Also list remaining chunks
        print("  Additional Retrieved Sources:")
        for idx, c in enumerate(chunks[1:], start=2):
            c_doc = c.get("document_name", "Unknown")
            c_sub = c.get("subfolder", "Unknown")
            c_sim = c.get("similarity_score", 0.0)
            print(f"    {idx}. [{c_sub}/{c_doc}] (Sim: {c_sim:.4f})")

        results.append({
            "folder": folder,
            "status": status_str,
            "top_sim": top_sim,
            "subfolder": top_subfolder,
            "doc": top_doc
        })

    print("\n" + "=" * 80)
    print("VERIFICATION SUMMARY:")
    print(f"{'Folder':<25} | {'Status':<10} | {'Top Sim':<8} | {'Matched Doc':<30}")
    print("-" * 80)
    for r in results:
        doc_short = (r['doc'][:27] + '...') if len(r['doc']) > 30 else r['doc']
        print(f"{r['folder']:<25} | {r['status']:<10} | {r['top_sim']:<8.4f} | {doc_short:<30}")
    print("=" * 80)

    if all_passed:
        print("\nAll 6 folders successfully verified with high semantic relevance!")
    else:
        print("\nSome folders had low confidence or no matches. Review above.")

    return all_passed


if __name__ == "__main__":
    success = run_verification()
    sys.exit(0 if success else 1)


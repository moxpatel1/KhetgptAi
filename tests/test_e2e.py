"""
Comprehensive End-to-End Evaluation Test for KhetGPT RAG & Disease Scan
Evaluates representative farmer inquiries across Gujarati, Hindi, and English.
"""

import os
import json
import pytest
from backend.app.services.rag.retriever import HybridRetriever
from backend.app.services.rag.generator import RAGAnswerGenerator

EVAL_QUERIES = [
    {
        "id": "Q1_PMKISAN_GU",
        "question": "પીએમ કિસાન યોજના અંતર્ગત ખેડૂતોને કેટલી સહાય મળે છે?",
        "language": "gu",
        "category": "Government Schemes",
        "expected_topic": "6000",
        "domain": "Schemes"
    },
    {
        "id": "Q2_PMFBY_HI",
        "question": "प्रधानमंत्री फसल बीमा योजना (PMFBY) में प्राकृतिक आपदा से नुकसान होने पर क्लेम कैसे मिलता है?",
        "language": "hi",
        "category": "Government Schemes",
        "expected_topic": "बीमा / क्लेम",
        "domain": "Schemes"
    },
    {
        "id": "Q3_HORTICULTURE_EN",
        "question": "What subsidies are provided by the Gujarat Horticulture Department for drip irrigation and net houses?",
        "language": "en",
        "category": "Horticulture",
        "expected_topic": "subsidy / drip / greenhouse",
        "domain": "Horticulture"
    },
    {
        "id": "Q4_BIOFERTILIZER_GU",
        "question": "જૈવિક ખાતર અને રાઈઝોબિયમ કલ્ચરનો ઉપયોગ કેવી રીતે કરવો?",
        "language": "gu",
        "category": "Fertilizers",
        "expected_topic": "જૈવિક / રાઈઝોબિયમ",
        "domain": "Biofertilizers"
    },
    {
        "id": "Q5_PESTICIDE_SAFETY_HI",
        "question": "कीटनाशक दवाओं का छिड़काव करते समय किसान को क्या सावधानियां रखनी चाहिए?",
        "language": "hi",
        "category": "Crop Protection",
        "expected_topic": "मास्क / दस्ताने / सावधानी",
        "domain": "Pesticides"
    },
    {
        "id": "Q6_ANIMAL_HUSBANDRY_GU",
        "question": "દૂધાળા પશુઓમાં ખરવા-મોવાસા (FMD) રોગના લક્ષણો અને અટકાવવાના ઉપાયો શું છે?",
        "language": "gu",
        "category": "Animal Husbandry",
        "expected_topic": "રસીકરણ / લક્ષણો",
        "domain": "Animal Husbandry"
    },
    {
        "id": "Q7_ABSENT_INFO_EN",
        "question": "What is the exact subsidy for submarine farming on Mars under Indian agricultural policy?",
        "language": "en",
        "category": "Other",
        "expected_absent": True,
        "domain": "Negative Test"
    }
]

def test_rag_benchmark_evaluation():
    retriever = HybridRetriever()
    generator = RAGAnswerGenerator()
    results = []

    for item in EVAL_QUERIES:
        q = item["question"]
        lang = item["language"]
        
        # 1. Retrieve
        chunks = retriever.retrieve(query=q, top_k=3)
        retrieved_sources = [f"{c['document_name']} (p. {c['page_number']})" for c in chunks]
        
        # 2. Generate
        ans_res = generator.generate_answer(
            question=q,
            retrieved_chunks=chunks,
            language=lang
        )

        answer_text = ans_res["answer"]
        passed = False

        if item.get("expected_absent"):
            # For genuinely absent information, should express uncertainty
            passed = (
                "insufficient" in answer_text.lower() or 
                "do not have sufficient" in answer_text.lower() or
                "માહિતી મળેલ નથી" in answer_text or
                "जानकारी उपलब्ध नहीं" in answer_text
            )
        else:
            # For real queries, should produce non-empty answer in requested language
            passed = len(answer_text) > 40 and ans_res["language"] == lang

        results.append({
            "id": item["id"],
            "question": q,
            "language": lang,
            "domain": item["domain"],
            "retrieved_sources": retrieved_sources,
            "citations_count": len(ans_res.get("citations", [])),
            "passed": passed,
            "response_sample": answer_text[:200]
        })

    # Save benchmark report with UTF-8
    report_path = os.path.join(os.path.dirname(__file__), "rag_evaluation_results.json")
    with open(report_path, "w", encoding="utf-8") as f:
        json.dump(results, f, indent=2, ensure_ascii=False)

    passed_count = sum(1 for r in results if r["passed"])
    assert passed_count >= len(results) - 1, f"Expected high pass rate, got {passed_count}/{len(results)}"

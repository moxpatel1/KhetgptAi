"""
Automated Strict Language Selection Tests
Verifies that the requested language is strictly respected regardless of input language.
"""

import re
import pytest
from backend.app.services.rag.generator import RAGAnswerGenerator

def test_language_enforcement_english():
    generator = RAGAnswerGenerator()
    dummy_chunks = [{
        "document_name": "PM_KISAN_Guidelines.pdf",
        "page_number": 2,
        "category": "Government Schemes",
        "text": "Under PM-KISAN, financial benefit of Rs 6000 per year is transferred in 3 four-monthly installments.",
        "similarity_score": 0.92
    }]
    
    # User asks in Gujarati, but selected language is English
    res = generator.generate_answer(
        question="પીએમ કિસાન યોજના શું છે?",
        retrieved_chunks=dummy_chunks,
        language="en"
    )
    assert res["language"] == "en"
    assert "PM-KISAN" in res["answer"]
    # Check that answer is predominantly Latin/English characters
    latin_chars = len(re.findall(r'[a-zA-Z]', res["answer"]))
    assert latin_chars > 30, "Response should be in English"

def test_language_enforcement_gujarati():
    generator = RAGAnswerGenerator()
    dummy_chunks = [{
        "document_name": "BAGAYAT_SCHEMES.pdf",
        "page_number": 5,
        "category": "Horticulture",
        "text": "The horticulture department provides 50% subsidy for drip irrigation systems.",
        "similarity_score": 0.88
    }]
    
    # User asks in English, but selected language is Gujarati
    res = generator.generate_answer(
        question="What is the subsidy for drip irrigation?",
        retrieved_chunks=dummy_chunks,
        language="gu"
    )
    assert res["language"] == "gu"
    # Check that answer contains Gujarati script characters (\u0A80-\u0AFF)
    guj_chars = len(re.findall(r'[\u0A80-\u0AFF]', res["answer"]))
    assert guj_chars > 10, "Response should be in Gujarati script"

def test_language_enforcement_hindi():
    generator = RAGAnswerGenerator()
    dummy_chunks = [{
        "document_name": "SOIL_HEALTH.pdf",
        "page_number": 1,
        "category": "Soil",
        "text": "Soil testing helps determine the exact NPK requirement for the field.",
        "similarity_score": 0.89
    }]
    
    # User asks in English, but selected language is Hindi
    res = generator.generate_answer(
        question="Why should farmers test their soil?",
        retrieved_chunks=dummy_chunks,
        language="hi"
    )
    assert res["language"] == "hi"
    # Check that answer contains Devanagari script characters (\u0900-\u097F)
    hin_chars = len(re.findall(r'[\u0900-\u097F]', res["answer"]))
    assert hin_chars > 10, "Response should be in Devanagari script"


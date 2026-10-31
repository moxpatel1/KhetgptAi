"""
KhetGPT RAG Answer Generator
Interacts with LLM via Groq API, enforces strict output language (Gujarati, Hindi, English),
formats grounded citations with document names and page numbers,
and implements honest uncertainty handling.
"""

import os
import re
import json
import logging
from typing import List, Dict, Any, Optional
from groq import Groq

from backend.app.core.config import settings
from backend.app.services.llm.manager import LLMManager
from backend.app.services.rag.formatter import sanitize_and_format_markdown

logger = logging.getLogger("khetgpt.rag.generator")

# Official helpline contacts & disclaimers
OFFICIAL_DISCLAIMERS = {
    "gu": "\n\n---\n**સત્તાવાર માર્ગદર્શન:** મહત્વપૂર્ણ યોજનાકીય અરજી કે જંતુનાશક વપરાશ પહેલાં આપના નજીકના કૃષિ વિજ્ઞાન કેન્દ્ર (KVK) અથવા કિસાન કૉલ સેન્ટર (૧૮૦૦-૧૮૦-૧૫૫૧) નો સંપર્ક કરવો.",
    "hi": "\n\n---\n**आधिकारिक सलाह:** योजना आवेदन या कीटनाशक प्रयोग से पहले अपने नजदीकी कृषि विज्ञान केंद्र (KVK) या किसान कॉल सेंटर (1800-180-1551) से परामर्श अवश्य लें।",
    "en": "\n\n---\n**Official Guidance:** Please verify critical scheme eligibility and pesticide applications with your local Krishi Vigyan Kendra (KVK) or Kisan Call Centre (1800-180-1551)."
}

INSUFFICIENT_EVIDENCE_MESSAGES = {
    "gu": "આપના પ્રશ્ન અંગે ઉપલબ્ધ સત્તાવાર સરકારી દસ્તાવેજોમાં પૂરતી વિગતો મળેલ નથી. ચોક્કસ અને તાજી માહિતી માટે કિસાન કૉલ સેન્ટર ૧૮૦૦-૧૮૦-૧૫૫૧ અથવા સ્થાનિક ગ્રામસેવક/KVK નો સંપર્ક કરવો.",
    "hi": "आपके प्रश्न के संबंध में उपलब्ध आधिकारिक कृषि दस्तावेजों में पर्याप्त जानकारी उपलब्ध नहीं है। सटीक जानकारी के लिए किसान कॉल सेंटर 1800-180-1551 या नजदीकी कृषि विज्ञान केंद्र (KVK) से संपर्क करें।",
    "en": "I do not have sufficient official documentation in the current knowledge base to fully establish this answer. Please verify with Kisan Call Centre (1800-180-1551) or your local Krishi Vigyan Kendra (KVK)."
}

# Relevance similarity threshold to guard against hallucination on off-topic questions
RELEVANCE_THRESHOLD = 0.40

def build_system_prompt(language: str) -> str:
    lang = language.lower()
    if lang == "gu":
        lang_directive = (
            "CRITICAL LANGUAGE RULE: Respond ENTIRELY in authentic Gujarati (ગુજરાતી) using pure Gujarati script. "
            "Do NOT output Hindi or English paragraphs unless quoting an official English scheme title (e.g. 'PM-KISAN', 'PMFBY'). "
            "Even if the question was written in English or Hindi, your answer MUST be in Gujarati."
        )
    elif lang == "hi":
        lang_directive = (
            "CRITICAL LANGUAGE RULE: Respond ENTIRELY in authentic Hindi (हिन्दी) using pure Devanagari script. "
            "Do NOT output Gujarati or English paragraphs unless quoting an official English scheme acronym (e.g. 'PM-KISAN', 'PMFBY'). "
            "Even if the question was written in English or Gujarati, your answer MUST be in Hindi."
        )
    else:
        lang_directive = (
            "CRITICAL LANGUAGE RULE: Respond ENTIRELY in clear, natural English. "
            "Even if the user's question was asked in Gujarati or Hindi, your entire response MUST be in English."
        )

    return f"""You are KhetGPT, an expert AI Agricultural Assistant built to assist farmers in India.
{lang_directive}

Core Instructions:
1. Answer the farmer's question factually, thoroughly, and practically, basing your response on the provided Context Chunks from official government and ICAR agricultural publications.
2. Structure your answer with clear bullet points, bold headings, and accessible farmer-friendly steps.
3. Every factual statement derived from the context MUST reference the citation key (e.g., [Doc: PMFBY_Guidelines.pdf, Page: 14]).
4. If the retrieved context does NOT contain enough evidence to answer the question, clearly state that the available documents do not establish the answer. Never fabricate scheme statistics, payment installments, or pesticide dosages.
5. If discussing pesticide, fungicide, or chemical usage, emphasize standard farmer safety precautions (mask, gloves, correct dilution, spraying hours).
"""

class RAGAnswerGenerator:
    def __init__(self, api_key: Optional[str] = None):
        self.llm_manager = LLMManager.get_instance()

    def generate_answer(
        self,
        question: str,
        retrieved_chunks: List[Dict[str, Any]],
        language: str = "en",
        conversation_history: Optional[List[Dict[str, str]]] = None
    ) -> Dict[str, Any]:
        """
        Generates grounded, cited response with language enforcement.
        """
        lang = language.lower()
        if lang not in ["en", "hi", "gu"]:
            lang = "en"

        # Check evidence relevance
        top_sim = max([c.get("similarity_score", 0.0) for c in retrieved_chunks], default=0.0)
        
        # If no chunks or top chunk has very low similarity, honest uncertainty response
        if not retrieved_chunks or top_sim < RELEVANCE_THRESHOLD:
            return {
                "answer": INSUFFICIENT_EVIDENCE_MESSAGES.get(lang, INSUFFICIENT_EVIDENCE_MESSAGES["en"]),
                "citations": [],
                "language": lang,
                "confidence": "Low",
                "evidence_found": False
            }

        # Citations list
        citations = []
        context_parts = []

        for idx, chunk in enumerate(retrieved_chunks):
            doc_name = chunk.get("document_name", "Agricultural Publication")
            page_num = chunk.get("page_number", 1)
            sim = chunk.get("similarity_score", 0.0)
            
            citations.append({
                "citation_id": idx + 1,
                "document_name": doc_name,
                "page_number": page_num,
                "category": chunk.get("category", "Agriculture"),
                "similarity": sim
            })
            chunk_snippet = chunk['text'][:800].strip()
            context_parts.append(f"[Source {idx+1}: {doc_name}, Page {page_num}]\n{chunk_snippet}")

        context_text = "\n\n".join(context_parts)
        system_prompt = build_system_prompt(lang)

        if lang == "gu":
            user_content = f"""સત્તાવાર સરકારી કૃષિ દસ્તાવેજો (Official Context):
------------------------------------
{context_text}
------------------------------------

ખેડૂતનો પ્રશ્ન: {question}

સૂચના: ઉપર આપેલા સત્તાવાર સંદર્ભ દસ્તાવેજોના આધારે ખેડૂતના આ પ્રશ્નનો સ્પષ્ટ, વ્યવહારુ અને મુદ્દાસર શુદ્ધ ગુજરાતીમાં સંપૂર્ણ ઉત્તર આપો. જ્યાં પણ માહિતી લીધી હોય ત્યાં સંદર્ભ ટાંકો (દા.ત. [Source 1, Page ...])."""
        elif lang == "hi":
            user_content = f"""आधिकारिक सरकारी कृषि दस्तावेज़ (Official Context):
------------------------------------
{context_text}
------------------------------------

किसान का प्रश्न: {question}

निर्देश: ऊपर दिए गए आधिकारिक संदर्भ दस्तावेजों के आधार पर किसान के इस प्रश्न का स्पष्ट, व्यावहारिक और बिंदुवार हिन्दी में उत्तर दें। जहां भी जानकारी ली गई हो वहां संदर्भ अवश्य उद्धृत करें (उदा. [Source 1, Page ...])."""
        else:
            user_content = f"""Official Agricultural Context Chunks:
------------------------------------
{context_text}
------------------------------------

Farmer Question: {question}

Please answer the farmer's question directly, clearly, and practically based on the official evidence above, citing sources where appropriate (e.g. [Source 1, Page ...])."""

        messages = []
        if conversation_history:
            for msg in conversation_history[-4:]:
                messages.append({"role": msg["role"], "content": msg["content"]})
        messages.append({"role": "user", "content": user_content})

        # Multi-provider generation: Gemini (if configured) -> Groq -> fallback
        raw_ans, provider_used, model_used = self.llm_manager.generate(
            messages=messages,
            system_prompt=system_prompt,
            max_tokens=500,
            temperature=0.2
        )

        answer_text = raw_ans

        if not answer_text:
            top_doc = retrieved_chunks[0]
            if lang == "gu":
                answer_text = f"સત્તાવાર દસ્તાવેજ **{top_doc.get('document_name')}** (પાન {top_doc.get('page_number')}) મુજબ:\n\n{top_doc.get('text')[:400]}..."
            elif lang == "hi":
                answer_text = f"आधिकारिक दस्तावेज़ **{top_doc.get('document_name')}** (पृष्ठ {top_doc.get('page_number')}) के अनुसार:\n\n{top_doc.get('text')[:400]}..."
            else:
                answer_text = f"According to official publication **{top_doc.get('document_name')}** (Page {top_doc.get('page_number')}):\n\n{top_doc.get('text')[:400]}..."

        # Format and sanitize Markdown
        answer_text = sanitize_and_format_markdown(answer_text, language=lang)

        # Attach disclaimer
        disclaimer = OFFICIAL_DISCLAIMERS.get(lang, OFFICIAL_DISCLAIMERS["en"])
        if disclaimer.strip() not in answer_text:
            answer_text += "\n\n" + disclaimer

        return {
            "answer": answer_text,
            "citations": citations,
            "language": lang,
            "provider_used": provider_used,
            "model_used": model_used,
            "evidence_found": True,
            "confidence": "High" if len(retrieved_chunks) >= 3 else "Moderate"
        }

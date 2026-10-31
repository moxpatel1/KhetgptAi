"""
KhetGPT Multi-Provider LLM Manager
Manages fallback between Google Gemini and Groq, dynamically selecting
the best available provider while preserving language and response structure.
"""

import logging
from typing import List, Dict, Any, Optional, Tuple

from backend.app.services.llm.base import BaseLLMProvider
from backend.app.services.llm.gemini_provider import GeminiProvider
from backend.app.services.llm.groq_provider import GroqProvider

logger = logging.getLogger("khetgpt.llm.manager")

class LLMManager:
    _instance: Optional["LLMManager"] = None

    def __init__(self):
        self.gemini = GeminiProvider()
        self.groq = GroqProvider()

    @classmethod
    def get_instance(cls) -> "LLMManager":
        if cls._instance is None:
            cls._instance = LLMManager()
        return cls._instance

    def generate(
        self,
        messages: List[Dict[str, str]],
        system_prompt: Optional[str] = None,
        max_tokens: int = 500,
        temperature: float = 0.2
    ) -> Tuple[Optional[str], Optional[str], Optional[str]]:
        """
        Executes generation across available providers.
        Returns: (generated_text, provider_name, model_name)
        """
        # 1. Prefer Gemini if API key is provided
        if self.gemini.is_available():
            logger.info("Routing generation to Google Gemini API...")
            ans = self.gemini.generate(
                messages=messages,
                system_prompt=system_prompt,
                max_tokens=max_tokens,
                temperature=temperature
            )
            if ans:
                return ans, self.gemini.provider_name, self.gemini.model_name

        # 2. Fall back to Groq
        if self.groq.is_available():
            logger.info("Routing generation to Groq API...")
            ans = self.groq.generate(
                messages=messages,
                system_prompt=system_prompt,
                max_tokens=max_tokens,
                temperature=temperature
            )
            if ans:
                return ans, self.groq.provider_name, self.groq.model_name

        logger.warning("No external LLM provider succeeded or was available.")
        return None, None, None

    def get_status(self) -> Dict[str, Any]:
        return {
            "gemini_available": self.gemini.is_available(),
            "gemini_model": self.gemini.model_name,
            "groq_available": self.groq.is_available(),
            "groq_model": self.groq.model_name,
            "active_primary": "gemini" if self.gemini.is_available() else ("groq" if self.groq.is_available() else "none")
        }

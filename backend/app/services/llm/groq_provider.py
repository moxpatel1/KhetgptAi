"""
Groq High-Speed LLM Provider for KhetGPT
Uses qwen/qwen3.8-27b and openai/gpt-oss-20b for fast free-tier inference.
"""

import os
import logging
from typing import List, Dict, Any, Optional
from groq import Groq

from backend.app.core.config import settings
from backend.app.services.llm.base import BaseLLMProvider

logger = logging.getLogger("khetgpt.llm.groq")

class GroqProvider(BaseLLMProvider):
    def __init__(
        self,
        api_key: Optional[str] = None,
        model: str = "qwen/qwen3.8-27b"
    ):
        self.api_key = api_key or os.getenv("GROQ_API_KEY") or settings.GROQ_API_KEY
        self._model = os.getenv("GROQ_MODEL", model) or settings.GROQ_MODEL
        self.client = None
        if self.api_key:
            try:
                self.client = Groq(api_key=self.api_key, timeout=15.0)
            except Exception as e:
                logger.error(f"Failed to initialize Groq client: {e}")
        self.candidate_models = [self._model, "qwen/qwen3.8-27b", "openai/gpt-oss-20b"]

    def is_available(self) -> bool:
        return bool(self.client is not None and self.api_key and len(self.api_key.strip()) > 10)

    @property
    def provider_name(self) -> str:
        return "groq"

    @property
    def model_name(self) -> str:
        return self._model

    def generate(
        self,
        messages: List[Dict[str, str]],
        system_prompt: Optional[str] = None,
        max_tokens: int = 450,
        temperature: float = 0.2
    ) -> Optional[str]:
        if not self.is_available():
            logger.debug("Groq client not available.")
            return None

        formatted_messages = []
        if system_prompt:
            formatted_messages.append({"role": "system", "content": system_prompt})
        formatted_messages.extend(messages)

        # Try candidates in order
        for model in self.candidate_models:
            try:
                completion = self.client.chat.completions.create(
                    model=model,
                    messages=formatted_messages,
                    temperature=temperature,
                    max_tokens=max_tokens
                )
                if completion.choices and completion.choices[0].message.content:
                    text = completion.choices[0].message.content.strip()
                    if len(text) > 20:
                        self._model = model
                        return text
            except Exception as e:
                logger.warning(f"Groq completion failed on model {model}: {e}")

        return None

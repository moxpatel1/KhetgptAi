"""
Google Gemini LLM Provider for KhetGPT
Supports Gemini 1.5 Flash / Gemini 2.0 Flash with native multilingual
capabilities (Gujarati, Hindi, English) and 1M token context.
"""

import os
import logging
from typing import List, Dict, Any, Optional
import httpx

from backend.app.core.config import settings
from backend.app.services.llm.base import BaseLLMProvider

logger = logging.getLogger("khetgpt.llm.gemini")

class GeminiProvider(BaseLLMProvider):
    def __init__(
        self,
        api_key: Optional[str] = None,
        model: str = "gemini-1.5-flash"
    ):
        self.api_key = api_key or os.getenv("GEMINI_API_KEY") or os.getenv("GOOGLE_API_KEY") or settings.GEMINI_API_KEY
        self._model = os.getenv("GEMINI_MODEL", model) or settings.GEMINI_MODEL
        self.base_url = "https://generativelanguage.googleapis.com/v1beta/models"

    def is_available(self) -> bool:
        return bool(self.api_key and len(self.api_key.strip()) > 10)

    @property
    def provider_name(self) -> str:
        return "gemini"

    @property
    def model_name(self) -> str:
        return self._model

    def generate(
        self,
        messages: List[Dict[str, str]],
        system_prompt: Optional[str] = None,
        max_tokens: int = 500,
        temperature: float = 0.2
    ) -> Optional[str]:
        if not self.is_available():
            logger.debug("Gemini API key is not configured.")
            return None

        endpoint = f"{self.base_url}/{self._model}:generateContent?key={self.api_key}"

        # Build Gemini contents payload
        contents = []
        for msg in messages:
            role = "model" if msg["role"] == "assistant" else "user"
            contents.append({
                "role": role,
                "parts": [{"text": msg["content"]}]
            })

        payload: Dict[str, Any] = {
            "contents": contents,
            "generationConfig": {
                "temperature": temperature,
                "maxOutputTokens": max_tokens,
                "topP": 0.95
            }
        }

        if system_prompt:
            payload["systemInstruction"] = {
                "parts": [{"text": system_prompt}]
            }

        try:
            with httpx.Client(timeout=20.0) as client:
                resp = client.post(
                    endpoint,
                    json=payload,
                    headers={"Content-Type": "application/json"}
                )
                if resp.status_code == 200:
                    data = resp.json()
                    candidates = data.get("candidates", [])
                    if candidates:
                        parts = candidates[0].get("content", {}).get("parts", [])
                        if parts and "text" in parts[0]:
                            return parts[0]["text"].strip()
                elif resp.status_code == 429:
                    logger.warning("Gemini rate limit (429) hit, will fallback.")
                else:
                    logger.warning(f"Gemini API returned status {resp.status_code}: {resp.text[:200]}")
        except Exception as e:
            logger.warning(f"Gemini generation exception: {e}")

        return None

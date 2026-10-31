"""
KhetGPT LLM Provider Abstraction
Defines the base interface for interchangeable language model providers.
"""

from abc import ABC, abstractmethod
from typing import List, Dict, Any, Optional

class BaseLLMProvider(ABC):
    """Abstract base class for all LLM providers (Gemini, Groq, etc.)"""

    @abstractmethod
    def is_available(self) -> bool:
        """Returns True if the provider has valid credentials and is ready."""
        pass

    @abstractmethod
    def generate(
        self,
        messages: List[Dict[str, str]],
        system_prompt: Optional[str] = None,
        max_tokens: int = 450,
        temperature: float = 0.2
    ) -> Optional[str]:
        """Generates a text completion for given messages."""
        pass

    @property
    @abstractmethod
    def provider_name(self) -> str:
        """Returns the provider identifier name (e.g. 'gemini', 'groq')."""
        pass

    @property
    @abstractmethod
    def model_name(self) -> str:
        """Returns the specific model identifier (e.g. 'gemini-1.5-flash', 'qwen/qwen3.8-27b')."""
        pass


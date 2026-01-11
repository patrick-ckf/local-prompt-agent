"""LLM Backend implementations."""

from local_prompt_agent.backends.base import Backend
from local_prompt_agent.backends.ollama import OllamaBackend

__all__ = ["Backend", "OllamaBackend"]

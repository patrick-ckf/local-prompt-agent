# -*- coding: utf-8 -*-
"""
Base backend interface for LLM providers.

Following Rule #1: Keep it simple - clear interface, easy to implement.
"""

from abc import ABC, abstractmethod
from typing import Any, AsyncIterator, Dict, List, Optional


class Message:
    """Simple message class."""

    def __init__(self, role: str, content: str):
        self.role = role  # "user", "assistant", "system"
        self.content = content

    def to_dict(self) -> Dict[str, str]:
        """Convert to dictionary."""
        return {"role": self.role, "content": self.content}


class Backend(ABC):
    """
    Abstract base class for LLM backends.

    Simple interface - just complete() and stream().
    """

    def __init__(self, config: Dict[str, Any]):
        """
        Initialize backend with configuration.

        Args:
            config: Backend configuration dictionary
        """
        self.config = config
        self.model = config.get("model", "default")
        self.temperature = config.get("temperature", 0.7)
        self.max_tokens = config.get("max_tokens", 2048)

    @abstractmethod
    async def complete(
        self,
        messages: List[Message],
        **kwargs: Any,
    ) -> str:
        """
        Generate a completion for the given messages.

        Args:
            messages: List of conversation messages
            **kwargs: Additional backend-specific parameters

        Returns:
            Generated response text

        Raises:
            Exception: If completion fails
        """
        pass

    @abstractmethod
    async def stream(
        self,
        messages: List[Message],
        **kwargs: Any,
    ) -> AsyncIterator[str]:
        """
        Stream a completion token by token.

        Args:
            messages: List of conversation messages
            **kwargs: Additional backend-specific parameters

        Yields:
            Generated tokens

        Raises:
            Exception: If streaming fails
        """
        pass

    async def health_check(self) -> bool:
        """
        Check if backend is healthy and accessible.

        Returns:
            True if backend is accessible, False otherwise
        """
        try:
            # Simple test message
            test_msg = [Message("user", "Hi")]
            response = await self.complete(test_msg)
            return response is not None and len(response) > 0
        except Exception:
            return False

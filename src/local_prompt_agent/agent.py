# -*- coding: utf-8 -*-
"""
Core Agent class - the main interface for interacting with LLMs.

Simple, clean interface following Rule #1: Keep it simple.
"""

from typing import AsyncIterator, List, Optional

from local_prompt_agent.backends.base import Backend, Message
from local_prompt_agent.backends.ollama import OllamaBackend
from local_prompt_agent.config import Config


class Agent:
    """
    Main Agent class for executing prompts.

    Simple interface:
    - execute(): Get a complete response
    - stream(): Get streaming response
    - chat(): Interactive conversation
    """

    def __init__(self, config: Optional[Config] = None):
        """
        Initialize agent with configuration.

        Args:
            config: Configuration object (uses defaults if None)
        """
        if config is None:
            from local_prompt_agent.config import load_config

            config = load_config()

        self.config = config
        self.backend = self._initialize_backend()
        self.conversation_history: List[Message] = []
        self.system_prompt: Optional[str] = None

    def _initialize_backend(self) -> Backend:
        """
        Initialize the LLM backend based on configuration.

        Returns:
            Backend instance

        Raises:
            ValueError: If backend type is unsupported
        """
        backend_config = self.config.backend.model_dump()
        backend_type = backend_config.get("type", "ollama")

        if backend_type == "ollama":
            return OllamaBackend(backend_config)
        else:
            raise ValueError(f"Unsupported backend type: {backend_type}")

    def set_system_prompt(self, prompt: str) -> None:
        """
        Set system prompt for agent behavior.

        Args:
            prompt: System prompt text
        """
        self.system_prompt = prompt

    def clear_history(self) -> None:
        """Clear conversation history."""
        self.conversation_history = []

    async def execute(
        self,
        message: str,
        use_history: bool = True,
    ) -> str:
        """
        Execute a prompt and get complete response.

        Args:
            message: User message/prompt
            use_history: Include conversation history

        Returns:
            Agent's response

        Example:
            >>> agent = Agent()
            >>> response = await agent.execute("Hello!")
            >>> print(response)
        """
        # Build messages list
        messages = []

        # Add system prompt if set
        if self.system_prompt:
            messages.append(Message("system", self.system_prompt))

        # Add history if requested
        if use_history:
            messages.extend(self.conversation_history)

        # Add current message
        user_msg = Message("user", message)
        messages.append(user_msg)

        # Get response from backend
        response_text = await self.backend.complete(messages)

        # Save to history
        if use_history:
            self.conversation_history.append(user_msg)
            self.conversation_history.append(Message("assistant", response_text))

        return response_text

    async def stream(
        self,
        message: str,
        use_history: bool = True,
    ) -> AsyncIterator[str]:
        """
        Execute prompt with streaming response.

        Args:
            message: User message/prompt
            use_history: Include conversation history

        Yields:
            Response tokens as they're generated

        Example:
            >>> agent = Agent()
            >>> async for token in agent.stream("Tell me a story"):
            ...     print(token, end='', flush=True)
        """
        # Build messages list
        messages = []

        # Add system prompt if set
        if self.system_prompt:
            messages.append(Message("system", self.system_prompt))

        # Add history if requested
        if use_history:
            messages.extend(self.conversation_history)

        # Add current message
        user_msg = Message("user", message)
        messages.append(user_msg)

        # Stream response
        full_response = ""
        async for token in self.backend.stream(messages):
            full_response += token
            yield token

        # Save to history
        if use_history:
            self.conversation_history.append(user_msg)
            self.conversation_history.append(Message("assistant", full_response))

    async def health_check(self) -> bool:
        """
        Check if backend is healthy.

        Returns:
            True if backend is accessible
        """
        return await self.backend.health_check()

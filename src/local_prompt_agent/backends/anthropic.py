# -*- coding: utf-8 -*-
"""
Anthropic/Claude backend implementation.

Supports Claude 3 models.
"""

from typing import Any, AsyncIterator, Dict, List

try:
    from anthropic import AsyncAnthropic
except ImportError:
    AsyncAnthropic = None

from local_prompt_agent.backends.base import Backend, Message


class AnthropicBackend(Backend):
    """
    Anthropic backend for Claude models.

    Supports Claude 3 Opus, Sonnet, Haiku.
    """

    def __init__(self, config: Dict[str, Any]):
        """
        Initialize Anthropic backend.

        Args:
            config: Configuration with api_key, model, etc.
        """
        super().__init__(config)
        
        if AsyncAnthropic is None:
            raise ImportError(
                "anthropic package required. Install with: pip install anthropic"
            )
        
        api_key = config.get("api_key")
        if not api_key:
            raise ValueError(
                "Anthropic API key is required. "
                "Set in config or ANTHROPIC_API_KEY environment variable"
            )
        
        self.client = AsyncAnthropic(api_key=api_key)
        self.timeout = config.get("timeout", 60)

    async def complete(
        self,
        messages: List[Message],
        **kwargs: Any,
    ) -> str:
        """
        Generate completion using Claude.

        Args:
            messages: Conversation messages
            **kwargs: Additional parameters

        Returns:
            Generated response text
        """
        # Separate system message if present
        system_message = None
        formatted_messages = []
        
        for msg in messages:
            if msg.role == "system":
                system_message = msg.content
            else:
                formatted_messages.append(msg.to_dict())

        # Call Claude API
        response = await self.client.messages.create(
            model=self.model,
            max_tokens=kwargs.get("max_tokens", self.max_tokens),
            temperature=kwargs.get("temperature", self.temperature),
            system=system_message,
            messages=formatted_messages,
        )

        return response.content[0].text

    async def stream(
        self,
        messages: List[Message],
        **kwargs: Any,
    ) -> AsyncIterator[str]:
        """
        Stream completion from Claude token by token.

        Args:
            messages: Conversation messages
            **kwargs: Additional parameters

        Yields:
            Generated tokens
        """
        # Separate system message
        system_message = None
        formatted_messages = []
        
        for msg in messages:
            if msg.role == "system":
                system_message = msg.content
            else:
                formatted_messages.append(msg.to_dict())

        # Stream from Claude
        async with self.client.messages.stream(
            model=self.model,
            max_tokens=kwargs.get("max_tokens", self.max_tokens),
            temperature=kwargs.get("temperature", self.temperature),
            system=system_message,
            messages=formatted_messages,
        ) as stream:
            async for text in stream.text_stream:
                yield text

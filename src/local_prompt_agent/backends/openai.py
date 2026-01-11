# -*- coding: utf-8 -*-
"""
OpenAI backend implementation.

Supports GPT-4, GPT-3.5, and other OpenAI models.
"""

from typing import Any, AsyncIterator, Dict, List

from openai import AsyncOpenAI

from local_prompt_agent.backends.base import Backend, Message


class OpenAIBackend(Backend):
    """
    OpenAI backend for cloud LLMs.

    Supports GPT-4, GPT-3.5-turbo, etc.
    """

    def __init__(self, config: Dict[str, Any]):
        """
        Initialize OpenAI backend.

        Args:
            config: Configuration with api_key, model, etc.
        """
        super().__init__(config)
        
        api_key = config.get("api_key")
        if not api_key:
            raise ValueError(
                "OpenAI API key is required. "
                "Set it in config.yaml or environment variable OPENAI_API_KEY"
            )
        
        self.client = AsyncOpenAI(api_key=api_key)
        self.timeout = config.get("timeout", 60)

    async def complete(
        self,
        messages: List[Message],
        **kwargs: Any,
    ) -> str:
        """
        Generate completion using OpenAI.

        Args:
            messages: Conversation messages
            **kwargs: Additional parameters

        Returns:
            Generated response text
        """
        # Format messages for OpenAI
        formatted_messages = [msg.to_dict() for msg in messages]

        # Call OpenAI API
        response = await self.client.chat.completions.create(
            model=self.model,
            messages=formatted_messages,
            temperature=kwargs.get("temperature", self.temperature),
            max_tokens=kwargs.get("max_tokens", self.max_tokens),
            stream=False,
        )

        return response.choices[0].message.content

    async def stream(
        self,
        messages: List[Message],
        **kwargs: Any,
    ) -> AsyncIterator[str]:
        """
        Stream completion from OpenAI token by token.

        Args:
            messages: Conversation messages
            **kwargs: Additional parameters

        Yields:
            Generated tokens
        """
        # Format messages
        formatted_messages = [msg.to_dict() for msg in messages]

        # Stream from OpenAI
        stream = await self.client.chat.completions.create(
            model=self.model,
            messages=formatted_messages,
            temperature=kwargs.get("temperature", self.temperature),
            max_tokens=kwargs.get("max_tokens", self.max_tokens),
            stream=True,
        )

        async for chunk in stream:
            if chunk.choices[0].delta.content:
                yield chunk.choices[0].delta.content

    async def list_models(self) -> List[str]:
        """
        List available OpenAI models.

        Returns:
            List of model IDs
        """
        try:
            models = await self.client.models.list()
            return [model.id for model in models.data if "gpt" in model.id.lower()]
        except Exception:
            # Return common models if API call fails
            return ["gpt-4", "gpt-4-turbo", "gpt-3.5-turbo"]

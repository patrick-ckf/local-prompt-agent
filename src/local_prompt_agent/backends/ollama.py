# -*- coding: utf-8 -*-
"""
Ollama backend implementation.

Supports local LLM execution via Ollama.
Simple, privacy-first approach.
"""

import json
from typing import Any, AsyncIterator, Dict, List

import aiohttp

from local_prompt_agent.backends.base import Backend, Message


class OllamaBackend(Backend):
    """
    Ollama backend for local LLMs.

    Connects to Ollama API running locally.
    """

    def __init__(self, config: Dict[str, Any]):
        """
        Initialize Ollama backend.

        Args:
            config: Configuration with base_url, model, etc.
        """
        super().__init__(config)
        self.base_url = config.get("base_url", "http://localhost:11434")
        self.timeout = config.get("timeout", 60)

    async def complete(
        self,
        messages: List[Message],
        **kwargs: Any,
    ) -> str:
        """
        Generate completion using Ollama.

        Args:
            messages: Conversation messages
            **kwargs: Additional parameters

        Returns:
            Generated response text
        """
        url = f"{self.base_url}/api/chat"

        # Format messages for Ollama
        formatted_messages = [msg.to_dict() for msg in messages]

        payload = {
            "model": self.model,
            "messages": formatted_messages,
            "stream": False,
            "options": {
                "temperature": kwargs.get("temperature", self.temperature),
                "num_predict": kwargs.get("max_tokens", self.max_tokens),
            },
        }

        async with aiohttp.ClientSession() as session:
            async with session.post(
                url,
                json=payload,
                timeout=aiohttp.ClientTimeout(total=self.timeout),
            ) as response:
                if response.status != 200:
                    error_text = await response.text()
                    raise Exception(
                        f"Ollama API error: {response.status} - {error_text}"
                    )

                data = await response.json()
                return data["message"]["content"]

    async def stream(
        self,
        messages: List[Message],
        **kwargs: Any,
    ) -> AsyncIterator[str]:
        """
        Stream completion from Ollama token by token.

        Args:
            messages: Conversation messages
            **kwargs: Additional parameters

        Yields:
            Generated tokens
        """
        url = f"{self.base_url}/api/chat"

        # Format messages
        formatted_messages = [msg.to_dict() for msg in messages]

        payload = {
            "model": self.model,
            "messages": formatted_messages,
            "stream": True,
            "options": {
                "temperature": kwargs.get("temperature", self.temperature),
                "num_predict": kwargs.get("max_tokens", self.max_tokens),
            },
        }

        async with aiohttp.ClientSession() as session:
            async with session.post(
                url,
                json=payload,
                timeout=aiohttp.ClientTimeout(total=self.timeout),
            ) as response:
                if response.status != 200:
                    error_text = await response.text()
                    raise Exception(
                        f"Ollama API error: {response.status} - {error_text}"
                    )

                # Stream response line by line
                async for line in response.content:
                    if line:
                        try:
                            data = json.loads(line)
                            if "message" in data:
                                content = data["message"].get("content", "")
                                if content:
                                    yield content

                            # Check if done
                            if data.get("done", False):
                                break
                        except json.JSONDecodeError:
                            continue

    async def list_models(self) -> List[str]:
        """
        List available Ollama models.

        Returns:
            List of model names
        """
        url = f"{self.base_url}/api/tags"

        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                if response.status != 200:
                    return []

                data = await response.json()
                return [model["name"] for model in data.get("models", [])]

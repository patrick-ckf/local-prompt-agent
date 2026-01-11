# -*- coding: utf-8 -*-
"""
Core Agent class - the main interface for interacting with LLMs.

Simple, clean interface following Rule #1: Keep it simple.
"""

from typing import AsyncIterator, List, Optional

from local_prompt_agent.backends.base import Backend, Message
from local_prompt_agent.backends.ollama import OllamaBackend
from local_prompt_agent.config import Config

try:
    from local_prompt_agent.backends.openai import OpenAIBackend
except ImportError:
    OpenAIBackend = None

try:
    from local_prompt_agent.backends.anthropic import AnthropicBackend
except ImportError:
    AnthropicBackend = None

try:
    from local_prompt_agent.rag.simple_rag import SimpleRAG
except ImportError:
    SimpleRAG = None

try:
    from local_prompt_agent.rag import RAGSystem
except ImportError:
    RAGSystem = None


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
        self.rag_system: Optional[Any] = None
        self.use_rag: bool = False

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
        elif backend_type == "openai":
            if OpenAIBackend is None:
                raise ImportError("openai package required. Already installed!")
            return OpenAIBackend(backend_config)
        elif backend_type == "anthropic":
            if AnthropicBackend is None:
                raise ImportError(
                    "anthropic package required. Install: pip install anthropic"
                )
            return AnthropicBackend(backend_config)
        else:
            raise ValueError(
                f"Unsupported backend: {backend_type}. "
                f"Supported: ollama, openai, anthropic"
            )

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

    def enable_rag(self, collection_name: str = "documents", use_simple: bool = True) -> None:
        """
        Enable RAG mode for document-based Q&A.

        Args:
            collection_name: Name of the document collection
            use_simple: Use SimpleRAG (fast, no ML) vs full RAG (slow, better quality)
        """
        if use_simple:
            # Use simple keyword-based RAG (fast, no dependencies!)
            if SimpleRAG is None:
                raise ImportError("SimpleRAG not available")
            self.rag_system = SimpleRAG()
        else:
            # Use full embedding-based RAG (slow but better)
            if RAGSystem is None:
                raise ImportError(
                    "Full RAG dependencies not installed. "
                    "Install with: pip install sentence-transformers chromadb"
                )
            self.rag_system = RAGSystem(collection_name=collection_name)
        
        self.use_rag = True

    def disable_rag(self) -> None:
        """Disable RAG mode."""
        self.use_rag = False

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

        # If RAG enabled, retrieve relevant context
        actual_message = message
        if self.use_rag and self.rag_system:
            rag_result = self.rag_system.query(message, k=5)
            if rag_result["has_results"]:
                # Augment message with retrieved context
                context = rag_result["context"]
                sources = ", ".join([s["file"] for s in rag_result["sources"]])
                actual_message = f"""Answer the question based on the following context.

Context from documents:
{context}

Question: {message}

Answer:"""
                # Add source info to response later
                self._last_rag_sources = rag_result["sources"]
            else:
                self._last_rag_sources = None
        else:
            self._last_rag_sources = None

        # Add current message
        user_msg = Message("user", actual_message)
        messages.append(user_msg)

        # Get response from backend
        response_text = await self.backend.complete(messages)

        # Add sources if RAG was used
        if self._last_rag_sources:
            sources_text = "\n\nSources:\n" + "\n".join(
                [f"- {s['file']}" for s in self._last_rag_sources]
            )
            response_text += sources_text

        # Save to history (save original user message, not augmented)
        if use_history:
            self.conversation_history.append(Message("user", message))
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

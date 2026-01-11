# -*- coding: utf-8 -*-
"""
Base tool class.

Simple tool interface following Rule #1: Keep it simple.
"""

from abc import ABC, abstractmethod
from typing import Any, Dict


class Tool(ABC):
    """
    Base class for all tools.

    Simple interface: just name, description, and execute().
    """

    def __init__(self, name: str, description: str):
        """
        Initialize tool.

        Args:
            name: Tool name
            description: What the tool does
        """
        self.name = name
        self.description = description

    @abstractmethod
    async def execute(self, **kwargs: Any) -> Dict[str, Any]:
        """
        Execute the tool.

        Args:
            **kwargs: Tool-specific parameters

        Returns:
            Result dictionary with 'success' and result data

        Example:
            return {"success": True, "result": "42"}
        """
        pass

    def get_schema(self) -> Dict[str, Any]:
        """
        Get OpenAI-compatible tool schema.

        Returns:
            Tool schema for function calling
        """
        return {
            "type": "function",
            "function": {
                "name": self.name,
                "description": self.description,
                "parameters": self.get_parameters(),
            },
        }

    @abstractmethod
    def get_parameters(self) -> Dict[str, Any]:
        """
        Get tool parameters schema.

        Returns:
            JSON schema for parameters
        """
        pass

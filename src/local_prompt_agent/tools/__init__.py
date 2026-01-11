"""Tool system for function calling."""

from local_prompt_agent.tools.base import Tool
from local_prompt_agent.tools.registry import ToolRegistry

__all__ = ["Tool", "ToolRegistry"]

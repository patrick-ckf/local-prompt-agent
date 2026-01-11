"""
Local Prompt Agent - Privacy-first local AI assistant.

A locally-hosted intelligent agent system for managing, optimizing,
and executing AI prompts against local or remote LLMs.
"""

__version__ = "0.1.0"
__author__ = "Patrick Cheung"

from local_prompt_agent.agent import Agent
from local_prompt_agent.config import Config

__all__ = ["Agent", "Config", "__version__"]

# -*- coding: utf-8 -*-
"""
Configuration settings using Pydantic.

Supports YAML files, environment variables, and defaults.
Following Rule #1: Keep it simple.
"""

from pathlib import Path
from typing import Any, Optional

import yaml
from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class BackendConfig(BaseSettings):
    """LLM Backend configuration."""

    type: str = Field(default="ollama", description="Backend type (ollama, openai)")
    base_url: str = Field(
        default="http://localhost:11434", description="Backend API URL"
    )
    model: str = Field(default="mistral", description="Model name")
    api_key: Optional[str] = Field(default=None, description="API key if needed")
    timeout: int = Field(default=60, description="Request timeout in seconds")
    max_tokens: int = Field(default=2048, description="Maximum tokens to generate")
    temperature: float = Field(default=0.7, description="Sampling temperature")


class DatabaseConfig(BaseSettings):
    """Database configuration."""

    url: str = Field(
        default="sqlite+aiosqlite:///data/conversations.db",
        description="Database connection URL",
    )
    echo: bool = Field(default=False, description="Echo SQL statements")


class SystemConfig(BaseSettings):
    """System-level configuration."""

    language: str = Field(default="en", description="UI language (en, zh-TW, zh-CN)")
    theme: str = Field(default="light", description="UI theme (light, dark)")
    log_level: str = Field(default="INFO", description="Logging level")
    data_dir: Path = Field(default=Path("data"), description="Data directory")


class Config(BaseSettings):
    """Main configuration class."""

    model_config = SettingsConfigDict(
        env_prefix="LPA_",
        env_nested_delimiter="__",
        case_sensitive=False,
    )

    system: SystemConfig = Field(default_factory=SystemConfig)
    backend: BackendConfig = Field(default_factory=BackendConfig)
    database: DatabaseConfig = Field(default_factory=DatabaseConfig)

    @classmethod
    def from_yaml(cls, path: Path) -> "Config":
        """Load configuration from YAML file."""
        if not path.exists():
            return cls()

        with open(path, "r", encoding="utf-8") as f:
            data = yaml.safe_load(f) or {}

        return cls(**data)

    def to_yaml(self, path: Path) -> None:
        """Save configuration to YAML file."""
        path.parent.mkdir(parents=True, exist_ok=True)

        with open(path, "w", encoding="utf-8") as f:
            yaml.dump(
                self.model_dump(mode="json"),
                f,
                default_flow_style=False,
                allow_unicode=True,
                encoding="utf-8",
            )


def load_config(config_path: Optional[Path] = None) -> Config:
    """
    Load configuration from file or use defaults.

    Args:
        config_path: Path to config file (default: config/config.yaml)

    Returns:
        Config instance
    """
    if config_path is None:
        config_path = Path("config/config.yaml")

    return Config.from_yaml(config_path)

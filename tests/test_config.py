# -*- coding: utf-8 -*-
"""Tests for configuration system."""

from pathlib import Path

import pytest

from local_prompt_agent.config import Config, load_config


def test_default_config() -> None:
    """Test default configuration."""
    config = Config()

    assert config.system.language == "en"
    assert config.backend.type == "ollama"
    assert config.backend.model == "mistral"
    assert config.database.url.startswith("sqlite")


def test_load_config_default() -> None:
    """Test loading config from default path."""
    config = load_config()

    assert config is not None
    assert isinstance(config, Config)


def test_config_model_dump() -> None:
    """Test config serialization."""
    config = Config()
    data = config.model_dump()

    assert "system" in data
    assert "backend" in data
    assert "database" in data

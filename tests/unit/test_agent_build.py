"""Hermetic construction tests for the agent factory (no model call, no subprocess)."""

from __future__ import annotations

import os

from pydantic import SecretStr
from pydantic_ai import Agent
from pydantic_ai.models.anthropic import AnthropicModel
from pydantic_ai.models.test import TestModel

from platform_core.agent import _scrubbed_env, build_agent  # pyright: ignore[reportPrivateUsage]
from platform_core.settings import Settings
from platform_core.tools import AuditReport


def test_build_agent_returns_agent_with_explicit_model() -> None:
    agent = build_agent(model=TestModel())
    assert isinstance(agent, Agent)
    assert agent.output_type is AuditReport


def test_build_agent_uses_settings_model_when_unspecified() -> None:
    settings = Settings(agent_model="test", anthropic_api_key=None)
    agent = build_agent(model=None, settings=settings)
    assert isinstance(agent, Agent)
    assert isinstance(agent.model, TestModel)
    assert agent.output_type is AuditReport


def test_build_agent_wires_anthropic_provider_from_secret_str() -> None:
    settings = Settings(
        agent_model="anthropic:claude-sonnet-4-6",
        anthropic_api_key=SecretStr("sk-ant-test-key"),
    )
    agent = build_agent(model=None, settings=settings)
    assert isinstance(agent.model, AnthropicModel)
    assert agent.output_type is AuditReport


def test_scrubbed_env_drops_secrets(monkeypatch: object) -> None:
    import pytest

    assert isinstance(monkeypatch, pytest.MonkeyPatch)
    monkeypatch.setenv("ANTHROPIC_API_KEY", "sk-ant-secret")
    monkeypatch.setenv("AWS_SECRET_ACCESS_KEY", "aws-secret")
    env = _scrubbed_env()
    assert "ANTHROPIC_API_KEY" not in env
    assert "AWS_SECRET_ACCESS_KEY" not in env
    assert set(env).issubset(set(os.environ))

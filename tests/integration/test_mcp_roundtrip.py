"""Integration: drive the real MCP server over stdio and assert the audit verdict.

Spawns ``example_mcp_server.server`` as a subprocess (no model / API key needed) and calls
the tool through a FastMCP client — the live agent↔tool transport proven at Milestone 1.
Marked ``integration`` so the credential-free commit/CI gate excludes it.
"""

from __future__ import annotations

import sys
from collections.abc import Callable, Iterable
from pathlib import Path

import pytest
from fastmcp import Client
from fastmcp.client.transports import StdioTransport
from fastmcp.exceptions import ToolError
from pydantic_ai import ModelMessage, ModelResponse, ToolCallPart
from pydantic_ai.models.function import AgentInfo, FunctionModel

from platform_core.agent import build_agent

pytestmark = pytest.mark.integration

MakeRepo = Callable[[Iterable[str]], Path]  # mirrors the make_repo fixture in conftest.py


async def test_audit_structure_over_stdio(make_repo: MakeRepo) -> None:
    repo = make_repo(["README.md", "pyproject.toml"])  # LICENSE missing -> drift
    transport = StdioTransport(
        command=sys.executable,
        args=["-m", "example_mcp_server.server"],
        cwd=str(repo.parent),
    )
    async with Client(transport) as client:
        result = await client.call_tool("audit_structure", {"path": str(repo)})
    report = result.data
    assert report.conforms is False
    assert "LICENSE" in report.missing


async def test_audit_structure_rejects_traversal_over_stdio(tmp_path: Path) -> None:
    transport = StdioTransport(
        command=sys.executable,
        args=["-m", "example_mcp_server.server"],
        cwd=str(tmp_path),
    )
    async with Client(transport) as client:
        with pytest.raises(ToolError, match="escapes allowed root"):
            await client.call_tool("audit_structure", {"path": "../.."})


async def test_audit_structure_rejects_non_directory_over_stdio(tmp_path: Path) -> None:
    file_path = tmp_path / "file.txt"
    file_path.write_text("x", encoding="utf-8")
    transport = StdioTransport(
        command=sys.executable,
        args=["-m", "example_mcp_server.server"],
        cwd=str(tmp_path),
    )
    async with Client(transport) as client:
        with pytest.raises(ToolError, match="is not an existing directory"):
            await client.call_tool("audit_structure", {"path": file_path.name})


async def test_build_agent_live_stdio_trajectory(
    make_repo: MakeRepo, monkeypatch: pytest.MonkeyPatch
) -> None:
    repo = make_repo(["README.md", "pyproject.toml"])
    monkeypatch.chdir(repo.parent)

    def decide(messages: list[ModelMessage], info: AgentInfo) -> ModelResponse:
        if len(messages) == 1:
            return ModelResponse(
                parts=[ToolCallPart(tool_name="audit_structure", args={"path": repo.name})]
            )
        tool_result = messages[-1].parts[0]
        content = getattr(tool_result, "content", {})
        return ModelResponse(
            parts=[
                ToolCallPart(
                    tool_name=info.output_tools[0].name,
                    args=content,
                )
            ]
        )

    agent = build_agent(model=FunctionModel(decide))
    result = await agent.run(f"Audit {repo.name}")
    assert result.output.conforms is False
    assert result.output.missing == ["LICENSE"]

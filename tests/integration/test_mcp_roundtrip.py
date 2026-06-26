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

pytestmark = pytest.mark.integration

MakeRepo = Callable[[Iterable[str]], Path]  # mirrors the make_repo fixture in conftest.py


async def test_audit_structure_over_stdio(make_repo: MakeRepo) -> None:
    repo = make_repo(["README.md", "pyproject.toml"])  # LICENSE missing -> drift
    transport = StdioTransport(command=sys.executable, args=["-m", "example_mcp_server.server"])
    async with Client(transport) as client:
        result = await client.call_tool("audit_structure", {"path": str(repo)})
    report = result.data
    assert report.conforms is False
    assert "LICENSE" in report.missing

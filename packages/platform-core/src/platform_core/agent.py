"""The runnable governance-audit agent (pydantic-ai) wired to the MCP server.

The agent reaches its tool through the example MCP server over stdio — the
headline "agent <-> MCP server runs end-to-end". The ``main`` entrypoint runs
the full LLM agent when ``ANTHROPIC_API_KEY`` is set, and otherwise falls back
to a direct MCP round-trip so the wiring is demonstrable with no credentials.
"""

from __future__ import annotations

import sys
from typing import TYPE_CHECKING

from fastmcp.client.transports import StdioTransport
from pydantic_ai import Agent
from pydantic_ai.mcp import MCPToolset

from platform_core.settings import Settings, load_settings
from platform_core.tracing import configure_tracing

if TYPE_CHECKING:
    from pydantic_ai.models import Model

SYSTEM_PROMPT = (
    "You are a governance-assurance assistant. Use the audit_structure tool to "
    "check a directory against the structure standard, then report any drift "
    "(missing required files) concisely."
)

#: Launch the example MCP server in THIS interpreter/venv over stdio.
_SERVER_ARGS = ["-m", "example_mcp_server.server"]


def _stdio_transport() -> StdioTransport:
    return StdioTransport(command=sys.executable, args=_SERVER_ARGS)


def build_agent(model: Model | str | None = None, settings: Settings | None = None) -> Agent:
    """Build the agent with the MCP toolset. Pass ``model`` (e.g. a TestModel) to override."""
    settings = settings or load_settings()
    return Agent(
        model or settings.agent_model,
        toolsets=[MCPToolset(_stdio_transport())],
        system_prompt=SYSTEM_PROMPT,
    )


async def _direct_mcp_roundtrip(target: str) -> None:
    """Prove the MCP-over-stdio wiring without an LLM (no-key fallback)."""
    from fastmcp import Client

    async with Client(_stdio_transport()) as client:
        result = await client.call_tool("audit_structure", {"path": target})
    print("[no ANTHROPIC_API_KEY -> direct MCP round-trip]")
    print(result.data)


def main() -> None:
    """Run the agent against a target directory (defaults to cwd)."""
    import anyio

    configure_tracing()
    settings = load_settings()
    target = sys.argv[1] if len(sys.argv) > 1 else "."

    if settings.anthropic_api_key:
        agent = build_agent(settings=settings)
        result = agent.run_sync(f"Audit the directory {target!r} and report any structure drift.")
        print(result.output)
    else:
        anyio.run(_direct_mcp_roundtrip, target)


if __name__ == "__main__":
    main()

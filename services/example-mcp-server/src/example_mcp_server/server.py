"""Governance-audit MCP server (FastMCP, stdio).

Exposes the shared ``platform_core.audit_structure`` logic as ONE verifiable MCP
tool. The audit logic lives in platform-core (single source), so the agent's
tool and this server never diverge.
"""

from mcp.server.fastmcp import FastMCP

from platform_core.tools import AuditReport, audit_structure

mcp = FastMCP("governance-audit")


@mcp.tool(name="audit_structure")
def audit_structure_tool(path: str) -> AuditReport:
    """Audit a directory against the structure standard; report drift (missing required files)."""
    return audit_structure(path)


def main() -> None:
    """Run the server over stdio (the default transport)."""
    mcp.run("stdio")


if __name__ == "__main__":
    main()

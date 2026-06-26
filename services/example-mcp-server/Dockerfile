# Containerised shipping artifact for the governance-audit MCP server (stdio).
# Build from the REPO ROOT (needs the workspace + platform-core):
#   docker build -f services/example-mcp-server/Dockerfile -t example-mcp-server:latest .
# Run (stdio; an MCP client launches it):
#   docker run -i --rm example-mcp-server:latest
# syntax=docker/dockerfile:1

FROM python:3.12.10-slim AS base

# Pinned uv (matches the dev toolchain) — declare the runtime, don't assume host tools.
COPY --from=ghcr.io/astral-sh/uv:0.11.18 /uv /uvx /bin/

WORKDIR /app
ENV UV_LINK_MODE=copy \
    UV_PROJECT_ENVIRONMENT=/app/.venv

# Workspace manifests + lock first (layer-cache friendly), then sources.
COPY pyproject.toml uv.lock .python-version README.md ./
COPY packages/ packages/
COPY services/ services/

# Reproducible install of the full workspace from the committed lock; no dev tooling.
RUN uv sync --frozen --all-packages --no-dev

# stdio transport: the MCP client attaches over stdin/stdout (docker run -i).
ENTRYPOINT ["uv", "run", "--no-dev", "python", "-m", "example_mcp_server.server"]

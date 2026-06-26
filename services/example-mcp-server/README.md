# example-mcp-server

A runnable [MCP](https://modelcontextprotocol.io) server from the
[`template-ai-monorepo`](../../README.md) reference template. It exposes the governance-audit tool
(`audit_structure`) over stdio so any MCP client — including the `platform-core` agent — can call it.

Import/build-isolated workspace member: depends on `platform-core` explicitly and imports no sibling service.

## Run

As a container (the shipping artefact — see `Dockerfile`):

```console
docker build -t example-mcp-server .
docker run -i example-mcp-server          # stdio transport
```

Or directly via the packaged console script (dev loop):

```console
uv run example-mcp-server
```

## MCP client config

```json
{ "mcpServers": { "example": { "command": "docker", "args": ["run", "-i", "example-mcp-server"] } } }
```

See `configs/mcp-config.template.json` for a ready-to-edit template.

## Tool

| Tool | Input | Output |
|---|---|---|
| `audit_structure` | `path` (repo/dir to audit) | `AuditReport` — `conforms`, `present`, `missing`, `target` |

Licensed Apache-2.0. Architecture and transport details in [`docs/ARCHITECTURE.md`](../../docs/ARCHITECTURE.md).

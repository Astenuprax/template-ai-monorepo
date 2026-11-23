---
id: REF-THREAT-001
type: REFERENCE
status: VERIFIED
gist: Trust boundaries, asset/threat inventory, and implemented mitigations for the governance-audit agent and stdio MCP server.
---

# Threat Model

This document records the security boundaries and implemented controls for `template-ai-monorepo` (`platform-core` and `example-mcp-server`).

## 1. Trust Boundaries

```text
User / CLI args ─▶ platform-core (agent.py, settings.py)
                      │
                      │  StdioTransport (allowlisted env via _scrubbed_env())
                      ▼
               example-mcp-server (server.py)
                      │
                      │  audit_structure(path, allowed_root=Path.cwd())
                      ▼
               Local Filesystem (confined to allowed_root)
```

1. **LLM / Tool-Call Boundary:** Untrusted or model-generated `path` arguments cross from the agent into `audit_structure_tool(path: str)`.
2. **Subprocess Environment Boundary:** `platform-core` spawns `example-mcp-server` as a child stdio process and must not leak host secrets (`ANTHROPIC_API_KEY`, cloud credentials) into the child environment.
3. **Container Runtime Boundary:** `example-mcp-server` ships a non-root container image intended to run with read-only root filesystem, no network, and dropped Linux capabilities.
4. **CI / Supply-Chain Boundary:** Third-party GitHub Actions, dependency resolution, and secret scanning.

## 2. Threats & Implemented Controls

| Threat | Control | Location |
| --- | --- | --- |
| Path traversal / arbitrary filesystem probing via `audit_structure` | Canonical `.resolve(strict=False)` + `is_relative_to(allowed_root)` + `is_dir()` enforced at the MCP boundary (`allowed_root=Path.cwd()`). The `allowed_root` parameter is not exposed in the MCP tool schema. | `packages/platform-core/src/platform_core/tools.py`, `services/example-mcp-server/src/example_mcp_server/server.py` |
| Secret leakage into MCP child subprocess | `_scrubbed_env()` restricts child environment variables to `_SAFE_SUBPROCESS_ENV_KEYS` (`PATH`, `SYSTEMROOT`, `TEMP`, `TMP`, `PATHEXT`, `HOME`, `LANG`). | `packages/platform-core/src/platform_core/agent.py` |
| Accidental API key exposure in logs or repr | `anthropic_api_key` typed as `pydantic.SecretStr | None` and unwrapped only when constructing `AnthropicProvider`. | `packages/platform-core/src/platform_core/settings.py`, `packages/platform-core/src/platform_core/agent.py` |
| Unbounded LLM/tool loop | `UsageLimits(request_limit=5, tool_calls_limit=5)` and structured `output_type=AuditReport`. | `packages/platform-core/src/platform_core/agent.py` |
| Container privilege escalation / network egress | Non-root `appuser`, direct venv `ENTRYPOINT`, and documented `--read-only --network=none --cap-drop=ALL` flags. | `services/example-mcp-server/Dockerfile`, `configs/mcp-config.template.json` |
| Compromised GitHub Actions tag or vulnerable dependency | 40-hex SHA-pinned Actions (`tests/test_structure.py`), `osv-scanner` (`uv.lock`), CycloneDX SBOM, `gitleaks`, and OpenSSF Scorecard. | `.github/workflows/ci.yml`, `.github/workflows/scorecard.yml` |

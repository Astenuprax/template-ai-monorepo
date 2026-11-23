# Changelog

All notable changes to this project are documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).
Released versions are derived from git tags via `hatch-vcs`; unreleased work
accumulates under `[Unreleased]` until a tag is cut.

## [1.0.0] - 2026-11-23

### Added

- Initial `uv` workspace spine: a `pydantic-ai` governance-audit agent
  (`platform-core`) reaching its tool through `example-mcp-server` over stdio.
- Canonical `allowed_root` path-jail boundary (`tools.py` + `server.py`),
  `SecretStr` + `AnthropicProvider` wiring (`settings.py` + `agent.py`),
  allowlisted stdio subprocess environment (`_scrubbed_env()`), `UsageLimits`,
  and non-root `appuser` container image.
- Repository furniture, `tests/test_structure.py` structure-lint gate,
  hermetic `FunctionModel` / `FunctionToolset` evals, live stdio MCP
  integration tests, CI matrix (`gate`, `check`, `sbom`, `osv-scan`,
  `actionlint`), and `docs/THREAT_MODEL.md`.

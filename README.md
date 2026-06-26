# template-ai-monorepo

A golden-standard template for AI/agentic Python monorepos, managed as a single `uv` workspace. The worked example is a `pydantic-ai` governance-audit agent (`platform-core`) that reaches a tool through an MCP server (`example-mcp-server`) over stdio, demonstrating a self-checking governance audit end to end.

[![CI](https://github.com/iitapanderson/template-ai-monorepo/actions/workflows/ci.yml/badge.svg)](https://github.com/iitapanderson/template-ai-monorepo/actions/workflows/ci.yml)
[![License: Apache-2.0](https://img.shields.io/badge/License-Apache_2.0-blue.svg)](LICENSE)
[![Python 3.12+](https://img.shields.io/badge/Python-3.12%2B-blue.svg)](https://www.python.org/downloads/)

## Quick start

```bash
uv sync --all-packages
uv run governance-agent .
```

`uv sync --all-packages` resolves and installs every workspace member into one shared environment. `uv run governance-agent .` runs the agent against the current directory: it audits the repository layout and reports structure drift against the embedded governance standards.

## Layout

```text
.
├── packages/
│   └── platform-core/         # pydantic-ai governance-audit agent
├── services/
│   └── example-mcp-server/    # MCP server (stdio) exposing the audit tool
├── tests/                     # pytest suite + test_structure.py structure-lint gate
├── docs/                      # project documentation
└── .github/                   # CI workflow (ci.yml) and repo metadata
```

## Quality gate

```bash
uvx pre-commit run --all-files
```

The gate runs `ruff` (lint + format), `pyright` in strict mode, and the structure-lint check at `tests/test_structure.py`, alongside the `pytest` suite.

## Governance

This template embodies the `repo-structure-standard`, `repo-hygiene`, and `governance-standards` standards; see `AGENTS.md` for the agent-facing contract and operating rules.

## License

Apache-2.0. See `LICENSE` for the full text and `NOTICE` for attribution.

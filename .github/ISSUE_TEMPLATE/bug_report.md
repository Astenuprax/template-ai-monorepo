---
name: Bug report
about: Report a defect in template-ai-monorepo (the governance-audit agent, example-mcp-server, or the quality gate)
title: "[Bug]: "
labels: bug
---

## Describe the bug

A clear and concise description of the defect. State which package or service is affected
(`platform-core` / `governance-agent`, `example-mcp-server`, or the structure-lint / pre-commit gate).

## To reproduce

Steps to reproduce the behaviour:

1. `uv sync --all-packages`
2. Run `uv run governance-agent .` (or the failing `ruff` / `pyright` / `pytest` command).
3. Provide the exact input, file, or path involved.
4. Observe the error.

Include the full command, the complete output or traceback, and the smallest input that triggers
the failure.

## Expected behaviour

A clear and concise description of what you expected to happen instead.

## Environment

- OS: (e.g. Windows 11, Ubuntu 24.04, macOS 14)
- Python: output of `python --version` (3.12+ required)
- uv version: output of `uv --version`
- Quality gate: which check failed (`ruff`, `pyright` strict, `pytest`, `tests/test_structure.py`, or `.pre-commit-config.yaml`)

## Additional context

Add any other context: relevant logs, the MCP stdio transcript, recent changes, or whether the
issue intersects the repo-structure-standard, repo-hygiene, or governance-standards conventions.

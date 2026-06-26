---
name: Feature request
about: Propose an enhancement to template-ai-monorepo
title: "[Feature] "
labels: enhancement
---

## Problem

Describe the limitation or gap. What are you trying to do, and where does the
current behaviour fall short? Reference the affected component where known: the
`platform-core` package (the pydantic-ai governance-audit agent), the
`example-mcp-server` service, the uv workspace, or the quality gate
(ruff, pyright strict, pytest, the `tests/test_structure.py` structure-lint,
or `.pre-commit-config.yaml`).

## Proposed solution

Describe the change you want. Be specific about the public surface it touches:
new agent tools, MCP tool/stdio contracts, CLI behaviour
(`uv run governance-agent .`), workspace layout, or the quality gate.
Note any new dependency and confirm it stays within `uv sync --all-packages`.
Changes to repository layout, file hygiene, or governance must remain
consistent with the repo-structure-standard, repo-hygiene, and
governance-standards conventions named in the project documentation.

## Alternatives

List the alternatives you considered (including doing nothing) and why the
proposed solution is preferable.

## Additional context

Add any other context: related issues or PRs, links, target Python version
(3.12+), example input/output, or constraints. Note any impact on the
Apache-2.0 licensing or NOTICE attribution.

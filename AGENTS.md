# AGENTS.md

Canonical onboarding guide for `template-ai-monorepo`. This file is the source of
truth; `CLAUDE.md` is a thin pointer to it. Read this before making changes.

The repository is a uv-workspace AI/agentic monorepo. The worked example is a
[pydantic-ai](https://ai.pydantic.dev) "governance-audit" agent that reaches a
tool through a [FastMCP](https://gofastmcp.com) server over stdio. Target runtime
is Python 3.12+, managed end to end by [uv](https://docs.astral.sh/uv/).

## Architecture

The repo is a single uv workspace with two members:

- **`platform-core`** (package) — the application. It holds the pydantic-ai agent
  (`governance-agent`), the audit tool the agent calls, typed settings, and OpenTelemetry
  tracing setup. This is where agent behaviour, prompts, and the tool contract live.
- **`example-mcp-server`** (service) — exposes the audit tool over **stdio** via a
  FastMCP server. The agent launches it as a subprocess and speaks MCP to it; there is
  no network listener and no broker.

The two members share **one `uv.lock` and one virtual environment**. The isolation
boundary here is **import and build isolation, not per-service dependency isolation**:
each member is its own installable distribution with its own `pyproject.toml`, build
metadata, and import root, so `platform-core` cannot accidentally import private
modules of `example-mcp-server` (or vice versa) without a declared dependency. They do
**not** get independent, divergent dependency trees — the workspace resolves a single
coherent dependency set for the whole repo. This keeps the example reproducible and the
lockfile authoritative, at the cost of not modelling true service-level dependency drift.

Data flow at runtime: `governance-agent` (in `platform-core`) constructs the pydantic-ai
agent, registers the MCP server as a tool source, spawns `example-mcp-server` over stdio,
and performs the audit round-trip. Tracing spans wrap the agent run and the tool call so
the MCP round-trip is observable end to end.

## Running it

```bash
# Sync the whole workspace into one venv (both members, all extras).
uv sync --all-packages

# Run the agent against the current directory.
uv run governance-agent .
```

`uv sync --all-packages` installs every workspace member into the shared environment from
the single `uv.lock`. `uv run governance-agent .` invokes the agent entry point exported by
`platform-core`.

**No-API-key path:** the default run requires no model credentials. When no LLM API key is
configured, `governance-agent` does a **direct MCP round-trip** — it starts
`example-mcp-server` over stdio, calls the audit tool, and returns the structured result
without ever calling a hosted model. This makes the example runnable, testable, and
demonstrable in a credential-free environment (including CI). Supplying a model key enables
the full agentic path where the LLM orchestrates the same tool.

## The quality gate

The credential-free gate is three tools plus a structure check:

```bash
uv run ruff check .
uv run ruff format --check .
uv run pyright            # strict mode
uv run pytest -m "not integration"
```

- **ruff** — lint and format. Must be clean.
- **pyright (strict)** — full strict-mode type checking across the workspace. Every package
  ships `py.typed`, so consumers and the checker get real types, not `Any`.
- **pytest** — runs with `-m "not integration"` for the default gate. **Integration tests
  are marked** (`@pytest.mark.integration`) and **excluded** from the credential-free gate
  because they require live credentials or external services; they are not part of the gate
  that must pass on every machine and in CI without secrets.
- **structure-lint** — `tests/test_structure.py` is a real test, not advisory. It asserts
  the on-disk layout against `CONFORMS_TO_STRUCTURE_VERSION` and **FAILS on drift** (a new
  top-level package without `py.typed`, a service without a `Dockerfile`, a docs file
  missing frontmatter, a member outside the declared workspace shape). When you change the
  repo's shape, you update the structure-lint expectations in the same change — the gate
  will not let drift land silently.

Run the same set locally that CI runs; `.pre-commit-config.yaml` wires ruff (and the fast
checks) so most failures surface before commit.

## Governance standards

This repository is built to externally maintained standards. They are referenced **by name
only** here — read the canonical documents, do not expect their bodies inline:

- **repo-structure-standard** — the canonical directory layout for the stack (workspace
  shape, src-layout, where packages versus services live). The structure-lint gate enforces
  conformance to a pinned version of this standard.
- **repo-hygiene** — the mechanical enforcement layer (frontmatter requirements, file
  placement, clean-repo rules) that the gates and pre-commit hooks operationalise.
- **governance-standards** — code-quality standards (typing, error handling, output
  contracts, idempotency) that `ruff`, `pyright --strict`, and `pytest` enforce in spirit.

When a convention below seems arbitrary, the rationale lives in one of those three
documents.

## Conventions

- **src-layout** — every package is `<member>/src/<package>/...`. Code is imported from the
  installed distribution, never from the repo root, so tests exercise what ships.
- **`py.typed` in every package** — typing is part of the public contract. A package without
  a `py.typed` marker fails the structure-lint gate.
- **A `Dockerfile` in every service** — `example-mcp-server` (and any future service) ships a
  `Dockerfile`. Packages that are libraries do not; services that run do. The structure-lint
  gate distinguishes the two.
- **`docs/` frontmatter** — every Markdown file under `docs/` carries **enum-valid YAML
  frontmatter** (a recognised `type`/`status` set, per repo-hygiene). Files missing or
  carrying invalid frontmatter fail the gate.
- **SHA-pinned GitHub Actions** — every `uses:` in `.github/workflows/` is pinned to a full
  commit SHA, not a moving tag. Supply-chain integrity over convenience.

---

Author: Phillip Anderson | Integrate-IT Australia
License: Apache-2.0 (see `LICENSE`; attribution in `NOTICE`).

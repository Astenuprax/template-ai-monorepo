---
id: ARCH-001
type: REFERENCE
status: VERIFIED
gist: How template-ai-monorepo wires a uv workspace, the platform-core pydantic-ai governance-audit agent, and an example-mcp-server over stdio into one import-isolated, gate-enforced repository.
---

# Architecture

`template-ai-monorepo` is a portfolio-grade template for AI/agentic Python projects. Its
worked example is a **governance-audit agent** (package `platform-core`, built on
[pydantic-ai](https://ai.pydantic.dev)) that reaches a single tool through an
**MCP server** (`example-mcp-server`, FastMCP over stdio). This document describes the
runtime topology, the agent <-> MCP data flow, the isolation model, and the quality gates.

Repository layout, mechanical hygiene, and code-quality conventions are enforced directly by
`.pre-commit-config.yaml`, `pyproject.toml`, and `tests/test_structure.py` (see `AGENTS.md`).

---

## 1. The uv workspace

The repo is a single [uv](https://docs.astral.sh/uv/) workspace: one root `pyproject.toml`
declares `[tool.uv.workspace]` members, and every package resolves against **one shared
lockfile** (`uv.lock`) into **one shared virtual environment** (`.venv`).

```
template-ai-monorepo/
  pyproject.toml            # workspace root: members, dev deps, tool config
  uv.lock                   # single resolved lock for the whole workspace
  packages/
    platform-core/          # pydantic-ai governance-audit agent
  services/
    example-mcp-server/     # FastMCP server exposing audit_structure (stdio)
  tests/
    test_structure.py       # structure-lint gate
  docs/
    ARCHITECTURE.md          # this file
  .pre-commit-config.yaml    # ruff + pyright(strict) + structure lint
  LICENSE                    # Apache-2.0, verbatim
  NOTICE                     # attribution
```

**Why a uv workspace.** A workspace gives one resolution graph, so the agent and the
server can never disagree on a shared dependency's version. `uv sync --all-packages`
installs every member editable in one pass; `uv run governance-agent .` launches the agent
entry point without per-package environment juggling. New members are added by dropping a
package under `packages/` and listing it in the workspace `members` glob — no new lock, no
new venv.

---

## 2. The `platform-core` agent runtime

`platform-core` is the agent package. Its runtime is split into four single-responsibility
modules so that configuration, behaviour, instrumentation, and tool wiring stay independently
testable.

| Module | Responsibility |
|---|---|
| `settings.py` | Typed configuration via `pydantic-settings` — `anthropic_api_key` (`SecretStr | None`) and `agent_model` loaded from environment / `.env`. |
| `tracing.py` | Optional `logfire` instrumentation setup (no-op when `logfire` is not installed). |
| `tools.py` | Defines `DEFAULT_REQUIRED`, the `AuditReport` Pydantic schema, and deterministic `audit_structure()` check logic with `allowed_root` confinement. |
| `agent.py` | Declares `_stdio_transport()` (`_scrubbed_env()`) / `MCPToolset`, constructs the pydantic-ai `Agent` (`output_type=AuditReport`), and provides the no-key `_direct_mcp_roundtrip` fallback. |

`agent.py` is the composition root: it reads `settings.py`, initialises `tracing.py`, builds
the agent with the toolset from `tools.py`, and runs it against a target directory passed on
the command line (`uv run governance-agent .`).

---

## 3. The `example-mcp-server`

`example-mcp-server` is a [FastMCP](https://github.com/modelcontextprotocol) server. It
exposes one tool, `audit_structure`, which checks a target directory (confined inside `cwd`)
for required root entries (`README.md`, `pyproject.toml`, `LICENSE`) and returns an `AuditReport`.

The server speaks the **Model Context Protocol over stdio**. It is not a long-lived network
service: the agent process spawns it as a subprocess, communicates over the child's
stdin/stdout, and tears it down when the run completes. stdio is chosen deliberately — it
needs no port, no auth surface, and no network egress, which keeps the template's threat
surface minimal and its example reproducible on any machine.

---

## 4. Agent <-> MCP data flow

```
            uv run governance-agent .
                      |
                      v
   +--------------------------------------+
   |  platform-core (agent.py)            |
   |  Agent(model, toolset, AuditReport)  |
   +--------------------------------------+
            |                  ^
            | spawn (stdio)    | AuditReport (drift)
            | tool call:       |
            | audit_structure  |
            v                  |
   +--------------------------------------+
   |  example-mcp-server (FastMCP)        |
   |  @tool audit_structure(path) -> drift|
   +--------------------------------------+
            |                  ^
            | reads files      | structural findings
            v                  |
        target directory (the repo under audit)
```

1. The agent run starts. pydantic-ai spawns `example-mcp-server` as a stdio subprocess via
   `_stdio_transport()` / `MCPToolset` in `agent.py`.
2. The model decides to call `audit_structure` with the target path. The call crosses the
   MCP stdio boundary as a structured request.
3. The server walks the target directory, compares it against the structure and hygiene
   expectations, and returns the discovered drift.
4. pydantic-ai validates and aggregates the findings into a typed **`AuditReport`** — the
   agent's result contract — which lists each structural deviation. The subprocess is then
   shut down.

The `AuditReport` is the only object the caller sees; the MCP transport, the subprocess
lifecycle, and the model's tool-selection are all internal to the run.

---

## 5. Isolation model

The workspace shares **one lockfile and one venv**, so isolation here is
**import + build isolation, not dependency isolation**:

- **Import isolation** — each package is its own importable distribution with its own
  `[project]` table, entry points, and public surface. `platform-core` imports nothing from
  `example-mcp-server`; their only contract is the MCP tool schema crossing stdio.
- **Build isolation** — each package builds and versions independently and could be
  published on its own.
- **Shared resolution (by design)** — because all members resolve against one lock, they
  cannot drift to conflicting versions of a shared dependency. The trade-off: the workspace
  does **not** provide per-package dependency isolation. A package needing a genuinely
  conflicting dependency set belongs in its own workspace, not as a member here.

---

## 6. Test and gate layers

Quality is enforced in layers, all run from the shared venv and wired into
`.pre-commit-config.yaml`:

| Layer | Tool | Checks |
|---|---|---|
| Lint / format | `ruff` | Style, import order, and lint rules across the workspace. |
| Types | `pyright` (strict) | Full strict static typing — the agent's typed settings and the `AuditReport` contract are verified at this layer. |
| Unit / behaviour | `pytest` | Agent and server logic, including the `audit_structure` tool and report assembly. |
| Structure lint | `tests/test_structure.py` | Asserts the repo matches the `[tool.structure_lint]` layout, frontmatter, and SHA-pinning rules. |

Local runs and CI invoke the same commands (`uv run ruff`, `uv run pyright`,
`uv run pytest`); `.pre-commit-config.yaml` runs them on commit so drift is caught before it
lands. The structure-lint gate is intentionally recursive: the template enforces on itself
the standard its example agent is built to detect.

---

*Author: Phillip Anderson. Licensed under Apache-2.0 (see `LICENSE`;
attribution in `NOTICE`).*

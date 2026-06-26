---
id: REF-STRUCTURE-001
type: REFERENCE
status: VERIFIED
gist: Canonical folder layout and naming contract for the template-ai-monorepo, enforced by tests/test_structure.py.
---

# Folders and Naming

This document is the human-readable narrative of the directory structure and naming
contract for `template-ai-monorepo`. It derives from the `repo-structure-standard`
(canonical layout per stack) and `repo-hygiene` (mechanical hygiene enforcement)
standards, and complies with the markdown frontmatter rules in `governance-standards`.

The contract described here is not advisory. `tests/test_structure.py` is the
executable enforcement — it asserts the root furniture, member layout, and frontmatter
rules below and fails the quality gate on drift. When this document and the test
disagree, the test wins; fix one to match the other in the same change.

## Root furniture

The repository root contains exactly the following structural members:

- `pyproject.toml` — the uv workspace root. Declares `[tool.uv.workspace]` with
  `members = ["packages/*", "services/*"]` and the shared tool configuration
  (`ruff`, `pyright` in strict mode, `pytest`). It is the workspace manifest, not a
  distributable package.
- `uv.lock` — the resolved, committed lockfile for the whole workspace. Regenerated
  by `uv sync --all-packages`; never hand-edited.
- `packages/` — importable library members (see below).
- `services/` — deployable runtime members (see below).
- `tests/` — the workspace-level test tree (see below).
- `docs/` — markdown knowledge artifacts (this file lives here).
- `.github/workflows/` — GitHub Actions CI definitions.
- `.pre-commit-config.yaml` — local quality gate (ruff, pyright, pytest, structure-lint).
- `README.md` — the project front door. Rendered on GitHub; carries no frontmatter.
- `LICENSE` — Apache-2.0, verbatim and unmodified.
- `NOTICE` — attribution: `Phillip Anderson | Integrate-IT Australia`.
- `.gitignore`, `.python-version` — standard repo meta.

## `packages/*` and `services/*` member layout

Every member of `packages/` and `services/` is a self-contained, individually
installable Python project using the **src-layout**:

```
<member>/
  pyproject.toml          # one per member; declares name, deps, build backend
  src/<import_name>/
    __init__.py
    py.typed              # PEP 561 marker — the member ships type information
    ...
  README.md               # optional, front-door only
```

Rules enforced for each member:

- **One `pyproject.toml` per member.** No member shares or inherits a manifest from
  another member. Shared tool config lives only in the root `pyproject.toml`.
- **src-layout is mandatory.** Importable code lives under `src/<import_name>/`, never
  at the member root. This prevents accidental imports of uninstalled code during test
  collection.
- **`py.typed` is required.** Each member ships the PEP 561 marker so downstream
  consumers and `pyright --strict` resolve the member's types.
- **Import name is stable.** The distribution name (e.g. `platform-core`) and the
  import name (e.g. `platform_core`) follow the standard hyphen-to-underscore mapping.

### `packages/` — libraries

Pure importable libraries with no runtime entrypoint of their own. The example is
`platform-core`, the pydantic-ai `governance-audit` agent. Libraries do **not** ship a
`Dockerfile`.

### `services/` — deployables

Runtime members that are deployed as a process. The example is `example-mcp-server`,
an MCP server reached over stdio. In addition to the member layout above, **every
service ships a `Dockerfile`** at the service root. `tests/test_structure.py` asserts
the presence of `services/*/Dockerfile`; a service without one fails the gate.

## `tests/` tree

The workspace test tree at the root mirrors the standard layout:

```
tests/
  unit/                   # fast, isolated, no external processes
  integration/            # marked with @pytest.mark.integration
  fixtures/               # shared test data and pytest fixtures (conftest.py)
  test_structure.py       # the executable structure-lint gate
```

- **`unit/`** holds deterministic tests with no network, filesystem, or subprocess
  dependencies.
- **`integration/`** holds tests that exercise the MCP stdio boundary or other live
  collaborators. Every such test carries the `@pytest.mark.integration` marker so it
  can be selected or excluded (`pytest -m "not integration"`).
- **`fixtures/`** holds shared fixtures and static test data; `conftest.py` exposes
  them to the tree.
- **`test_structure.py`** is the structure-lint gate itself and runs as part of the
  ordinary `pytest` invocation.

## `docs/` frontmatter contract

Every markdown file under `docs/` (this one included) MUST begin with a YAML
frontmatter block carrying exactly these four keys, per `governance-standards`:

```yaml
---
id: <STABLE-ID>
type: <SKILL|WORKFLOW|LESSON|ADR|REFERENCE>
status: <EXPERIMENTAL|VERIFIED|DEPRECATED>
gist: <one-line machine-readable summary>
---
```

- `id` is a stable, unique identifier (e.g. `REF-STRUCTURE-001`).
- `type` MUST be one of `SKILL`, `WORKFLOW`, `LESSON`, `ADR`, `REFERENCE`.
- `status` MUST be one of `EXPERIMENTAL`, `VERIFIED`, `DEPRECATED`.
- `gist` is a single line stating what the document is for.

`README.md`, `LICENSE`, and `NOTICE` are front-door / meta files and are exempt — they
render directly and carry no frontmatter. `tests/test_structure.py` asserts the
frontmatter contract for `docs/**/*.md`.

## GitHub Actions

CI definitions live under `.github/workflows/`. Every third-party action reference
MUST be **pinned to a full 40-character commit SHA**, never a floating tag such as
`@v4`. SHA-pinning is a supply-chain control required by `repo-hygiene`; the structure
gate flags any `uses:` line pinned to a mutable ref.

## Enforcement summary

| Contract | Enforced by | Standard |
| --- | --- | --- |
| Root furniture present | `tests/test_structure.py` | `repo-structure-standard` |
| src-layout + `py.typed` + one `pyproject.toml` per member | `tests/test_structure.py` | `repo-structure-standard` |
| `services/*/Dockerfile` present | `tests/test_structure.py` | `repo-structure-standard` |
| `tests/` tree shape and integration markers | `tests/test_structure.py` | `repo-structure-standard` |
| `docs/**` frontmatter contract | `tests/test_structure.py` | `governance-standards` |
| GitHub Actions SHA-pinned | `tests/test_structure.py` | `repo-hygiene` |

Run the gate with `uv run pytest tests/test_structure.py`, or the full quality gate
(`ruff`, `pyright --strict`, `pytest`) via `.pre-commit-config.yaml`.

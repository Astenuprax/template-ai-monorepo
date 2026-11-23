---
id: REF-STRUCTURE-001
type: REFERENCE
status: VERIFIED
gist: Canonical folder layout and naming contract for the template-ai-monorepo, enforced by tests/test_structure.py.
---

# Folders and Naming

This document is the human-readable narrative of the directory structure and naming
contract for `template-ai-monorepo`.

The contract described here is not advisory. `tests/test_structure.py` is the
executable enforcement — it asserts the root furniture, member layout, and frontmatter
rules below and fails the quality gate on drift. When this document and the test
disagree, the test wins; fix one to match the other in the same change.

## Root furniture

The authoritative, enforced set of required root entries is
`[tool.structure_lint].root_required` in `pyproject.toml`, asserted by
`tests/test_structure.py`. This narrative lists the same set (grouped for readability)
plus the structural directories; when the two disagree, the test wins.

**Workspace and build files**

- `pyproject.toml` — the uv workspace root. Declares `[tool.uv.workspace]` with
  `members = ["packages/*", "services/*"]`, the shared tool configuration (`ruff`,
  `pyright` in strict mode, `pytest`), and `[tool.structure_lint]`. It is the workspace
  manifest, not a distributable package.
- `uv.lock` — the resolved, committed lockfile for the whole workspace. Regenerated
  by `uv sync --all-packages`; never hand-edited.
- `.pre-commit-config.yaml` — local quality gate (ruff, pyright, pytest, structure-lint).
- `.python-version`, `.gitignore`, `.editorconfig` — standard repo meta.

**OSS furniture** (all required; all front-door / meta files, frontmatter-exempt)

- `README.md` — the project front door. Rendered on GitHub; carries no frontmatter.
- `LICENSE` — Apache-2.0, verbatim and unmodified.
- `NOTICE` — attribution: `Phillip Anderson`.
- `CHANGELOG.md`, `CODE_OF_CONDUCT.md`, `CONTRIBUTING.md`, `SECURITY.md` — standard OSS meta.
- `AGENTS.md`, `CLAUDE.md` — agent-instruction files.

`AGENTS.local.md` — the local home for per-clone agent notes — is **git-ignored**, not
furniture: you create it yourself and it is never committed. Because it is git-ignored the
structure-lint drops it before the root-markdown check, so it needs no allowlist entry.

**Structural directories**

- `packages/` — importable library members (see below).
- `services/` — deployable runtime members (see below).
- `tests/` — the workspace-level test tree (see below).
- `docs/` — markdown knowledge artifacts (this file lives here).
- `.github/workflows/` — GitHub Actions CI definitions.

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
  fixtures/               # shared static test data
  conftest.py             # shared pytest fixtures, exposed to the whole tree
  test_structure.py       # the executable structure-lint gate
```

- **`unit/`** holds deterministic tests with no network, filesystem, or subprocess
  dependencies.
- **`integration/`** holds tests that exercise the MCP stdio boundary or other live
  collaborators. Every such test carries the `@pytest.mark.integration` marker so it
  can be selected or excluded (`pytest -m "not integration"`).
- **`fixtures/`** holds shared static test data; `conftest.py` (at the `tests/` root,
  not under `fixtures/`) exposes the shared fixtures to the whole tree.
- **`test_structure.py`** is the structure-lint gate itself and runs as part of the
  ordinary `pytest` invocation.

## `docs/` frontmatter contract

Every markdown file under `docs/` (this one included) MUST begin with a YAML
frontmatter block carrying exactly these four keys:

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
`@v4`. SHA-pinning is a supply-chain control enforced by `tests/test_structure.py`, which
flags any `uses:` line pinned to a mutable ref.

## Enforcement summary

| Contract | Enforced by | Gate |
| --- | --- | --- |
| Root furniture present | `tests/test_structure.py` | `test_required_root_file_present` |
| src-layout + `py.typed` + one `pyproject.toml` per member | `tests/test_structure.py` | `test_every_member_has_typed_src_package` |
| `services/*/Dockerfile` present | `tests/test_structure.py` | `test_every_service_ships_a_dockerfile` |
| `tests/` tree shape and integration markers | `tests/test_structure.py` | `test_tests_tree_holds_only_tests_and_support` |
| `docs/**` frontmatter contract | `tests/test_structure.py` | `test_docs_knowledge_artefacts_have_enum_valid_frontmatter` |
| GitHub Actions SHA-pinned | `tests/test_structure.py` | `test_all_workflow_actions_are_sha_pinned` |

Run the gate with `uv run pytest tests/test_structure.py`, or the full quality gate
(`ruff`, `pyright --strict`, `pytest`) via `.pre-commit-config.yaml`.

# CLAUDE.md

Read **AGENTS.md** first — it is the canonical agent guide for this repository
(architecture, workspace layout, conventions, and task workflow). This file holds
only repo-specific pointers and does not duplicate it.

## Quick pointers

- **Quality gate:** run `uvx pre-commit run --all-files` before every commit
  (ruff + pyright strict + pytest).
- **Structure enforcement:** the repo layout is verified by `tests/test_structure.py`
  — keep new packages and services compliant or that gate fails.
- **Governance standards (apply by name):** `repo-structure-standard` (directory
  layout), `repo-hygiene` (mechanical cleanliness and frontmatter), and
  `governance-standards` (coding and authoring rules).

Maintainer: Phillip Anderson | Integrate-IT Australia.

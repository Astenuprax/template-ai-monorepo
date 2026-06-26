---
id: REF-PLANNING-001
type: REFERENCE
status: VERIFIED
gist: Lean Tier-0 planning templates (PLAN/TRACKER/DONE) demonstrating the project-planning-artifacts methodology for cloners to fill per project.
---

# Planning Templates (Tier-0)

This directory holds **lean Tier-0 planning templates** for `template-ai-monorepo`. They
demonstrate the `project-planning-artifacts` methodology so that anyone cloning this
template has a working planning surface from the first commit.

These files are **empty scaffolds**. They carry **no real project state** — every line is a
placeholder to be replaced when the template is cloned and a concrete project begins. Treat
them as the shape of the methodology, not as a record of work.

## What Tier-0 means

Tier-0 is the minimum durable planning surface a project needs to stay legible without
incurring process overhead. It is three files, no more:

| File | Role | Holds |
|---|---|---|
| `PLAN.md` | Intent | The goal, scope boundaries, constraints, and the ordered approach. The *what* and *why*. |
| `TRACKER.md` | Live state | Open work items, their status, blockers, and next action. The single source of in-flight truth. |
| `DONE.md` | Closed record | Completed items and explicitly deferred/abandoned decisions (with reason). Append-only. |

One durable state surface per repo: `TRACKER.md` is authoritative for what is in flight.
Agent or session memory is not a substitute for it. When an item closes, move it from
`TRACKER.md` to `DONE.md` rather than deleting it — the deferral record is part of the
project's history.

## How to use these (per clone)

1. **Fill `PLAN.md` first.** State the real goal, scope in/out, and the constraints
   (quality gate is ruff + pyright strict + pytest, plus the structure-lint gate at
   `tests/test_structure.py` and `.pre-commit-config.yaml`). Define done before starting.
2. **Work through `TRACKER.md`.** Add discrete, checkable items. Update status as work
   progresses — do not batch updates at the end. Record blockers inline.
3. **Close into `DONE.md`.** When an item is finished or a decision is deferred, append it
   with a one-line outcome. Keep `TRACKER.md` lean.

Do not commit these scaffolds unchanged as if they were a real plan. A cloned project with
the placeholder text still present has not started planning.

## Governance alignment

The structure and lifecycle of these artifacts follow the `project-planning-artifacts`
standard. Repository layout and clean-repo expectations are governed by the
`repo-structure-standard` and `repo-hygiene` standards; coding and telemetry conventions by
`governance-standards`. This README and the templates reference those standards by name and
do not restate their bodies.

> **Frontmatter note.** README basenames are exempt from the frontmatter gate (they render as
> the directory front door). The block above is carried deliberately, for consistency with the
> other REFERENCE artifacts indexed in this repository.

---

Author: Phillip Anderson | Integrate-IT Australia

---
id: REF-PLANNING-001
type: REFERENCE
status: VERIFIED
gist: Lean Tier-0 planning templates (PLAN/TRACKER/DONE) demonstrating the project-planning-artifacts methodology for cloners to fill per project.
---

# Planning Templates (Tier-0)

This directory holds the **Tier-0 planning surface** for `template-ai-monorepo`, following the
`project-planning-artifacts` methodology so that anyone cloning this template has a working
planning surface from the first commit.

As the archetype's reference impl this repo wears two hats: `ROADMAP.md` and `DEBT.md` carry
**real state** for this repo's own work, while `TRACKER.md` and `DONE.md` are **scaffolds** a
cloner fills per project. Decision content lives in `docs/adr/`, never in these files.

## What Tier-0 means

Tier-0 is the minimum durable planning surface a project needs to stay legible without
incurring process overhead. It is the four-file quartet (rate-of-change separated):

| File | Role | Holds |
|---|---|---|
| `ROADMAP.md` | Strategic arc | Where this is headed — target end-state + phased milestones. Decisions cited by ADR ID; zero decision content. Created lazily, once real roadmap content exists. |
| `TRACKER.md` | Live state | Open work items, their status, blockers, and next action. The single source of in-flight truth. |
| `DONE.md` | Closed record | Completed, verified work. Append-only. |
| `DEBT.md` | Deferred / gaps | Consciously-deferred work and known gaps, each with a reason and a trigger to revisit. The single home for "not yet done" work. |

One durable state surface per repo: `TRACKER.md` is authoritative for what is in flight.
Agent or session memory is not a substitute for it. When an item closes, move it from
`TRACKER.md` to `DONE.md` rather than deleting it; consciously-deferred work goes to
`DEBT.md`, not `DONE.md`.

## How to use these (per clone)

1. **Frame direction in `ROADMAP.md`** (lazily — once you have a real target end-state and
   phased path). State the strategic arc and constraints (quality gate is ruff + pyright
   strict + pytest, plus the structure-lint gate at `tests/test_structure.py` and
   `.pre-commit-config.yaml`). Keep decisions in `docs/adr/`, not here.
2. **Work through `TRACKER.md`.** Add discrete, checkable items. Update status as work
   progresses — do not batch updates at the end. Record blockers inline.
3. **Close into `DONE.md`** (completed work) **and `DEBT.md`** (deferred work / known gaps,
   with a reason and a trigger). Keep `TRACKER.md` lean.

Do not commit the `TRACKER.md`/`DONE.md` scaffolds unchanged as if they were a real plan. A
cloned project with the placeholder text still present has not started planning.

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

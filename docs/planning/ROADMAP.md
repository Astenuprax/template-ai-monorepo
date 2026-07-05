---
id: REF-ROADMAP-001
type: REFERENCE
status: VERIFIED
gist: Strategic arc for template-ai-monorepo — evolve the single reference impl into a Copier base+overlay template family; where it's headed and the phased path, decisions cited by ADR ID only.
---

# Roadmap

Last-updated: 2026-07-05 <!-- refresh to the current date (yyyy-mm-dd) on every edit; REF-PLANNING-ARTIFACTS cross-cutting rule -->

**Where this is headed** — the strategic arc only. *Why* each choice was made lives in the ADRs
(`docs/adr/`, cited by ID); *what's left to do* lives in the tracker; *known gaps/debt* live in `DEBT.md`;
*what shipped* lives in git history + `DONE.md`. This file carries no decision content.

## Context / goal

`template-ai-monorepo` is the v1 reference impl for the AI-monorepo archetype (a uv workspace: a pydantic-ai
agent in `packages/` reaching a tool through an MCP server in `services/`, one quality gate across all members).
The goal is to evolve it into a **Copier template family** — a stack-agnostic governance **base** plus composable
per-stack overlays — so governance is authored once and propagated by `copier update`, without rewriting the
working template. Full rationale, partition map, and empirical dry-run: `docs/spike-copier-partition.md`
(REF-SPIKE-COPIER-001) and ADR-0004.

## Target end-state

- **Three Copier layers:** `template-governance-base` (stack-agnostic furniture + lint harness) → `template-py-uv-workspace`
  (Python/uv content) → optional `template-mcp-capability` (the MCP service + roundtrip). Apply order base → python → mcp.
- **This repo = the composed materialization** of base + python-stack + mcp-capability, linked back to the base via
  `.copier-answers.*.yml` so it pulls governance updates while staying an ordinary (non-Jinja) working reference impl.
- **Realization is reference-impl-first:** base + Python are materialized; un-built stacks (PowerShell / M365 / generic)
  ship a declarative `*-structure-repo.md` contract, never a speculative tree — materialized only after a real build.
- **One base-owned structure-version integer** governs conformance across the family.

## Phased milestones

**Shipped (✓ — see git history / `DONE.md` / the named ADRs):**
- ✓ Extract `template-governance-base` (harness + furniture + shrink-floor tests); own CI gate. Tags `v0.1.0`–`v0.1.2`.
- ✓ Extract `template-py-uv-workspace` (Python/uv content, lint constants, `{% raw %}`-guarded CI).
- ✓ Extract `template-mcp-capability` (MCP service, config template, roundtrip test).
- ✓ Hoist `[tool.structure_lint]` data + two-tier non-overridable floor (config-hoist, ADR-0004; spike §4).
- ✓ Link this repo via `.copier-answers.{base,python,mcp}.yml` (per-overlay independent update proven).
- ✓ Planning taxonomy: `docs/planning/` ratified as the archetype home; canonical **TRACKER/DONE/ROADMAP/DEBT**
  quartet adopted (ADR-0004 decision 7; ADR-0005 retiring the interim `PLAN.md` scaffold).

**Remaining:**
- ☐ **Validate the no-MCP render path** — author a bare, non-MCP `agent.py` variant and prove a python-only render
  passes `pytest`/`pyright`(strict)/structure-lint green; only then is the partition "golden" (ADR-0004 decision 3 caveat).
- ☐ **Composite per-overlay structure-versioning** — codify from the first real independent two-overlay `copier update`
  (tracked `DEBT.md` D-8; deliberately deferred until a real exemplar exists — reference-impl-first).
- ☐ **Materialize the next stack** (PowerShell / M365 / generic) from a real build, promoting its contract to VERIFIED.

## Strategic alternatives rejected (arc-level only; see ADRs for full rationale)

- **A single hand-maintained repo (no family).** Rejected — governance drift across repos is the failure this exists to kill.
- **Cruft instead of Copier.** Rejected — Copier's per-overlay independent `copier update` is the mechanic the partition needs (ADR-0004 decision 2).
- **Bake MCP into the python stack.** Rejected — a separate optional `mcp-capability` overlay is lower-regret (ADR-0004 decision 3).
- **Speculative trees for un-built stacks.** Rejected — declarative contracts until a real build (reference-impl-first).

---

Author: Phillip Anderson | Integrate-IT Australia

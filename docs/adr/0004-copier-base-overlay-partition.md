---
id: ADR-0004
type: ADR
status: VERIFIED
gist: Adopt a Copier governance base + per-stack overlays (base + python-stack + optional mcp-capability), with materialized base/Python and declarative contracts for un-built stacks; this repo links to the base via copier-answers.
---

# ADR-0004 — Copier base+overlay partition for the template family

**Status:** VERIFIED (independent Tier-0 review returned GO-WITH-CHANGES on both lenses; all findings folded — see §Independent review).
**Date:** 2026-06-30.
**Supersedes/relates:** builds on ADR-0001 (uv workspace). Decision record only — the full evidence,
partition map, and dry-run results live in `docs/planning/spike-copier-partition.md` (REF-SPIKE-COPIER-001).

## Context

`template-ai-monorepo` is the v1 reference impl for the AI-monorepo archetype. The goal is to evolve it
into a **template family** — a stack-agnostic governance **base** + composable per-stack overlays — so
governance is authored once and propagated, without rewriting the working template. A GO-verdicted
read-only spike (two prior `/plan-review` passes) produced the partition map, a config-hoist verdict, a
tool comparison, and an empirical sandboxed Copier dry-run. This ADR records the ratified choices.

## Decision

1. **Partition** the repo into three Copier layers: **base** (`template-governance-base`), **python-stack**
   (`template-py-uv-workspace`), and an **optional `mcp-capability`** overlay (`template-mcp-capability`).
   All 59 tracked files are assigned a layer × mutation-class × rename-risk × shared-interface (spike §3).
2. **Tool: Copier.** Multi-overlay independent `copier update` is empirically confirmed (spike §6 TEST 3).
3. **MCP architecture B** — a separate *optional* `mcp-capability` overlay, not baked into python-stack
   (lower-regret direction; A→B re-split is expensive because Copier never deletes baked-in paths). "Done"
   is gated on **authoring a bare, non-MCP `agent.py` variant** (the existing `agent.py` is wholly MCP-coupled —
   imports `MCPToolset`, launches `example_mcp_server`) and proving the no-MCP render passes
   `pytest`/`pyright`/structure-lint green. No bare-Python exemplar exists yet (reference-impl-first caveat).
4. **Per-stack realization (R-A):** base + Python are **materialized**; un-built stacks (PowerShell, M365,
   projects, generic) are **declarative `*-structure-repo.md` contracts**, never speculative trees. A
   stack's tree is materialized only after a real reference build (reference-impl-first).
5. **This repo's link-back (R-B):** extract a **copy** of governance into `template-governance-base` (do not
   move/delete from this repo); link this repo via `.copier-answers.base.yml` so governance propagates by
   `copier update`. This repo is **not** Jinja-ified.
6. **Structure-version:** a **single base-owned integer**; composite per-overlay versioning is deferred to
   the register (codify from the first real two-overlay update).
7. **Planning taxonomy (WS-0): R2** — ratify `docs/planning/` as the AI-monorepo archetype canonical home;
   amend the standard (additive) rather than relocating the repo's tracker. The deferred-vs-DEBT tension is
   a non-conflict — one debt register suffices; no second file is added.
8. **Config-hoist (WS-2):** three list literals (`root_required`, `py_source_roots`, `member_roots`) move to
   `[tool.structure_lint]`; everything else stays harness-invariant; a base-enforced **non-overridable floor**
   asserts the overlay sets contain the mandatory keys (Form-vs-Substance), buying back the lost test
   independence.

## Empirical basis (dry-run, copier 9.16.0)

- GitHub Actions `${{ }}` **hard-fails** Jinja without `{% raw %}` → CI workflows raw-guarded/excluded.
- A **diverged** `uv.lock` 3-way merge injects conflict markers that break `tomllib` → lockfile
  templating-excluded, regenerated via `uv lock` post-render (a resolved lock is a generated artifact, never merged).
- Independent per-overlay `copier update` confirmed (base updated, python untouched, sha-identical).

## Consequences

- **Positive:** governance authored once, pulled via `copier update`; Copier's heavy machinery is bounded to
  the base (+Python); the working template is untouched and stays a clean reference impl; un-built stacks
  cost a one-page contract, not a speculative tree.
- **Negative / risks:** two HIGH silent-failure couplings to fix at build time — the `end-session` tracker
  probe miss and the version-marker ownership crossing the base↔python seam (spike §8.5 WS-6 #1/#2). Hoisting
  the lint reduces test independence (mitigated by the two-tier floor, spike §4.3). The no-MCP render path is
  unvalidated until a de-MCP'd `agent.py` is authored and rendered green.
- **Deferred (register):** composite per-overlay versioning; adding `.copier-answers.base.yml` to
  `ROOT_REQUIRED` for linked repos; the post-spike `/manage-rules` standards amendment + tracker-probe
  widening (separately signed).

## Independent review

Two independent Tier-0 reviewers (governance + technical lenses), each verifying against the live files.
**Verdict: GO-WITH-CHANGES on both lenses — no NO-GO.** Both confirmed `git ls-files = 59`, exact citations,
the verbatim §11 diff, the deferred-vs-DEBT non-conflict, and that the spike edits no standard. Two MAJOR
findings — the config-hoist floor gap and the wholly-MCP-coupled `agent.py` — plus the minor citation/wording
items were folded into the spike report (REF-SPIKE-COPIER-001 §13) and this ADR. A subsequent independent review
of the fold itself returned GO (no new defects; both MAJORs genuinely resolved). Nothing rose to a design defect. Full finding
list and resolutions: spike report §13.

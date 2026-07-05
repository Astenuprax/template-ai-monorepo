---
id: ADR-0005
type: ADR
status: VERIFIED
gist: Retire the interim docs/planning/PLAN.md scaffold and adopt the canonical ROADMAP.md as the strategic-arc member of the standard's TRACKER/DONE/ROADMAP/DEBT quartet; a new decision that complements — does not supersede — ADR-0004 decision 7.
---

# ADR-0005 — ROADMAP.md replaces the interim PLAN.md scaffold

## Status

Accepted. **Date:** 2026-07-05.

**Relates:** complements ADR-0004 decision 7 (which ratified `docs/planning/` as the archetype's canonical home) —
it does **not** supersede it. Decision 7 makes no PLAN-vs-ROADMAP naming choice, so it stands unaffected; ROADMAP
still lives in `docs/planning/`.

## Context

The canonical `project-planning-artifacts` standard defines the AI-monorepo Tier-0 planning surface as the
**TRACKER / DONE / ROADMAP / DEBT** quartet, with `docs/planning/ROADMAP.md` as the strategic-arc member. It has no
`PLAN` role, and it explicitly flags a standalone `PLAN.md` as a drift-prone synonym.

This repo had instead shipped an interim `docs/planning/PLAN.md` scaffold — a *per-work-item* plan template
(Context / Goals / Approach / Milestones), a role the standard does not name. Its "PLAN/TRACKER/DONE trio" framing
originated in the exploratory spike (REF-SPIKE-COPIER-001), never in a ratified decision, and it diverged from the
standard that this repo — the archetype's reference impl — exists to model.

## Decision

**Adopt the canonical `docs/planning/ROADMAP.md`** as the strategic-arc member of the quartet, and **retire the
non-canonical `PLAN.md` scaffold.**

- `ROADMAP.md` (REF-ROADMAP-001) carries the strategic arc only — target end-state + phased milestones — with zero
  decision content (decisions cited by ADR ID), consistent with the standard's ROADMAP role.
- It is **populated** for this repo (the reference-impl hat), symmetric with the already-populated `DEBT.md`; an
  empty scaffold would instead violate the standard's lazy-creation rule.
- No gate referenced `PLAN.md`, so its removal is gate-safe. The built overlays seed neither `PLAN.md` nor
  `ROADMAP.md`, so cloners and the overlay family are unaffected — no cross-repo change is required.

## Consequences

- **Positive:** the reference impl now conforms to the quartet it models; a cold reader gets a real strategic arc,
  and the PLAN/ROADMAP terminology drift between the standard and the exemplar is closed.
- **Neutral:** `docs/planning/` holds the exact quartet + its README index (5 files), clearing the folder-index
  hygiene WARN without an extra INDEX file.
- **Negative / risks:** none material — fully reversible via git; no downstream consumer depended on `PLAN.md`.

## Alternatives considered

- **Keep `PLAN.md`.** Rejected — it is a non-canonical role that drifts from the standard's quartet and, per the
  standard, reads as exactly the synonym-proliferation failure the one-name-per-role rule prevents.
- **Cosmetic rename `PLAN.md` → `ROADMAP.md` with the per-task-plan content intact.** Rejected — that content model
  is not the strategic-arc ROADMAP role; it would be a mislabelled file, not a conforming ROADMAP.

---

Author: Phillip Anderson | Integrate-IT Australia

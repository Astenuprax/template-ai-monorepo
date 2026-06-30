---
description: Repo-Template project-scope end-session orchestrator — overrides Phase 2 to aggregate commits across the family's sibling overlay repos into the handoff. Self-contained (replaces the user-scope orchestrator for this repo).
alias: /end-session
targets-spec: CORE-END-SESSION
spec-version: "1.0.0"
---

# /end-session — Repo-Template (cross-repo family override)

This repo is the **planning home** of a Copier base+overlay family whose work each session spans
FOUR repos: this one plus the sibling overlay repos. The user-scope orchestrator's Phase-2 handoff is
**cwd-scoped** (git state from this repo only), so it under-represents a session whose real commits
landed in `template-governance-base` / `template-py-uv-workspace` / `template-mcp-capability`. This
override changes **only the Bindings and Phase 2** (cross-repo aggregation); every other phase, gate,
and the §core-handoff safety floor are unchanged from the spec (`~/.agents/workflows/end-session.global.md`).

**Conventions adopted** (per spec §Project-agnostic scope): single-file registers under `docs/registers/`
+ `docs/planning/`, dated handoffs in `docs/sessions/` (gitignored — local-only journal), git without
worktree parallelism, Claude Code task primitives for background state.

## Bindings

| Binding | Value |
|---|---|
| `SESSIONS_DIR` | `docs/sessions` |
| `HANDOFF_GLOB` | `handoff-session*.md` |
| `REGISTER_ACTIVE` | `docs/registers/deferred-hardening.md` |
| `REGISTER_RESOLVED` | (unset — the register carries its own `## Closed` section) |
| `ID_PREFIXES` | `D\|WS\|ADR` |
| `CLOSED_STATUSES` | (unset — register-cleanup inject omitted) |
| `SESSION_NUM_RULE` | highest `HANDOFF_GLOB` number across `SESSIONS_DIR/` + `SESSIONS_DIR/archive/`, +1 |
| `WORKTREES_DIR` | (unset → Phase 4 omitted) |
| `DEFAULT_BRANCH` | `main` |
| `AGENT_BRANCH_PREFIX` | `agent-` |
| `PUSH_POLICY` | `confirm` |
| `LONG_RUNNING_PROCS` | `[]` |
| `INFRA_PROBES` | the 4 repos' `main` SHA + public/CI state (see Phase 2) |
| `SIBLING_REPOS` | `../template-governance-base`, `../template-py-uv-workspace`, `../template-mcp-capability` (project-specific; used by Phase 2 + the durable cross-repo sweep) |

Print the resolved table. Announce omitted phases with their reason (by design, not failure).

## Phase sequence

Same sequence as the spec. For each `fixed`/`inject` phase: evaluate the gate, then `Read` the module
and execute. Phases **0** (pre-close triage) and **3** (register cleanup) are inject slots with **no
content** here → omitted. Phase **6** (cache) self-skips (no `.agent/MANIFEST.json`).

| # | Phase | Gate | Module |
|---|-------|------|--------|
| 0 | Pre-close triage | — (omitted, no inject) | — |
| 1 | Git state + push | always (push gated by `PUSH_POLICY=confirm`) | `~/.agents/workflows/modules/core-git.md` |
| 2 | **Handoff (cross-repo)** | `SESSIONS_DIR` set AND (commits ≠ ∅ in THIS repo OR any `SIBLING_REPOS` OR modified files ≠ ∅) | `~/.agents/workflows/modules/core-handoff-hybrid.md` **+ the cross-repo extension below** |
| 3 | Register cleanup | — (omitted, no inject) | — |
| 4 | Worktree hygiene | `WORKTREES_DIR` unset → omitted | `~/.agents/workflows/modules/core-worktree.md` |
| 5 | Background cleanup | active wakeup/monitor/bg task exists | `~/.agents/workflows/modules/core-background-cleanup.md` |
| 6 | Cache sync | self-skips (no MANIFEST) | `~/.agents/workflows/modules/core-cache.md` |
| 7 | Skill-usage retro | skill/workflow exercised AND nameable friction | `~/.agents/workflows/modules/core-skill-retro.md` |
| 8 | Durable summary | always | `~/.agents/workflows/modules/core-durable-summary.md` |

Then **Step 3 — Phase-7 disposition census**: `Read` `~/.agents/workflows/modules/core-phase7-census.md`
and run its frozen append block verbatim (`disposition` from the Phase-7 outcome; `sessionRef` = your own
session id). Non-fatal.

## Phase 2 — cross-repo extension (the only contract-bearing change)

`core-handoff-hybrid` is used **unchanged** for the §core-handoff floor (write-before-archive, Unaccounted
carry-forward, free-text flagging, non-blocking reconcile, summary line, all 8 sections, Verification Gaps).
Two project augmentations, applied at the 2a scaffold and the 2d Gate-6 step:

1. **Commits set is the UNION across `THIS repo + SIBLING_REPOS`.** In 2a, after building this repo's
   `COMMITS_TSV`, append each sibling's session commits. Derive a sibling's session commits as those with
   author-date `>=` the **prior handoff's date** (parsed from the prior `HANDOFF_GLOB` filename
   `handoff-sessionN-YYYY-MM-DD.md`) — a per-repo `git -C <sibling> log --since=<date> --format=...`.
   The Commits table gains a leading **`Repo`** column; rows are grouped by repo. (Files Modified stays
   THIS-repo-scoped — sibling files live in their own repos; capture sibling file work in prose, not a table.)
2. **Gate 6 hash allowlist = the union set.** Every hash-shaped token in the handoff must exist in the
   union `COMMITS_TSV` (this repo ∪ siblings), not just this repo's — otherwise legitimate sibling-repo
   hashes false-fail as "fabricated." Build `SCAFFOLD_HASHES` from the union.

`INFRA_PROBES` for Phase 2's Infrastructure-State section: one line per repo (`THIS` + `SIBLING_REPOS`) —
`<repo>: <branch>@<short-sha>, <public|private>, <CI state>, <pushed|N-ahead>`, collected via
`git -C <repo> log -1` + `gh repo view`/`gh run list` (best-effort; skip gh if unavailable).

Everything else (the §core-handoff 7 properties, the size-gate direct-write path, archiving) is the base
module's behaviour, unchanged.

## Authorisation + hard rails

Per spec §Authorisation: invoking this authorises the commits + the `PUSH_POLICY=confirm` push **in THIS
repo only**. Sibling-repo and governance-estate (`~/.claude`/`~/.gemini`/`~/.agents`) commits are **outside**
the grant — surface them (Phase 1 governance-estate reminder; Phase 8 cross-repo sweep), never auto-commit.
Hard rails: fast-forward only; never `--force`/`--force-with-lease`/`--no-verify`; abort + report on any
non-ff or push failure.

## Locked design rules (spec §Locked design rules)

1. Orchestrator owns gating; modules execute unconditionally once read.
2. Orchestrator owns shared state; modules consume and return.
3. One-way dependency — this project orchestrator references global modules; never the reverse.

The §core-handoff override safety floor is non-negotiable: the Phase-2 extension above **adds** cross-repo
breadth, it does not drop any of the seven properties.

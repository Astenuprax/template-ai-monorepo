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
| `REGISTER_ACTIVE` | `docs/planning/DEBT.md` |
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
| 2 | **Handoff (cross-repo)** | `SESSIONS_DIR` set AND (commits ≠ ∅ in THIS repo OR any `SIBLING_REPOS` OR modified files ≠ ∅) | `~/.agents/workflows/modules/core-handoff.md` **+ the cross-repo extension below** |
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

`core-handoff.md` (status `VERIFIED`) is used **unchanged** for the §core-handoff floor (write-before-archive,
Unaccounted carry-forward, free-text flagging, non-blocking reconcile, summary line, all 8 sections,
Verification Gaps). Its own execution is a flat 5-step sequence — 1. Write the handoff directly, 2. Verify
non-zero size, 3. Reconcile the outgoing handoff, 4. Archive the prior handoff (bounded retention, keep last
3), 5. optional Gemini-usage cost-capture line — with no delegated-LLM prose step and therefore no
provenance-fabrication gate to extend. (This override previously targeted `core-handoff-hybrid.md`, a
5-sub-step decomposition that offloaded prose generation to Gemini Flash behind a Gate-6 fabrication check;
that module was retired 2026-07-01 after a real fabrication incident and the global orchestrator's Phase 2
switchpoint was flipped back to `core-handoff.md`. This override is updated to match.)

Two project augmentations, both applied while the agent executes **Step 1 — "Write the handoff"** (there is
no separate scaffold sub-step in `core-handoff.md` to anchor them to; Step 1 is where Commits, Files
Modified, and Infrastructure State are all assembled directly from git state, so the augmentation is folded
into that assembly rather than bolted on as a gate):

1. **Commits set is the UNION across `THIS repo + SIBLING_REPOS`.** While assembling the Commits section in
   Step 1, after building this repo's commit set, append each sibling's session commits. **Derive a
   sibling's session commits by SHA range, not by date:** parse that sibling's prior HEAD short-SHA from the
   **prior handoff's Infrastructure-State section** (the `<repo>: <branch>@<short-sha>` line this override
   writes — see `INFRA_PROBES` below) and run `git -C <sibling> log <prior-sha>..HEAD --format=...`. This is
   exact and **same-day-robust**. *Why not `--since=<prior-handoff-date>` (the original approach —
   replaced):* git resolves a bare, time-less date to the **current time-of-day**, not midnight, so on any
   same-calendar-day run `--since=<today>` silently drops every sibling commit made earlier that day — a
   total miss, not mere coarseness (caught session-9: it returned ZERO across all three siblings, all
   committed earlier the same day). **Fallback** only if a baseline SHA is unparseable (e.g. a prior handoff
   predating this override's Infrastructure-State format): `git -C <sibling> log --since="<date> 00:00:00"
   ...` — the explicit midnight defeats the time-of-day drop, though it still cannot separate two same-day
   sessions. The Commits table gains a leading **`Repo`** column; rows are grouped by repo. (Files Modified
   stays THIS-repo-scoped — `core-handoff.md`'s Files Modified table is native `git diff --numstat` output
   for the current repo only; sibling file work goes in prose/Notes, not a table.)
2. **There is no Gate-6-equivalent augmentation in `core-handoff.md`, and none is added.** The hybrid
   module's Gate 6 was a hash/path "no-extras" fabrication check needed only because that module delegated
   prose generation to Gemini Flash, which could invent sibling-repo-shaped hashes; widening its allowlist to
   the cross-repo union was this override's second augmentation. `core-handoff.md` has no delegated-LLM
   prose step — Claude writes the Commits table directly from git output it already holds, for both this
   repo and each sibling — so the entire class of risk Gate 6 defended against does not exist here. This
   augmentation point is dropped, not translated; no replacement gate is introduced.

`INFRA_PROBES` for Phase 2's Infrastructure-State section (populated as part of Step 1, unchanged from
before): one line per repo (`THIS` + `SIBLING_REPOS`) —
`<repo>: <branch>@<short-sha>, <public|private>, <CI state>, <pushed|N-ahead>`, collected via
`git -C <repo> log -1` + `gh repo view`/`gh run list` (best-effort; skip gh if unavailable).

Everything else (the §core-handoff 7 properties, the write-before-archive ordering, the bounded-retention
archiving, the optional Gemini-usage cost-capture line) is the base module's behaviour, unchanged.

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

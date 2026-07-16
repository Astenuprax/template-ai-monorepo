---
description: Repo-Template end-session — thin override; inherits the user-scope orchestrator and extends Phase 2 to aggregate commits across the family's sibling overlay repos.
alias: /end-session
targets-spec: CORE-END-SESSION
spec_version: "2026-07-17 (Python driver)"
---

# /end-session — Repo-Template (thin override, cross-repo family)

**Base:** `Read` `~/.agents/workflows/end-session.md` (user-scope orchestrator) and execute its Steps 1–3
with the bindings and deltas below. Phase tables, authorisation, hard rails, census, and locked rules live in
the base/spec — not restated here.

This repo is the **planning home** of a Copier base+overlay family whose work each session spans FOUR repos.
The base Phase-2 handoff is cwd-scoped, so it under-represents a session whose real commits landed in the
siblings — the Phase-2 extension below adds that breadth.

## Adopted / diverged conventions
- **Adopted:** single-file registers under `docs/planning/`; dated handoffs in
  `docs/sessions/` (gitignored — local-only journal); git without worktree parallelism; Claude Code task
  primitives for background state.
- **Omitted:** worktrees, cache manifest.

## Bindings (non-detectable only)
Pass at Step 1:
`--bindings '{"REGISTER_ACTIVE":"docs/planning/DEBT.md","REGISTER_RESOLVED":"docs/planning/DEBT.md","ID_PREFIXES":"D|WS|ADR"}'`
| Binding | Value |
|---|---|
| `REGISTER_ACTIVE` | `docs/planning/DEBT.md` (outside Probe's candidate list) |
| `REGISTER_RESOLVED` | same file — the register carries its own `## Closed` section. Supplying it suppresses the base's `registerResolvedMissing` remediation: do **NOT** create a `done.md` here. |
| `ID_PREFIXES` | `D\|WS\|ADR` |
| `INFRA_PROBES` | one line per repo (`THIS` + `SIBLING_REPOS`): `<repo>: <branch>@<short-sha>, <public\|private>, <CI state>, <pushed\|N-ahead>` — via `git -C <repo> log -1` + `gh repo view`/`gh run list` (best-effort; skip gh if unavailable) |
| `SIBLING_REPOS` | `../template-governance-base`, `../template-py-uv-workspace`, `../template-mcp-capability` |

## Phase deltas
- **Phase 2 gate widens:** run the handoff when commits ≠ ∅ in THIS repo **OR any `SIBLING_REPOS`** OR
  modified files ≠ ∅.
- **Phase 2 extension (contract-bearing — adds breadth, drops none of the §core-handoff floor):** while
  authoring the handoff (module step 1), the **Commit-range line's attribution notes UNION across
  `THIS repo + SIBLING_REPOS`** — the range line itself (`<fromSha>..<toSha> (N commits)`) stays THIS-repo-scoped
  from the driver's `fromSha`/`toSha`/`count` fields; each sibling gets its own attribution note (repo, sha
  range, commit count/subjects) appended below the range line, not a separate table. **Derive each sibling's
  session commits by SHA range, not by date:** parse the sibling's prior HEAD short-SHA from the **prior
  handoff's Infrastructure-State line** (the `<repo>: <branch>@<short-sha>` format above) and run
  `git -C <sibling> log <prior-sha>..HEAD`. *Why not `--since=<date>`:* git resolves a bare date to the
  current time-of-day, silently dropping every sibling commit made earlier the same day (total miss, caught
  session-9). **Fallback** only if a baseline SHA is unparseable: `git -C <sibling> log --since="<date>
  00:00:00"` — explicit midnight defeats the time-of-day drop, though it cannot separate two same-day
  sessions. Sibling file-level detail goes in prose/Notes for Next Session, never a Files-Modified table
  (retired from the base template — D3). No fabrication gate is added: Claude writes the attribution notes
  directly from git output it holds — the delegated-LLM-prose risk class the retired hybrid module's Gate 6
  defended against does not exist here.
- **Authorisation delta:** the end-session grant covers commits + the `confirm` push **in THIS repo only**.
  Sibling-repo and governance-estate commits are **outside** the grant — surface them (Phase 1 reminder;
  Phase 8 cross-repo sweep), never auto-commit.

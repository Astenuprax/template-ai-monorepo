---
id: DONE-TEMPLATE
type: REFERENCE
status: EXPERIMENTAL
gist: Append-only log of completed, verified work for template-ai-monorepo; deferred work and known gaps live in DEBT.md, not here.
---

# Done

<!--
USAGE (clone-to-start): append-only log of completed, verified work — never read for routine status.
- Append at the BOTTOM via a shell append (`>>` / `Add-Content`), one line per completed item or
  completed part of a still-open tracker row:
  `- <tracker-id> - <what shipped> - <yyyy-mm-dd> - <commit / proof> [- retro: <pointer>]`
- Remove the row from `docs/planning/TRACKER.md` when appending it here. Consciously-deferred work and
  known gaps belong in `docs/planning/DEBT.md`, not here. Cite the proof (gate run, test, commit), not
  the intention.
- Conventions follow "repo-structure-standard" (layout) and "repo-hygiene" (frontmatter, placement).
Example:
- P0.1 - `example-mcp-server` stdio transport wired - 2026-01-31 - abc1234 (`uv run pytest` green)
Author: Phillip Anderson | Integrate-IT Australia.
-->

### 2026-08-10 — Template-build exercise residuals dispositioned as superseded (migrated from retired `~/.claude` copy)

- **Scope:** Four exercise/verify residuals from the original template-build program, previously tracked only in the now-retired `~/.claude/docs/registers/template-program-roadmap.md` (a 45-day-stale external snapshot; its decisions were already promoted to `~/.claude` memories). Verbatim: **R-A** CI fails at runner-startup (private-repo Actions minutes — not a workflow defect; deferred: verify when repo goes public); **R-B** devcontainer authored-not-built; **R-C** `release.yml` not tag-exercised; **E2/G2** estate structure-marker scan deferred until ≥2 repos carry markers.
- **Outcome:** Recorded here as superseded/obsolete rather than carried as open DEBT — they were not tracked in this repo's own ROADMAP/DEBT, and the repo's subsequent `v0.1.0` tagging + per-overlay `.copier-answers.*` link-back (DEBT D-16 / LINK-BACK, dated after the residuals) overtook the CI/release/marker concerns.
- **Verified by:** Operator-directed disposition (2026-08-10). NOT independently re-verified live — `gh` repo-visibility/release-run and the estate-wide marker census both stalled (flaky auth / filesystem hydration). If any residual is later found live, refile it as a DEBT row with its trigger.
- **Notes:** Closes the finding from a `/manage-project-planning` audit of `~/.claude`, which identified `template-program-roadmap.md` as out-of-unit content belonging to this repo. That stale copy is being removed from `~/.claude` in the same pass.

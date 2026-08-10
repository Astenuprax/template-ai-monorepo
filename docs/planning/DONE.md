---
id: DONE-TEMPLATE
type: REFERENCE
status: EXPERIMENTAL
gist: Append-only log of completed, verified work for template-ai-monorepo; deferred work and known gaps live in DEBT.md, not here.
---

<!-- Append completed items at the top (newest first). Move closed items here from the tracker; never delete. Deferred or knowingly-incomplete work goes in the DEBT register (docs/planning/DEBT.md), not here. -->

# Done

Completed, verified work for `template-ai-monorepo`. Each entry records what shipped and how it was proven, so the planning surface reflects as-built reality rather than intent.

Conventions follow `repo-structure-standard` (layout) and `repo-hygiene` (frontmatter, placement); entry discipline follows `governance-standards`.

## Completed

<!-- One entry per shipped unit of work. Newest first. Cite the proof (gate run, test, command), not the intention. -->

### 2026-08-10 — Template-build exercise residuals dispositioned as superseded (migrated from retired `~/.claude` copy)

- **Scope:** Four exercise/verify residuals from the original template-build program, previously tracked only in the now-retired `~/.claude/docs/registers/template-program-roadmap.md` (a 45-day-stale external snapshot; its decisions were already promoted to `~/.claude` memories). Verbatim: **R-A** CI fails at runner-startup (private-repo Actions minutes — not a workflow defect; deferred: verify when repo goes public); **R-B** devcontainer authored-not-built; **R-C** `release.yml` not tag-exercised; **E2/G2** estate structure-marker scan deferred until ≥2 repos carry markers.
- **Outcome:** Recorded here as superseded/obsolete rather than carried as open DEBT — they were not tracked in this repo's own ROADMAP/DEBT, and the repo's subsequent `v0.1.0` tagging + per-overlay `.copier-answers.*` link-back (DEBT D-16 / LINK-BACK, dated after the residuals) overtook the CI/release/marker concerns.
- **Verified by:** Operator-directed disposition (2026-08-10). NOT independently re-verified live — `gh` repo-visibility/release-run and the estate-wide marker census both stalled (flaky auth / filesystem hydration). If any residual is later found live, refile it as a DEBT row with its trigger.
- **Notes:** Closes the finding from a `/manage-project-planning` audit of `~/.claude`, which identified `template-program-roadmap.md` as out-of-unit content belonging to this repo. That stale copy is being removed from `~/.claude` in the same pass.

### YYYY-MM-DD — <short title>

- **Scope:** <what changed — package/service/path, e.g. `platform-core` agent wiring, `example-mcp-server` stdio transport>.
- **Outcome:** <observable result the change delivers>.
- **Verified by:** <how it was proven — `uv run governance-agent .`, `ruff check`, `pyright` (strict), `pytest`, `tests/test_structure.py`, pre-commit hooks>.
- **Notes:** <decisions, follow-ups, or links to the originating tracker/ROADMAP item>.

<!-- Consciously-deferred work and known gaps do NOT live here — they belong in the dedicated DEBT register (`docs/planning/DEBT.md`), the single home for "not yet done" work per `repo-hygiene` §3. DONE.md records only *completed* work; DEBT.md owns the deferred/gap role. -->

<!-- Template — replace example entries with real ones. Author: Phillip Anderson | Integrate-IT Australia. -->

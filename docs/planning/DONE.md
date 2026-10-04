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

### 2026-10-04 — ND-E go/kill: six aging DEBT rows declined, D-20 narrowed

- **Scope:** W4.1 fleet sweep ND-E (aging rows 90-99 days). Evidence pass by agy, adjudicated by Claude, blind-lens UPHELD on every item, operator sign-off.
- **Outcome:** D-1, D-2, D-5, D-6, D-13, D-14 DECLINED (low ROI: latent or fail-closed, no live impact). Each row's own trigger stands: re-file if it fires. D-20 part (b) DONE (CLAUDE.md:8-10 carries the path-exact planning pointer block); part (a), the ADR-0004 Consequences correction, stays open as D-20.
- **Rows verbatim:**
  - | D-1 | **Full file-TYPE placement allowlist** in `tests/test_structure.py` (beyond the current `.py`/`.md` rules). | Opened: 2026-06-27 · reason: scope-cut · Phase-2 scope — the current gate polices the two highest-churn file types; a complete per-extension allowlist is broader than the spine needed. | A new file type needs placement rules, or the structure-standard adds a binding per-type rule. |
  - | D-2 | **Content-hash over the structure-lint rule set** so "rules changed ⇒ `CONFORMS_TO_STRUCTURE_VERSION` bump" is *enforced*, not discipline. Today the gate only asserts the in-test marker equals `[tool.structure_lint].version`. | Opened: 2026-06-27 · reason: scope-cut · Phase-2 scope — the cross-assert catches the common "bumped one integer, forgot the other" error; hashing the rule body is a stronger, later control. | The version-marker discipline proves insufficient (a rule changes without a bump), or the standard mandates the hash. |
  - | D-5 | **`_USES_REF` in `test_structure.py` matches `uses:` anywhere on a line, including comments.** A commented `# uses: actions/x@v4` would false-positive as unpinned. Direction is fail-closed (safe), so low priority. | Opened: 2026-06-27 · reason: low-priority · Cosmetic robustness; no live impact today (no such comment exists). | A legitimate comment ever trips the gate; then skip comment text before matching. |
  - | D-6 | **ruff version drift.** The pre-commit hook runs ruff from its own isolated env (`rev: v0.13.2`); CI and the `justfile` run `uv run ruff` (lock-pinned). The two can diverge on format/lint output. | Opened: 2026-06-27 · reason: low-priority · Low — both are recent; divergence is latent, not active. | First format/lint disagreement between the local hook and CI; align the versions (e.g. run ruff via `uv run` in the hook, or match the pins). |
  - | D-13 | **Family README copier recipes omit `--trust`, diverging from the CI render invocation.** The overlay READMEs render with bare `uvx copier copy --overwrite …` while every render-gate CI passes `--trust` to all layers. Verified 2026-06-30 (M6 red-team) that NO family template declares `_tasks`/`_jinja_extensions`/`_migrations`, so `--trust` is a **no-op today** — the README is correct without it and CI's `--trust` is defensive. The only residual is the README↔CI invocation divergence. | Opened: 2026-06-30 · reason: low-priority · Harmless until a family template adds a trust-gated feature (`_tasks` etc.); cosmetic otherwise. | Any family template adds a trust-gated feature (then the README recipe needs `--trust` to render fully), OR align CI to drop the unneeded `--trust`. |
  - | D-14 | **Image name/tag + run-flag drift in `example-mcp-server`.** The seed README's run line + MCP-client-config JSON use bare `example-mcp-server` (no tag, no `--rm`), while the `Dockerfile` header and `configs/mcp-config.template.json` use `example-mcp-server:latest` with `--rm`. Functionally harmless (docker resolves the missing tag to `:latest`, `--rm` is optional). The M6 docs fix aligned the README *build* command (the real breakage) but deliberately left this tag/flag axis. Source = exemplar `services/example-mcp-server/` + the `template-mcp-capability` overlay copy. | Opened: 2026-06-30 · reason: low-priority · Cosmetic stale-seed drift across three hand-authored artifacts; no functional impact. | Next docs pass on the example service — pick one canonical form (`docker run -i --rm example-mcp-server:latest`) and use it verbatim in README run line, README client-config JSON, and `mcp-config.template.json`. |

---
id: DONE-TEMPLATE
type: REFERENCE
status: EXPERIMENTAL
gist: Append-only log of completed work plus deferred/DEBT items for template-ai-monorepo.
---

<!-- Append completed items at the top (newest first). Move closed items here from PLAN/TRACKER; never delete. Deferred or knowingly-incomplete work goes under "Deferred / DEBT" with a reason and a trigger to revisit. -->

# Done

Completed, verified work for `template-ai-monorepo`. Each entry records what shipped and how it was proven, so the planning surface reflects as-built reality rather than intent.

Conventions follow `repo-structure-standard` (layout) and `repo-hygiene` (frontmatter, placement); entry discipline follows `governance-standards`.

## Completed

<!-- One entry per shipped unit of work. Newest first. Cite the proof (gate run, test, command), not the intention. -->

### YYYY-MM-DD — <short title>

- **Scope:** <what changed — package/service/path, e.g. `platform-core` agent wiring, `example-mcp-server` stdio transport>.
- **Outcome:** <observable result the change delivers>.
- **Verified by:** <how it was proven — `uv run governance-agent .`, `ruff check`, `pyright` (strict), `pytest`, `tests/test_structure.py`, pre-commit hooks>.
- **Notes:** <decisions, follow-ups, or links to the originating PLAN/TRACKER item>.

## Deferred / DEBT

<!-- Work consciously NOT done. Each item states WHY it was deferred and the TRIGGER that should bring it back. An empty section is the correct state for a clean template. -->

_None._

<!-- Template — replace example entries with real ones. Author: Phillip Anderson | Integrate-IT Australia. -->

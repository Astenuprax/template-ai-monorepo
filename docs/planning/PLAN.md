---
id: PLAN-TEMPLATE
type: REFERENCE
status: EXPERIMENTAL
gist: Tier-0 planning scaffold for template-ai-monorepo work — copy, rename, and fill before starting a unit of work.
---

# Plan: <title>

<!--
Tier-0 plan template. Copy this file to docs/planning/<slug>-PLAN.md, set the
frontmatter `id`/`gist`, and replace `<title>`. Keep it terse — one plan per
unit of work. Structure, hygiene, and authoring conventions are governed by the
repo-structure-standard, repo-hygiene, and governance-standards documents; do
not restate their bodies here.
-->

## Context

<!--
Why this work exists. State the current behaviour, the gap or trigger, and the
constraints that bound the solution (target packages such as platform-core or
example-mcp-server, Python 3.12+, uv workspace, the ruff + pyright(strict) +
pytest quality gate). Link issues or prior plans rather than duplicating them.
-->

## Goals

<!--
The observable outcomes that define "done". One bullet per goal, each
verifiable. Include explicit non-goals to fence scope. Avoid implementation
detail here — that belongs under Approach.
-->

## Approach

<!--
How the goals will be met. Name the modules, agents, MCP tools, and transports
touched (e.g. governance-audit agent reaching a tool via example-mcp-server over
stdio). Note key decisions and the alternatives rejected. Keep it at design
altitude, not line-by-line.
-->

## Milestones

<!--
Ordered, independently shippable steps. Each milestone is a checkable box with a
clear completion criterion. Prefer small increments that keep the quality gate
green at every step.

- [ ] <milestone> — done when <criterion>
-->

## Verification

<!--
How completion is proven. List the commands that must pass (uv sync
--all-packages, uv run governance-agent ., ruff, pyright, pytest including the
tests/test_structure.py structure-lint gate, pre-commit) and any manual checks.
Tie each Goal to the evidence that confirms it.
-->

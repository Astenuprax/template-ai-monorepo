# Contributing

Thanks for your interest in `template-ai-monorepo`. This document covers local
setup, the quality gate, commit and pull-request conventions, and licensing.

This repository follows the `repo-structure-standard`, `repo-hygiene`, and
`governance-standards` conventions. Familiarity with those standards is assumed;
contributions are reviewed against them.

## Development setup

Requires Python 3.12+ and [uv](https://docs.astral.sh/uv/).

```bash
git clone <repo-url>
cd template-ai-monorepo
uv sync --all-packages
uvx pre-commit install
```

`uv sync --all-packages` resolves and installs every workspace member
(including `platform-core` and `example-mcp-server`) into a single virtual
environment. `uvx pre-commit install` registers the local hooks so the gate runs
on each commit.

## Running the gate locally

The quality gate is ruff (lint + format), pyright in strict mode, the
structure-lint check at `tests/test_structure.py`, and pytest. Run it before
pushing:

```bash
uvx pre-commit run --all-files
uv run pytest -m "not integration"
```

`uvx pre-commit run --all-files` executes every hook in
`.pre-commit-config.yaml` across the whole tree. The `-m "not integration"`
selector skips tests that require external processes (such as a live
`example-mcp-server` over stdio); CI runs the integration suite separately.

You can run the agent example end-to-end with:

```bash
uv run governance-agent .
```

## Commit style

Commits follow [Conventional Commits](https://www.conventionalcommits.org/).
Use a type prefix and an imperative, present-tense summary:

```
feat(platform-core): add governance-audit retry policy
fix(example-mcp-server): handle empty stdio frame
docs: clarify gate invocation
```

Common types: `feat`, `fix`, `docs`, `refactor`, `test`, `chore`, `ci`. Scope
the change to the affected package or service where it helps reviewers.

## Pull request process

1. Branch from the default branch; do not push directly to it.
2. Make your change and keep it focused on a single concern.
3. Get the gate green locally (`uvx pre-commit run --all-files` and
   `uv run pytest -m "not integration"`).
4. Open the pull request and fill out the PR template completely.
5. CI must pass on the pull request before review and merge — CI also runs the
   integration suite. Address review feedback with follow-up commits.

## Code of conduct

Participation in this project is governed by [CODE_OF_CONDUCT.md](CODE_OF_CONDUCT.md).
By contributing, you agree to uphold it.

## Licensing

This project is licensed under the Apache License 2.0; see [LICENSE](LICENSE) for
the full text and [NOTICE](NOTICE) for attribution. By submitting a contribution,
you agree that it is licensed under Apache-2.0 under the terms in Section 5 of
the license (inbound = outbound), and that you have the right to submit it.

Maintained by Phillip Anderson | Integrate-IT Australia.

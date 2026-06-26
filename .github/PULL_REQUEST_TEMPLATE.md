# Pull Request

## Summary

<!-- What does this change do, and why? Keep it to a few clinical sentences. -->

## Type of change

<!-- Tick all that apply. -->

- [ ] Bug fix (non-breaking change that resolves an issue)
- [ ] New feature (non-breaking change that adds capability)
- [ ] Breaking change (fix or feature that alters existing behaviour or contracts)
- [ ] Refactor (no functional change)
- [ ] Documentation only
- [ ] Tooling / CI / build (uv workspace, pre-commit, quality gate)

## Checklist

- [ ] The quality gate passes locally via `pre-commit run --all-files` (ruff + pyright strict + pytest)
- [ ] `uv run pytest` passes, including the structure-lint gate at `tests/test_structure.py`
- [ ] Tests added or updated to cover the change
- [ ] Documentation updated where behaviour, interfaces, or usage changed
- [ ] Layout and hygiene conform to the `repo-structure-standard`, `repo-hygiene`, and `governance-standards`
- [ ] No AI-provenance text anywhere in the diff (commits, code, comments, docs)

## Related issues

<!-- e.g. Closes #123, Relates to #456. -->

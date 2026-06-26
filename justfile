# template-ai-monorepo task runner (casey/just)
# Author: Phillip Anderson | Integrate-IT Australia
#
# Conventions follow repo-structure-standard, repo-hygiene, and governance-standards.
# Quality gate = ruff + pyright(strict) + pytest, mirrored by .pre-commit-config.yaml.
# Run `just` (no args) to list every recipe.

set shell := ["bash", "-cu"]

# List available recipes
default:
    @just --list

# Resolve and install the full uv workspace
sync:
    uv sync --all-packages

# Lint with ruff
lint:
    uv run ruff check .

# Format with ruff
fmt:
    uv run ruff format .

# Static type-check with pyright (strict mode set in pyproject.toml)
types:
    uv run pyright

# Run the unit suite (excludes integration-marked tests)
test:
    uv run pytest -m "not integration"

# Run every test, including integration-marked tests
test-all:
    uv run pytest

# Run the full pre-commit gate across all files
gate:
    uvx pre-commit run --all-files

# Launch the governance-audit agent against the current directory
run:
    uv run governance-agent .

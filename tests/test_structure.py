"""Structure-lint gate (G1) — the AI-monorepo archetype, encoded as executable tests.

This file is the *executable form of the structure standard* for a uv-workspace AI/agentic
monorepo. Each test FAILS on a real drift class (a stray ``.py``/``.md``, a member missing
``py.typed``, an unpinned Action, off-vocabulary doc frontmatter) rather than merely checking
presence — per the repo-hygiene Form-vs-Substance principle, a gate that asserts existence is
gameable. (A full file-TYPE placement allowlist beyond ``.py``/``.md`` is Phase-2 scope.)

``CONFORMS_TO_STRUCTURE_VERSION`` is the marker this repo advertises as the standard version
it satisfies; ``test_version_marker_matches_declaration`` ties it to the authoritative
``[tool.structure_lint].version`` in the root ``pyproject.toml`` so neither can drift silently.
"""

from __future__ import annotations

import re
import tomllib
from pathlib import Path

import pytest

# Bump in lockstep with [tool.structure_lint].version in the root pyproject.toml when the
# archetype rules below change (dec.16). The two are cross-asserted, so a forgotten bump fails.
CONFORMS_TO_STRUCTURE_VERSION = 1

REPO_ROOT = Path(__file__).resolve().parents[1]

# Root furniture every repo of this archetype must carry (the standard's required surface).
ROOT_REQUIRED: tuple[str, ...] = (
    "README.md",
    "LICENSE",
    "NOTICE",
    "CHANGELOG.md",
    "CODE_OF_CONDUCT.md",
    "CONTRIBUTING.md",
    "SECURITY.md",
    "AGENTS.md",
    "CLAUDE.md",
    "pyproject.toml",
    "uv.lock",
    ".gitignore",
    ".editorconfig",
    ".pre-commit-config.yaml",
    ".python-version",
)

# Markdown allowed at the repo ROOT (everything else markdown must live under docs/).
ROOT_MD_ALLOWLIST: frozenset[str] = frozenset(
    {
        "README.md",
        "CHANGELOG.md",
        "CODE_OF_CONDUCT.md",
        "CONTRIBUTING.md",
        "SECURITY.md",
        "AGENTS.md",
        "CLAUDE.md",
    }
)

# Frontmatter contract for docs/ knowledge artefacts (governance-standards §3 L2 header).
FRONTMATTER_TYPES: frozenset[str] = frozenset({"SKILL", "WORKFLOW", "LESSON", "ADR", "REFERENCE"})
FRONTMATTER_STATUS: frozenset[str] = frozenset({"EXPERIMENTAL", "VERIFIED", "DEPRECATED"})

# Directories that legitimately hold Python source (file-placement allowlist).
_PY_SOURCE_ROOTS = ("packages", "services", "tests")

# A SHA-pinned Action ref ends in a 40-char hex commit (supply-chain mandate, dec.10).
# `uses:` is matched ANYWHERE on the line (not just line-leading) so a flow-style
# `[{ uses: x@tag }]` step cannot evade the pin check.
_SHA_PIN = re.compile(r"@[0-9a-f]{40}$")
_DIGEST_PIN = re.compile(r"@sha256:[0-9a-f]{64}$")  # docker:// actions pin by image digest
_USES_REF = re.compile(r"\buses:\s*(?P<ref>[^\s#]+)")

# Genuine noise skipped at ANY depth; build outputs skipped only at repo ROOT (a nested
# `packages/x/build/` is NOT a free hiding place for stray files — red-team MED).
_NOISE_DIRS = {
    ".git",
    ".venv",
    "venv",
    "__pycache__",
    ".ruff_cache",
    ".pytest_cache",
    ".mypy_cache",
}
_ROOT_ONLY_SKIP = {"build", "dist"}


def _tracked_and_present(rel: str) -> bool:
    return (REPO_ROOT / rel).exists()


def _iter_repo_files(suffix: str) -> list[Path]:
    """All files with ``suffix`` under the repo, skipping only genuine noise."""
    out: list[Path] = []
    for p in REPO_ROOT.rglob(f"*{suffix}"):
        parts = p.relative_to(REPO_ROOT).parts
        if any(part in _NOISE_DIRS for part in parts):
            continue
        if parts and parts[0] in _ROOT_ONLY_SKIP:
            continue
        out.append(p)
    return out


def _member_globs() -> list[str]:
    """The workspace member globs as actually declared in pyproject (not hardcoded)."""
    data = tomllib.loads((REPO_ROOT / "pyproject.toml").read_text(encoding="utf-8"))
    globs = data.get("tool", {}).get("uv", {}).get("workspace", {}).get("members", [])
    return [str(g) for g in globs]


def _workspace_members() -> list[Path]:
    """Resolve every directory matched by the declared member globs (deduped)."""
    seen: dict[Path, None] = {}
    for glob in _member_globs():
        for match in sorted(REPO_ROOT.glob(glob)):
            if match.is_dir():
                seen.setdefault(match.resolve(), None)
    return list(seen)


def _read_frontmatter(md: Path) -> dict[str, str] | None:
    text = md.read_text(encoding="utf-8")
    if not text.startswith("---"):
        return None
    end = text.find("\n---", 3)
    if end == -1:
        return None
    block = text[3:end].strip().splitlines()
    fm: dict[str, str] = {}
    for line in block:
        if ":" in line:
            key, _, val = line.partition(":")
            fm[key.strip()] = val.strip().strip("'\"")
    return fm


# --- Version marker ------------------------------------------------------------------


def test_version_marker_matches_declaration() -> None:
    """The in-test marker and the authoritative pyproject declaration must agree.

    Scope (honest): this catches bumping one integer and forgetting the other. It does NOT
    enforce "rules changed => version bumped" — that linkage is still discipline (a content
    hash over the rule set is Phase-2 scope).
    """
    data = tomllib.loads((REPO_ROOT / "pyproject.toml").read_text(encoding="utf-8"))
    declared = data.get("tool", {}).get("structure_lint", {}).get("version")
    assert isinstance(CONFORMS_TO_STRUCTURE_VERSION, int) and CONFORMS_TO_STRUCTURE_VERSION > 0
    assert declared == CONFORMS_TO_STRUCTURE_VERSION, (
        f"[tool.structure_lint].version={declared!r} != "
        f"CONFORMS_TO_STRUCTURE_VERSION={CONFORMS_TO_STRUCTURE_VERSION!r} — bump both together."
    )


# --- Root furniture ------------------------------------------------------------------


@pytest.mark.parametrize("name", ROOT_REQUIRED)
def test_required_root_file_present(name: str) -> None:
    assert _tracked_and_present(name), f"required root entry missing (drift): {name}"


def test_license_is_unmodified_apache() -> None:
    """LICENSE is verbatim Apache-2.0 boilerplate — attribution belongs in NOTICE, not here."""
    text = (REPO_ROOT / "LICENSE").read_text(encoding="utf-8")
    assert "Apache License" in text and "Version 2.0" in text
    assert "Phillip Anderson" not in text and "Integrate-IT" not in text, (
        "no copyright/identity line may be edited into the verbatim LICENSE body"
    )


# --- File placement ------------------------------------------------------------------


def test_no_stray_python_at_root() -> None:
    strays = [p.name for p in REPO_ROOT.glob("*.py")]
    assert not strays, f"Python files must live under {_PY_SOURCE_ROOTS}, not repo root: {strays}"


def test_python_sources_only_in_allowed_roots() -> None:
    offenders = [
        str(p.relative_to(REPO_ROOT))
        for p in _iter_repo_files(".py")
        if p.relative_to(REPO_ROOT).parts[0] not in _PY_SOURCE_ROOTS
    ]
    assert not offenders, f".py outside {_PY_SOURCE_ROOTS}: {offenders}"


# --- Workspace member integrity ------------------------------------------------------


_ALLOWED_MEMBER_ROOTS = ("packages", "services")


def test_every_member_has_typed_src_package() -> None:
    """Each declared workspace member is an installable, *typed* src-layout package.

    Members are resolved from the actual ``[tool.uv.workspace].members`` globs (not hardcoded
    roots), so a member smuggled in under an unexpected glob is still integrity-checked and is
    flagged if it sits outside the allowed top-level roots.
    """
    problems: list[str] = []
    pkg_names: dict[str, str] = {}
    for member in _workspace_members():
        rel = member.relative_to(REPO_ROOT)
        if rel.parts[0] not in _ALLOWED_MEMBER_ROOTS:
            problems.append(f"{rel}: member outside allowed roots {_ALLOWED_MEMBER_ROOTS}")
        if not (member / "pyproject.toml").is_file():
            problems.append(f"{rel}: missing pyproject.toml")
            continue
        src = member / "src"
        pkgs = (
            [d for d in src.iterdir() if d.is_dir() and (d / "__init__.py").is_file()]
            if src.is_dir()
            else []
        )
        if not pkgs:
            problems.append(f"{rel}: no src/<package>/__init__.py (not a src-layout package)")
            continue
        for pkg in pkgs:
            if not (pkg / "py.typed").is_file():
                problems.append(f"{rel}: {pkg.name} ships no py.typed (untyped distribution)")
            if pkg.name in pkg_names:
                problems.append(
                    f"{rel}: import package {pkg.name!r} collides with {pkg_names[pkg.name]}"
                )
            else:
                pkg_names[pkg.name] = str(rel)
    assert not problems, "workspace member drift:\n  " + "\n  ".join(problems)


def test_every_service_ships_a_dockerfile() -> None:
    """Containerisation mandate: every service we build is delivered as a container."""
    base = REPO_ROOT / "services"
    missing = (
        [
            str(d.relative_to(REPO_ROOT))
            for d in base.iterdir()
            if d.is_dir() and not (d / "Dockerfile").is_file()
        ]
        if base.is_dir()
        else []
    )
    assert not missing, f"services missing a Dockerfile (containerisation mandate): {missing}"


# --- Markdown / docs -----------------------------------------------------------------


def test_markdown_only_at_root_allowlist_or_under_docs() -> None:
    offenders: list[str] = []
    for md in _iter_repo_files(".md"):
        rel = md.relative_to(REPO_ROOT)
        parts = rel.parts
        if len(parts) == 1:
            if rel.name not in ROOT_MD_ALLOWLIST:
                offenders.append(str(rel))
        elif parts[0] not in {"docs", ".github"}:
            offenders.append(str(rel))
    assert not offenders, f"markdown outside root-allowlist / docs / .github: {offenders}"


def test_docs_knowledge_artefacts_have_enum_valid_frontmatter() -> None:
    docs = REPO_ROOT / "docs"
    if not docs.is_dir():
        pytest.skip("no docs/ yet")
    problems: list[str] = []
    for md in docs.rglob("*.md"):
        if md.name.upper() == "README.MD":
            continue
        fm = _read_frontmatter(md)
        rel = md.relative_to(REPO_ROOT)
        if fm is None:
            problems.append(f"{rel}: no YAML frontmatter")
            continue
        for key in ("id", "gist"):  # L2 header mandates these alongside type/status
            if not fm.get(key):
                problems.append(f"{rel}: missing required frontmatter key {key!r}")
        if fm.get("type") not in FRONTMATTER_TYPES:
            problems.append(f"{rel}: type={fm.get('type')!r} not in {sorted(FRONTMATTER_TYPES)}")
        if fm.get("status") not in FRONTMATTER_STATUS:
            problems.append(
                f"{rel}: status={fm.get('status')!r} not in {sorted(FRONTMATTER_STATUS)}"
            )
        if fm.get("type") == "ADR" and rel.parts[:2] != ("docs", "adr"):
            problems.append(f"{rel}: ADR-typed doc must live under docs/adr/")
    assert not problems, "docs frontmatter drift:\n  " + "\n  ".join(problems)


# --- Tests tree ----------------------------------------------------------------------


def test_tests_tree_holds_only_tests_and_support() -> None:
    """tests/ contains test modules + conftest/fixtures only — no production code parked here."""
    tests = REPO_ROOT / "tests"
    offenders: list[str] = []
    for p in tests.rglob("*.py"):
        rel = p.relative_to(tests)
        if any(part in {"__pycache__", "fixtures"} for part in rel.parts):
            continue
        if p.name == "conftest.py" or p.name.startswith("test_"):
            continue
        offenders.append(str(rel))
    assert not offenders, f"non-test .py under tests/ (move to a package): {offenders}"


# --- CI / supply chain ---------------------------------------------------------------


def test_ci_workflow_present() -> None:
    ci = REPO_ROOT / ".github" / "workflows" / "ci.yml"
    assert ci.is_file(), "missing .github/workflows/ci.yml"


def test_all_workflow_actions_are_sha_pinned() -> None:
    """Every `uses:` external Action must be pinned to a 40-hex commit SHA (supply chain)."""
    wf_dir = REPO_ROOT / ".github" / "workflows"
    if not wf_dir.is_dir():
        pytest.skip("no workflows yet")
    unpinned: list[str] = []
    for wf in sorted(wf_dir.glob("*.yml")) + sorted(wf_dir.glob("*.yaml")):
        for line in wf.read_text(encoding="utf-8").splitlines():
            for m in _USES_REF.finditer(line):
                ref = m.group("ref").strip("\"'")
                if ref.startswith("./"):
                    continue  # local composite action — no external ref to pin
                if ref.startswith("docker://"):
                    # container actions ARE pinnable — by image digest, not a floating tag.
                    if not _DIGEST_PIN.search(ref):
                        unpinned.append(f"{wf.name}: {ref} (docker:// needs @sha256:<digest>)")
                    continue
                if not _SHA_PIN.search(ref):
                    unpinned.append(f"{wf.name}: {ref}")
    assert not unpinned, "Actions not SHA-pinned:\n  " + "\n  ".join(unpinned)

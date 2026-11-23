"""The agent's governance-audit tool.

A generic, self-demonstrating governance-assurance check: audit a directory
against a minimal structure standard and report drift (required entries that
are missing). No client/vendor coupling — the "standard" is just a tuple of
required entry names, so the same logic dogfoods the repo-structure-conformance
theme without embedding any private rule set.
"""

from pathlib import Path

from pydantic import BaseModel, Field

#: The minimal structure standard this demonstrator audits against.
DEFAULT_REQUIRED: tuple[str, ...] = ("README.md", "pyproject.toml", "LICENSE")


class AuditReport(BaseModel):
    """Structured result of a structure audit (typed output — showcases type rigor)."""

    target: str = Field(description="The audited directory path.")
    conforms: bool = Field(description="True when no required entry is missing.")
    present: list[str] = Field(default_factory=list, description="Required entries that exist.")
    missing: list[str] = Field(
        default_factory=list, description="Required entries missing (drift)."
    )


def audit_structure(
    path: str,
    required: tuple[str, ...] = DEFAULT_REQUIRED,
    *,
    allowed_root: Path | None = None,
) -> AuditReport:
    """Audit ``path`` against ``required`` and report which entries are missing.

    Validates that ``path`` is an existing directory and, when ``allowed_root``
    is supplied (enforced at the MCP boundary via ``Path.cwd()``), confines
    inspection inside that root.
    """
    base = Path(path).resolve(strict=False)
    if allowed_root is not None:
        root = allowed_root.resolve(strict=False)
        if not base.is_relative_to(root):
            raise ValueError(f"Target path {path!r} escapes allowed root {str(root)!r}")
    if not base.is_dir():
        raise ValueError(f"Target path {path!r} is not an existing directory")
    present = [name for name in required if (base / name).exists()]
    missing = [name for name in required if name not in present]
    return AuditReport(
        target=str(base),
        conforms=not missing,
        present=present,
        missing=missing,
    )

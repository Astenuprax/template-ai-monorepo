"""Golden eval — the audit tool against a table of repos with known-correct verdicts.

A lightweight, hermetic eval: each case pins the *exact* expected drift so a regression in
the audit logic (wrong conforms flag, miscounted missing) fails loudly against ground truth.
"""

from __future__ import annotations

from collections.abc import Callable, Iterable
from pathlib import Path

import pytest
from pydantic_ai import Agent, ModelMessage, ModelResponse, ToolCallPart
from pydantic_ai.models.function import AgentInfo, FunctionModel
from pydantic_ai.toolsets import FunctionToolset

from platform_core.tools import AuditReport, audit_structure

MakeRepo = Callable[[Iterable[str]], Path]  # mirrors the make_repo fixture in conftest.py

# (seeded entries, expected conforms, expected sorted-missing)
CASES = [
    pytest.param(["README.md", "pyproject.toml", "LICENSE"], True, [], id="full"),
    pytest.param(["README.md", "pyproject.toml"], False, ["LICENSE"], id="no-license"),
    pytest.param(["README.md"], False, ["LICENSE", "pyproject.toml"], id="readme-only"),
    pytest.param([], False, ["LICENSE", "README.md", "pyproject.toml"], id="empty"),
]


@pytest.mark.parametrize(("entries", "conforms", "missing"), CASES)
def test_audit_matches_golden(
    make_repo: MakeRepo, entries: list[str], conforms: bool, missing: list[str]
) -> None:
    report = audit_structure(str(make_repo(entries)))
    assert report.conforms is conforms
    assert sorted(report.missing) == missing


def test_agent_eval_calls_confined_tool_and_returns_audit_report(
    make_repo: MakeRepo, monkeypatch: pytest.MonkeyPatch
) -> None:
    repo = make_repo(["README.md", "pyproject.toml"])
    monkeypatch.chdir(repo.parent)

    def audit_structure_tool(path: str) -> AuditReport:
        return audit_structure(path, allowed_root=Path.cwd())

    observed_schemas: list[set[str]] = []

    def decide(messages: list[ModelMessage], info: AgentInfo) -> ModelResponse:
        if len(messages) == 1:
            assert info.function_tools
            tool_def = info.function_tools[0]
            props = tool_def.parameters_json_schema.get("properties", {})
            observed_schemas.append(set(props))
            return ModelResponse(
                parts=[ToolCallPart(tool_name="audit_structure_tool", args={"path": repo.name})]
            )
        tool_result = messages[-1].parts[0]
        content = getattr(tool_result, "content", {})
        payload = content.model_dump() if isinstance(content, AuditReport) else content
        return ModelResponse(
            parts=[
                ToolCallPart(
                    tool_name=info.output_tools[0].name,
                    args=payload,
                )
            ]
        )

    agent: Agent[None, AuditReport] = Agent(
        FunctionModel(decide),
        output_type=AuditReport,
        toolsets=[FunctionToolset([audit_structure_tool])],
    )
    result = agent.run_sync(f"Audit {repo.name}")
    assert observed_schemas == [{"path"}]
    assert result.output.conforms is False
    assert result.output.missing == ["LICENSE"]

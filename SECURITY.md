# Security Policy

## Reporting a vulnerability

Report security vulnerabilities privately by email to
**panderson@integrate-it.com.au**. Do not open a public issue, pull request, or
discussion for a suspected vulnerability — public disclosure before a fix is
available puts downstream users at risk.

Include enough detail to reproduce: affected package (`platform-core` or the
`example-mcp-server` service), version or commit, environment, and a minimal
proof of concept. You will receive an acknowledgement of your report. Valid
reports are triaged, and a remediation or mitigation is published before the
issue is disclosed.

## Supported versions

Security fixes are applied only to the latest tagged release. Older tags are not
patched; upgrade to the current release to receive fixes.

| Version            | Supported          |
| ------------------ | ------------------ |
| Latest tagged release | Yes             |
| Older releases     | No                 |

## Scope

This repository is an open-source template. It ships an illustrative
"governance-audit" agent and example MCP server, not a production service.
Downstream users are expected to fork and adapt it: replace the example agent
and tooling, set their own contact address in this file, and apply their own
review and governance controls (see the `repo-structure-standard`,
`repo-hygiene`, and `governance-standards` policies referenced by this
template).

Reports against this repository should concern the template's own code,
dependency pins, and quality-gate configuration (ruff, pyright, pytest, the
`tests/test_structure.py` structure-lint gate, and `.pre-commit-config.yaml`).
Vulnerabilities introduced by downstream adaptations are the responsibility of
the adopting project.

---

Maintainer: Phillip Anderson | Integrate-IT Australia

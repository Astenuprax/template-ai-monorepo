---
id: REF-SPIKE-COPIER-001
type: REFERENCE
status: EXPERIMENTAL
gist: Decision-grade feasibility spike for splitting template-ai-monorepo into a Copier governance base + per-stack overlays — partition map, config-hoist, tool choice, MCP architecture, taxonomy, realization strategy, and empirical dry-run results.
---

# Spike — Copier Base+Overlay Partition (template-ai-monorepo)

Read-only feasibility analysis (plus a throwaway sandboxed Copier render) for evolving this
repo into a **template family**: a stack-agnostic governance **base** + composable per-stack
overlays, authored once and propagated via Copier. The spike **changes no repository or standards
files** beyond this report and its companion ADR. Every standards edit and the repo split itself
are explicitly **post-spike, separately-signed** work. Conventions follow `repo-structure-standard`,
`repo-hygiene`, and `governance-standards`, cited by name (not restated).

## 1. Summary / Recommendation

**Verdict: GO to the build phase** — the partition is feasible, the riskiest mechanics are
empirically pinned, and Copier's footprint is bounded to the layer that needs it. The decision-gate
axes, each with confidence and reversibility cost:

| # | Gate | Recommendation | Confidence | Reversibility |
|---|------|----------------|-----------|---------------|
| G1 | Partition or not | **Partition** — base + python-stack + mcp-capability; 59 files cleanly assigned, no `TBD` | High | n/a (this is the decision) |
| G2 | Tool | **Copier** (vs cruft) — multi-overlay independent update **empirically confirmed** | High | Low (cruft migration possible but unneeded) |
| G3 | Per-stack realization (R-A) | **Materialized for base + Python; declarative `*-structure-repo.md` contract for un-built stacks** | High | High (contract→tree is additive) |
| G4 | MCP architecture (WS-4) | **B — separate optional `mcp-capability` overlay** | Med-High | B→A cheap; A→B expensive (decides direction) |
| G5 | This-repo link-back (R-B / WS-11) | **`.copier-answers.base.yml` link** (extract a copy, pull governance via `copier update`) | High | High (de-link = delete one file) |
| G6 | Planning taxonomy (WS-0) | **R2 — ratify `docs/planning/` as the archetype canonical; amend the standard, not the repo** | Med-High | High (additive standard edit) |
| G7 | Structure-version | **Single base-owned integer**; composite per-overlay versioning deferred to the register | High | High |

**Two HIGH-severity silent-failure couplings** must be resolved at build time (both fail green
today): the `end-session` tracker-path probe miss (WS-6 #1) and the version-marker ownership
crossing the base↔python seam (WS-6 #2).

## 2. Context / Givens

- This repo (`template-ai-monorepo`) is the v1 reference impl named in `repo-structure-standard.md`.
  59 tracked files; uv virtual workspace (`members = ["packages/*","services/*"]`); quality gate =
  ruff + pyright(strict) + pytest, with the structure-lint at `tests/test_structure.py` cross-asserted
  to `pyproject.toml [tool.structure_lint].version = 1`.
- **Operator decisions folded into this spike (2026-06-30):**
  - **R-A** — realization is per-stack and governed by reference-impl-first: base + Python materialized;
    un-built stacks (PowerShell/M365/projects/generic) are declarative contracts, **not** speculative trees.
  - **R-B** — extract a **copy** of governance into a new `template-governance-base` (do not move/delete
    it from this repo, which stays a working, governed reference impl).
- **Locked prior (2026-06-27):** base + per-stack overlays via Copier; new repos first, retrofit opt-in;
  lazy touch-time `copier update`; `template-*` repos vs verb-based `scaffold-*` workflows.

## 3. Partition Map (WS-1)

Authoritative file set: `git ls-files` = **59 tracked files** at spike time (exhaustive against the live
tree). The count **excludes this spike's own two meta-docs** (`docs/planning/spike-copier-partition.md`,
`docs/adr/0004-*.md`) — committing them makes the tree 61, both **user-data-class** by the `docs/planning/*`
and `docs/adr/≥0004` rules below (no explicit row needed; class-covered). Layer key: **base**
(template-governance-base), **python-stack**, **mcp-capability**, **user-data**; `+` = genuine split-ownership.

| File | Layer | Mutation-class | Rename-risk | Shared-iface | Note |
|---|---|---|---|---|---|
| `.devcontainer/devcontainer.json` | base + python-stack | re-render | low | no | Base mandates presence; python-stack owns the uv/Python image + features content. |
| `.dockerignore` | base | re-render | low | no | Generic ignore, tuned for the Python build context. |
| `.editorconfig` | base | re-render | low | no | Universal editor defaults. |
| `.env.example` | user-data | skip_if_exists | low | no | Sample env the user copies to `.env` and fills; never clobber. |
| `.github/ISSUE_TEMPLATE/bug_report.md` | base | re-render | low | no | OSS furniture. |
| `.github/ISSUE_TEMPLATE/config.yml` | base | re-render | low | no | OSS furniture. |
| `.github/ISSUE_TEMPLATE/feature_request.md` | base | re-render | low | no | OSS furniture. |
| `.github/PULL_REQUEST_TEMPLATE.md` | base | re-render | low | no | OSS furniture. |
| `.github/dependabot.yml` | base + python-stack | re-render | low | no | Base owns presence; python-stack owns the pip/uv ecosystem entries (github-actions ecosystem is base). |
| `.github/workflows/ci.yml` | base + python-stack | re-render | low | **yes** | Triple-seam: base owns presence/skeleton, python-stack owns uv/ruff/pyright/pytest + MCP-roundtrip steps. **MUST be `{% raw %}`-guarded** (empirical: bare `${{ }}` → jinja `UndefinedError`). Mirrors the pre-commit gate. |
| `.github/workflows/release.yml` | base + python-stack | re-render | low | **yes** | Base presence; python-stack owns build/SBOM/sign/provenance. `{% raw %}`-guarded. |
| `.github/workflows/scorecard.yml` | base | re-render | low | no | Supply-chain furniture. `{% raw %}`-guarded. |
| `.gitignore` | base + python-stack | re-render | low | no | Base presence; python-stack content (`.venv`, `__pycache__`, etc.). |
| `.pre-commit-config.yaml` | base + python-stack | re-render | low | **yes** | MIXED hooks: base-generic (whitespace/eof/check-yaml/toml/merge-conflict/large-files/gitleaks) + python-stack (ruff, ruff-format, local pyright + structure-lint). References `tests/test_structure.py`; mirrors `ci.yml`. |
| `.python-version` | python-stack | re-render | low | no | Pins the interpreter for the Python overlay. |
| `AGENTS.md` | base + python-stack + mcp-capability | re-render | low | **yes** | Composed canonical guide: base header + governance-by-name; python-stack + mcp supply the architecture body; a delimited trailing project-notes region is `skip_if_exists`. `CLAUDE.md` points here. |
| `CHANGELOG.md` | user-data | skip_if_exists | low | no | Project history; never clobber. |
| `CLAUDE.md` | base | re-render | low | **yes** | Thin templated pointer to `AGENTS.md`; project additions go in a `skip_if_exists` region. References the gate + `test_structure.py`. |
| `CODE_OF_CONDUCT.md` | base | re-render | low | no | Standard CoC; contact is a templated variable. |
| `CONTRIBUTING.md` | base | re-render | low | no | Furniture; references the gate by name. |
| `LICENSE` | base | **re-render** | low | no | Verbatim Apache-2.0. MUST re-render — **NOT** `skip_if_exists`: a stale or user-edited licence must be corrected, and there is no user data to preserve. |
| `NOTICE` | user-data | skip_if_exists | low | no | Copyright holder/year + attribution accretes; user owns. |
| `README.md` | user-data | skip_if_exists | low | no | Renders on GitHub; project front-door, user owns. |
| `SECURITY.md` | base | re-render | low | no | Policy furniture; contact is a templated variable. |
| `configs/mcp-config.template.json` | mcp-capability | re-render | med | **yes** | The client↔server launch contract (command/args/path to the service). Template-owned pattern; a service rename drifts the referenced path. |
| `docs/ARCHITECTURE.md` | python-stack + mcp-capability | skip_if_exists | low | no | Seeds the worked-example architecture; user rewrites once their real system diverges. Carries `docs/` frontmatter. |
| `docs/adr/0001-uv-workspace.md` | python-stack | re-render | low | no | Archetype decision. Seeds 0001–0003 are template-reserved; project ADRs start 0004 as user-data (untouched). |
| `docs/adr/0002-mcp-client-server-libraries.md` | mcp-capability | re-render | low | no | Archetype MCP-library decision; template-owned seed. |
| `docs/adr/0003-supply-chain-pinning-scope.md` | base | re-render | low | no | Archetype supply-chain decision; template-owned seed. |
| `docs/folders-and-naming.md` | python-stack | re-render | low | no | Documents the archetype layout; tracks the structure standard. |
| `docs/planning/DONE.md` | user-data | skip_if_exists | low | no | Project planning state; user owns. |
| `docs/planning/PLAN.md` | user-data | skip_if_exists | low | no | Project planning state; user owns. |
| `docs/planning/README.md` | user-data | skip_if_exists | low | no | Planning-dir index; seeded once, user owns. |
| `docs/planning/TRACKER.md` | user-data | skip_if_exists | low | no | Project planning state; user owns. (Location reconciliation: WS-0/WS-6 #1.) |
| `docs/planning/DEBT.md` | user-data | skip_if_exists | low | no | The durable debt register; template seeds, project accretes; never clobber. (Renamed from `docs/registers/deferred-hardening.md` 2026-07-02 — retired filename, and relocated to the AI-monorepo `docs/planning/` carve-out.) |
| `justfile` | base + python-stack | re-render | low | no | Base mandates presence; python-stack owns the uv recipes. |
| `packages/platform-core/README.md` | python-stack | skip_if_exists | **high** | no | Member long-description; path carries the package name → rename orphans it. |
| `packages/platform-core/pyproject.toml` | python-stack | skip_if_exists | **high** | **yes** | Member manifest; its name is referenced by root `[tool.uv.sources]`; rename orphans the dir (copier won't delete). |
| `packages/platform-core/src/platform_core/__init__.py` | python-stack | skip_if_exists | **high** | no | Example barrel; a package-dir rename orphans the whole `src/` tree. |
| `packages/platform-core/src/platform_core/agent.py` | mcp-capability (see ‡) | skip_if_exists | **high** | **yes** | **‡ Wholly MCP-coupled, NOT region-splittable** — imports `MCPToolset`/`fastmcp` and launches `example_mcp_server` as a subprocess (verified L14/16/31/43/50). It cannot belong to python-stack as-is; a no-MCP python render must **author a de-MCP'd `agent.py` variant** (or `agent.py` is purely mcp-capability and the bare stack ships a different example). This is the concrete mechanism behind the §5 no-exemplar caveat — distinct from the *within-file region-splits* (`pyproject.toml`, `test_structure.py`). |
| `packages/platform-core/src/platform_core/py.typed` | python-stack | re-render | **high** | no | Required typing marker (structure-lint asserts presence); empty file; orphans on package rename. |
| `packages/platform-core/src/platform_core/settings.py` | python-stack | skip_if_exists | **high** | no | Example typed settings. |
| `packages/platform-core/src/platform_core/tools.py` | python-stack | skip_if_exists | **high** | no | Example audit tool. |
| `packages/platform-core/src/platform_core/tracing.py` | python-stack | skip_if_exists | **high** | no | Example OTel setup. |
| `pyproject.toml` | base + python-stack | re-render | med | **yes** | SPLIT (see §3.1): base owns presence + `[project]` + `[tool.uv.workspace] members`; python-stack owns `[tool.ruff]`/`[tool.pyright]`/`[tool.pytest]`/`[dependency-groups]`/`[tool.structure_lint]`. `[tool.uv.sources]` composed per active members. `structure_lint.version` must equal the `test_structure.py` marker. |
| `services/example-mcp-server/Dockerfile` | mcp-capability | re-render | **high** | **yes** | Template-owned container pattern; every service MUST ship one (structure-lint `test_every_service_ships_a_dockerfile`, unconditional). Orphans on service rename. |
| `services/example-mcp-server/README.md` | mcp-capability | skip_if_exists | med | no | Member README; path carries the service name. |
| `services/example-mcp-server/pyproject.toml` | mcp-capability | skip_if_exists | **high** | **yes** | Member manifest; referenced by root `[tool.uv.sources]`; rename orphans the dir. |
| `services/example-mcp-server/src/example_mcp_server/__init__.py` | mcp-capability | skip_if_exists | **high** | no | Example barrel; orphans on rename. |
| `services/example-mcp-server/src/example_mcp_server/py.typed` | mcp-capability | re-render | **high** | no | Required typing marker; empty; orphans on rename. |
| `services/example-mcp-server/src/example_mcp_server/server.py` | mcp-capability | skip_if_exists | **high** | **yes** | Implements the tool contract that `mcp-config.template.json`, `agent.py` and `test_mcp_roundtrip` all depend on. |
| `tests/conftest.py` | base + python-stack | re-render | low | no | Shared test-harness/fixtures wiring. |
| `tests/fixtures/.gitkeep` | base | re-render | low | no | Keeps the fixtures dir tracked. |
| `tests/integration/test_mcp_roundtrip.py` | mcp-capability | skip_if_exists | med | **yes** | Tests the example roundtrip; couples to the server's tool contract; user evolves it with their service. |
| `tests/test_structure.py` | base (harness) + python-stack/mcp (data) | re-render | med | **yes** | SPLIT (see §3.1): base owns the engine (test fns, pin regexes, frontmatter-enum machinery); overlays own the DATA (`ROOT_REQUIRED`, `_ALLOWED_MEMBER_ROOTS`, per-service-Dockerfile assertion, `CONFORMS_TO_STRUCTURE_VERSION`). THE contract enforcing every layer's shape; its marker must equal root `[tool.structure_lint]`. |
| `tests/unit/test_agent_build.py` | python-stack | skip_if_exists | med | no | Tests the example agent build; couples to `platform-core`. |
| `tests/unit/test_eval_audit.py` | python-stack | skip_if_exists | med | no | Deterministic golden eval of the example audit; couples to `platform-core`. |
| `tests/unit/test_tools.py` | python-stack | skip_if_exists | med | no | Tests example `tools.py`. |
| `uv.lock` | base + python-stack | **migration-gated** | low | **yes** | ONE resolved lock for the whole workspace; regenerated by a post-render `uv lock` (never hand-merged — see §6 WS-8). CI lock-freshness + OSV-Scanner gate depend on it. |

### 3.1 Contested seams resolved

- **`pyproject.toml` split** — base owns *presence + `[project]` schema + `[tool.uv.workspace] members` glob*
  (the workspace contract that exists regardless of stack); python-stack owns `[tool.ruff]`/`[tool.pyright]`/
  `[tool.pytest]`/`[dependency-groups]`/`[tool.structure_lint]`. `[tool.uv.sources]` is **overlay-composed**
  (one `{ workspace = true }` entry per active member), so it is migration-gated within an otherwise re-rendered file.
- **`tests/test_structure.py` (harness vs data)** — base owns the *harness* (test functions, the SHA/digest/`uses`
  pin regexes, the frontmatter-enum validators, the version-marker cross-check); overlays own the *data* the harness
  asserts against (`ROOT_REQUIRED`, `_ALLOWED_MEMBER_ROOTS`, the unconditional per-service-Dockerfile assertion, the
  `FRONTMATTER_TYPES/STATUS` enums, `CONFORMS_TO_STRUCTURE_VERSION`). Re-renders as one file with overlay-injected
  constants; it is the master shared interface.
- **`ci.yml` / `.pre-commit-config.yaml` / `justfile` / `devcontainer.json` (triple-seam)** — in all four, **base
  mandates presence only**; the **content is python-stack**. `.pre-commit-config.yaml` and `ci.yml` additionally carry
  base-generic content (whitespace/gitleaks hooks; checkout/setup boilerplate), so they are base+python-stack split.
  CI/release/scorecard YAML **must be `{% raw %}`-guarded** (empirically: copier 9.16.0 hard-fails on bare `${{ }}`).
- **`AGENTS.md` / `CLAUDE.md` (accreting user content)** — **position: templated-header + user-body**, NOT whole-file
  `skip_if_exists`. Governance-by-name section, gate pointers, conventions, and the overlay-composed architecture body
  are template-owned and **re-render** so corrections reach every instance; a single delimited "project notes" region
  is `skip_if_exists`. Whole-file skip is rejected — it would freeze the governance pointers and let them rot.
- **`LICENSE` (re-render, not skip)** — verbatim Apache-2.0, no user data; **re-render** so a drifted/edited licence is
  restored. `skip_if_exists` is the trap to avoid (it preserves a tampered licence).
- **user-data** (`README`/`CHANGELOG`/`NOTICE`/`.env.example`/`docs/planning/*`/`DEBT.md`) — all
  `skip_if_exists`. Example *code* members are also `skip_if_exists` seed the user evolves — with required scaffold
  markers (`py.typed`, the service `Dockerfile`) kept **re-render** because structure-lint asserts their presence. Every
  member-pathed file is **high rename-risk**: a package/service rename orphans `src/<name>/` (copier never deletes) and
  breaks the root `[tool.uv.sources]` reference — needs a rename-migration step.

## 4. Config-Hoist (WS-2)

### 4.1 Per-constant / per-symbol verdict

| Symbol (line) | Verdict | Owner | Reason |
|---|---|---|---|
| `CONFORMS_TO_STRUCTURE_VERSION` (25) | **HARNESS-INVARIANT** | base | Standard-version join; cross-asserted. Overlay-mutable would let a consumer self-certify any version. |
| `ROOT_REQUIRED` (30-46) | **HOISTABLE (floored)** | overlay extends base floor | Pure data. OSS-furniture subset = base floor; stack rows (`pyproject.toml`, `uv.lock`, `.pre-commit-config.yaml`, `.python-version`) = python-uv specifics. |
| `ROOT_MD_ALLOWLIST` (49-59) | **HARNESS-INVARIANT** | base | Governance OSS-furniture MD set (repo-hygiene §3), identical across stacks. |
| `FRONTMATTER_TYPES` (62) | **HARNESS-INVARIANT** | base | Governance vocabulary enum. |
| `FRONTMATTER_STATUS` (63) | **HARNESS-INVARIANT** | base | Governance vocabulary enum. |
| `_PY_SOURCE_ROOTS` (66) | **HOISTABLE** | overlay (python-stack) | Where `.py` may live; a non-Python stack differs entirely. |
| `_ALLOWED_MEMBER_ROOTS` (195) | **HOISTABLE** | overlay (python-stack) | uv-workspace-specific (`packages`/`services`). |
| `_SHA_PIN` / `_DIGEST_PIN` / `_USES_REF` (71-73) | **HARNESS-INVARIANT** | base | Assertion *logic* (regexes). A tunable pin grammar is the canonical gate-bypass. |
| `_NOISE_DIRS` (77-85) / `_ROOT_ONLY_SKIP` (86) | **HARNESS-INVARIANT** | base | Universal VCS/tooling noise; widening it is an attack surface. |
| every `test_*` assertion body | **HARNESS-INVARIANT** | base / python-stack | Assertion logic; consumes the hoisted data but the loops/asserts are fixed. `test_every_member_has_typed_src_package` + `test_declared_member_readme_resolves` live in the python-stack overlay's lint. |
| `test_every_service_ships_a_dockerfile` (235) | **HARNESS-INVARIANT (new-knob if relaxed)** | overlay (python-stack) | Unconditional containerisation Iron Law; vacuously passes with no `services/`, so needs no toggle. Making the mandate itself toggleable is a NEW knob — out of scope. |

### 4.2 Minimal `[tool.structure_lint]` schema (hoisted data only)

```toml
[tool.structure_lint]
version = 1                                      # base-owned marker; cross-asserted, NOT hoisted behaviour
root_required = [                                # overlay supplies; base floor enforced (below)
  "README.md", "LICENSE", "NOTICE", "CHANGELOG.md", "CODE_OF_CONDUCT.md",
  "CONTRIBUTING.md", "SECURITY.md", "AGENTS.md", "CLAUDE.md", ".gitignore",
  ".editorconfig",                              # ^ floor rows
  "pyproject.toml", "uv.lock", ".pre-commit-config.yaml", ".python-version",  # python-uv rows
]
py_source_roots = ["packages", "services", "tests"]   # overlay supplies
member_roots    = ["packages", "services"]            # overlay supplies
```

Only the three list literals move. Everything else (regexes, enums, MD allowlist, noise sets, every assertion body)
stays hardcoded in the base test module.

### 4.3 Base-enforced NON-OVERRIDABLE FLOOR (Form-vs-Substance)

The floor is **two-tier** — a base floor (stack-agnostic furniture) **plus a per-overlay floor** (the stack's own
non-negotiable rows). This two-tier shape is the fix for the review's MAJOR finding: a base-only floor would leave the
python-uv rows (`uv.lock`, `pyproject.toml`, …) — hard-enforced today — shrinkable by a consumer. Each tier asserts
membership + non-emptiness (not mere key presence):

```python
# --- base harness (template-governance-base) — stack-agnostic minimum ---
_ROOT_REQUIRED_FLOOR = frozenset({
    "README.md", "LICENSE", "NOTICE", "CHANGELOG.md", "CODE_OF_CONDUCT.md",
    "CONTRIBUTING.md", "SECURITY.md", "AGENTS.md", "CLAUDE.md", ".gitignore", ".editorconfig",
})

def test_base_floor_not_weakened() -> None:
    cfg = _load_structure_lint()
    assert frozenset(cfg["root_required"]) >= _ROOT_REQUIRED_FLOOR

# --- python-stack overlay — its OWN non-shrinkable rows (mirrors the base pattern) ---
_PY_ROOT_REQUIRED_FLOOR = frozenset({"pyproject.toml", "uv.lock", ".pre-commit-config.yaml", ".python-version"})
_PY_MEMBER_ROOTS_FLOOR  = frozenset({"packages", "services"})   # membership floor, not just non-empty

def test_python_stack_floor_not_weakened() -> None:
    cfg = _load_structure_lint()
    assert frozenset(cfg["root_required"]) >= _PY_ROOT_REQUIRED_FLOOR, "uv-workspace root files are non-negotiable"
    assert frozenset(cfg["member_roots"]) >= _PY_MEMBER_ROOTS_FLOOR
    assert "tests" in cfg["py_source_roots"]
```

An overlay that deletes `LICENSE` (base floor) or `uv.lock` (python floor) from its allowlist to dodge
`test_required_root_file_present` fails the matching floor test instead. The python floor lives **in the python-stack
overlay's lint**, so it travels with any python-stack consumer; shrinking it requires editing that overlay's lint
module — **diff-visible against the overlay template, not silently possible** (the same diff-visibility guarantee, not
literal impossibility, that §4.4 describes for the base floor).

### 4.4 Trade-off (stated explicitly)

Hoisting makes the lint **source its own expectations from a file inside the repo it lints** — a consumer could weaken
the gate by editing the same `pyproject.toml` the gate reads. That is a real reduction in test independence. The
**two-tier floor (§4.3) is what keeps it safe**: overlay-supplied sets are *extensions above* a hardcoded minimum that
includes both the base furniture AND the python-uv rows. A set cannot be shrunk past its floor without editing the
relevant lint module (base-out-of-reach for the base floor; visible in a diff against the python-stack overlay for the
python floor). **Honest scope of the floor:** it defends *shrinkage*; it does **not** make all upward-widening benign —
widening `py_source_roots` or `member_roots` *relaxes placement strictness* (where `.py` and members may live). That is
acceptable because those are **layout conventions, not security gates**, and the security-critical checks stay
base-hardcoded and HARNESS-INVARIANT regardless of config: the SHA/digest/`uses` pin regexes, `_NOISE_DIRS`,
`ROOT_MD_ALLOWLIST`, and `test_no_stray_python_at_root` (which hardcodes the root `*.py` ban, so widening
`py_source_roots` can never re-admit stray root Python). Net: configurability buys per-stack reuse; the floors buy back
shrink-safety; the hardcoded security gates are never config-reachable at all.

## 5. MCP Architecture (WS-4)

**Recommendation: B — base + python-stack overlay + optional `mcp-capability` overlay.**

- **A non-MCP python-stack consumer is realistic.** A uv virtual workspace exists for multi-member Python; an MCP server
  is one *kind* of service, not the reason the workspace exists. Under A, such a consumer deletes `example-mcp-server` —
  exactly the "removed template paths are NOT auto-deleted" footgun on a later `copier update`.
- **The MCP seam is cleanly separable and already exemplar'd.** `configs/mcp-config.template.json` +
  `services/example-mcp-server/**` + `tests/integration/test_mcp_roundtrip.py` are a self-contained capability codified
  *from a working exemplar that exists today* (reference-impl-first satisfied).
- **The `services/`+Dockerfile coupling lands on python-stack, not MCP.** `test_every_service_ships_a_dockerfile` is
  vacuous when `services/` is empty, so python-stack renders and passes its own gate with zero services; the MCP overlay
  then lands a concrete service. The seams compose without a base toggle.
- **Honest caveat (reference-impl-first):** in *this* repo there is no built bare-Python exemplar — `platform-core` is
  itself a pydantic-ai agent wiring an MCP *client*. So the python-stack-minus-MCP render path is **not yet validated by
  a materialized exemplar**. B is correct but the partition must not be declared "golden" until a no-MCP render is built
  and passes `pytest`/`pyright`/structure green. (The MCP-*server* is what becomes optional; `platform-core`'s
  agent-client wiring is AI-agent content that stays in the python/agent layer — the split must not strand it.)

**Reversibility (the deciding axis):** B→A (collapse) is cheap and unaffecting; A→B (split later) is expensive — copier
never removes the baked-in `example-mcp-server`, so every existing consumer needs a hand-migration. B is lower-regret and
preserves optionality. **"Done" gate (sharpened per review):** because `agent.py` is wholly MCP-coupled (§3 ‡), the no-MCP
render is **not** merely a subset of existing files — the python-stack overlay must **author a bare, non-MCP `agent.py`
variant** (or ship a different non-agent example), and *that* render must pass `pytest`/`pyright`(strict)/structure-lint
green before the partition is declared golden. Until that exists, B is the chosen direction but the no-MCP path is
unvalidated.

## 6. Tool (WS-3) + Dry-Run Results (empirical)

**Tool verdict: Copier** (vs cruft). Copier's per-overlay independent `copier update`, `_skip_if_exists`, 3-way merge,
and migration hooks are exactly the mechanics this partition needs, and the multi-overlay-independent-update claim is now
**empirically confirmed** (TEST 3 below) rather than documentation-only. Diff-based-rename limitation noted → the
high-rename-risk member files in §3 carry a rename-migration requirement.

Sandboxed render in scratch only (copier 9.16.0); discarded. Three claims tested:

- **TEST 1 — `${{ }}` ↔ Jinja collision (WS-10): PROVEN.** Without `{% raw %}`, `copier copy` hard-fails:
  `jinja2.exceptions.UndefinedError: 'matrix' is undefined` — **zero files rendered**. With `{% raw %}{% endraw %}`
  guards the `${{ matrix.os }}` / `${{ matrix.python }}` survive verbatim. ⇒ every CI workflow with `${{ }}` MUST be
  raw-guarded or templating-excluded.
- **TEST 2 — `uv.lock` 3-way merge (WS-8): PROVEN — a *diverged* lock merge corrupts the TOML.** (Precise claim: not
  that a lockfile is categorically un-mergeable, but that when template and user diverge on the same key, Copier's 3-way
  merge injects git conflict markers that make the TOML invalid.) Carrying `uv.lock` in a template and updating after
  template+user diverge injects those markers:
  ```
  [[package]]
  name = "anyio"
  <<<<<<< before updating      <- uv.lock line 6
  version = "4.6.2"
  =======
  version = "4.5.0"
  >>>>>>> after updating
  ```
  → `tomllib.TOMLDecodeError: Invalid statement (at line 6, column 1)`. ⇒ `uv.lock` is **templating-EXCLUDED**;
  regenerate via `uv lock` in a post-render migration. (Matches its `migration-gated` class in §3.)
- **TEST 3 — independent multi-overlay update (WS-3/WS-9): PROVEN.** Two overlays composed into one project with
  coexisting `.copier-answers.base.yml` + `.copier-answers.python.yml`; bumping only `base` to v2 and running
  `copier update -a .copier-answers.base.yml --vcs-ref v2` updated `GOVERNANCE.md` (base v1→v2) and left `PYSTACK.md`
  **byte-identical** (sha unchanged; `git status` shows it untouched). ⇒ per-overlay update is genuinely independent.

> Methodology note (honesty): the first dry-run pass failed both TEST 2/3 with `Template not found` — the spike
> templates lacked a `{{ _copier_answers }}` answers-file template, so no `.copier-answers.*.yml` was written and
> `copier update` had no `_src_path`. The corrected harness adds the answers template (named `{{ _copier_conf.answers_file }}.jinja`
> for per-overlay files) and drops `_subdirectory`. **Build requirement:** every overlay template must ship the answers
> template, or `copier update` is dead on arrival.

## 7. WS-8…WS-12 findings (woven)

- **WS-8 `uv.lock` coherence** — PROVEN un-mergeable (§6 TEST 2). Templating-excluded; `uv lock` post-render migration; the
  CI lock-freshness (`uv lock --check`) + OSV-Scanner-on-`uv.lock` gates run against the regenerated file.
- **WS-9 overlay ordering / idempotency** — `mcp-capability` presupposes `python-stack` (it lands a service into the
  `services/` scaffold + adds `[tool.uv.sources]` rows). Apply order: **base → python-stack → mcp-capability**. Independent
  update proven (§6 TEST 3); guard against a base re-apply stomping overlay-injected `pyproject` regions (the split in §3.1
  keeps `[tool.uv.sources]` overlay-composed/migration-gated, not base-re-rendered).
- **WS-10 Jinja collision** — PROVEN (§6 TEST 1). `ci.yml`/`release.yml`/`scorecard.yml` raw-guarded or templating-excluded.
- **WS-11 dogfooding paradox** — resolved as R-B: `.copier-answers.base.yml` link (see §10).
- **WS-12 `.copier-answers.*.yml` vs the lint** — the current structure-lint has **no root-level catch-all allowlist**:
  `test_no_stray_python_at_root` only flags `*.py`, `test_markdown_only_at_root_*` only flags `*.md`, and `ROOT_REQUIRED` is
  a presence (not exclusivity) check. A root `.copier-answers.base.yml` (a dotfile, non-`.md`/non-`.py`) therefore **does not
  trip the lint** — confirmed by reading `tests/test_structure.py`. Phase-2 option (do NOT force now): add
  `.copier-answers.base.yml` to `ROOT_REQUIRED` for *linked* repos so a repo that lost its answers file (its update linkage)
  is flagged. Filed to the register, not built in the spike.

## 8. Standard Reconciliation + Version (WS-5)

### 8.1 Overlay → archetype-section map (no invented layouts)

| Overlay | Maps to | Gap |
|---|---|---|
| **base** (`template-governance-base`) | No dedicated section — base furniture is only *implied* (OSS-furniture root set `repo-structure-standard.md:111`, MD allowlist `repo-hygiene.md:136`, Universal principles `:24-36`). | Amendment: promote a named "base / governance-furniture" archetype. |
| **python-stack** (`template-py-uv-workspace`) | "AI-agent / MCP monorepo (Python, uv workspace)" `:100-155`; simpler shape "Python package" `:86-98`. | The `:100` section bundles MCP+agent; a pure py-uv overlay is a *subset*. |
| **mcp-capability** (`template-mcp-capability`) | Woven into `:100-155` (`services/<svc>/` + Dockerfile Iron Law `:119,142`; `configs/` MCP template `:128`). | No standalone MCP section. |

### 8.2 Reference-impl claim after the split

Asserted today at `repo-structure-standard.md:100` and `repo-hygiene.md:123`. After the split this repo is the **composed
output** of the three overlays. Keep the claim anchored to the `:100` section, amended to mean "the *composed
materialization* of base + python-stack + mcp-capability," not a monolith. Each *separately materialized* overlay earns
its own reference-impl claim only when independently built (un-built stacks stay declarative contracts per R-A).

### 8.3 Structure-version strategy — **single base-owned integer**

Retain the single integer (`v1`, declared `repo-structure-standard.md:18`, mirrored in `pyproject.toml`, asserted by
`test_structure.py:142-155`, guarded by config-audit R1). The whole conformance system assumes one integer (R1 captures a
single `vN`; estate roll-up deferred until ≥2 marker repos). Composite per-overlay versioning is a *real* future need (once
overlays update independently, one integer can't express "python bumped, base didn't") but is exactly the
standard-ahead-of-exemplar that reference-impl-first warns against — **codify it from the first real two-overlay update**.
File composite versioning to the deferred register.

### 8.4 Required standard amendments (RECOMMENDATIONS — unsigned)

1. Add a named "base / governance-furniture" archetype (promote `:111` + `:24-36`).
2. Amend `:100` so "template-ai-monorepo" denotes the *composed* materialization.
3. Record the R-A realization rule (un-built stacks = declarative contracts).
4. State the single base-owned integer scheme; flag composite versioning deferred.
5. Reconcile the tracker location (WS-0 / WS-6 #1).

### 8.5 Drift-Tooling Punch List (WS-6)

Every coupling that breaks (or is gapped) when the single repo is split. Ranked by severity — silent (fail-green)
failures rank highest. **#1 and #2 are the load-bearing build-time must-fixes** flagged throughout this report.

| # | Sev | File | Coupling | Current | Required | Owner |
|---|---|---|---|---|---|---|
| 1 | **HIGH** | `~/.gemini/workflows/end-session.md:27` | `REGISTER_ACTIVE` tracker-discovery probe (verified: globs `ISSUES.md`, `REGISTER.md`, `docs/register*.md`, `docs/issues*.md`, `docs/registers/tracker.md`) | Repo ships `docs/planning/TRACKER.md` → **none of those globs match → binding unset → carry-forward silently omitted**. Each overlay inherits the miss. | Widen the probe to resolve both homes (`docs/{registers,planning}/{TRACKER,tracker}.md`), per WS-0 R2. **Fails silently** → top rank. | base overlay (docs layout) + end-session spec |
| 2 | **HIGH** | `test_structure.py:142-155` ↔ `pyproject.toml:56-57` | `test_version_marker_matches_declaration` cross-asserts `CONFORMS_TO_STRUCTURE_VERSION` == `[tool.structure_lint].version` | Both in one repo today. On split, `pyproject.toml` is python-stack-owned but the version *concept* tracks the base standard → the two-place agreement spans an overlay seam; ownership ambiguous, and an independent `copier update` of one side could desync it. | Explicit seam decision: which overlay declares the version, and how the cross-assert stays satisfiable post-independent-update (recommended: base owns the marker concept, python-stack carries it mechanically, the assert stays in the base harness reading the rendered pyproject). | base (marker concept) / python-stack (pyproject mechanics) |
| 3 | MED | `manage-repo-structure` | Only existing scaffolder workflow | Scaffolds the PowerShell pillar/verb taxonomy; zero copier-overlay awareness. | A copier-backed `scaffold-repo` (WS-7) to materialize the overlays — else the split has no realization tool. Gap, not breakage. | new `scaffold-repo` workflow |
| 4 | MED | `manage-project-planning` + `project-planning-artifacts.md` | Canonical tracker location / one-name-per-role | Canon = `docs/registers/tracker.md`; repo ships `docs/planning/`. An audit flags the divergence (couples with #1). | Reconcile via WS-0 R2 (amend canon, additive). | base overlay + REF-PLANNING |
| 5 | MED | `.pre-commit-config.yaml` | Mixed base + python hooks in one file | Generic hooks (whitespace/eof/gitleaks) + python hooks (ruff/pyright/structure-lint) co-located → copier 3-way-merge territory on split. | Seam: base ships generic hooks, python-stack ships ruff/pyright/structure-lint, mcp adds none. | base / python-stack seam |
| 6 | MED | config-audit R1 (`Test-StandardVersionAnchor.ps1`) | R1 regex matches a single `vN`, asserts integer | Works for the single integer. | Change **only if** WS-5 reverses to composite per-overlay versioning (it did not) — listed as the trip-wire. | config-audit (R1) |
| 7 | LOW | config-audit R1 anchor read | R1 reads the machine-local `~/.claude/rules/repo-structure-standard.md` | R-B extracts a **copy** into `template-governance-base`; R1 guards only the local anchor → the copy could drift unnoticed. | Keep the base-template copy in sync with / referencing the local anchor. Drift surface, no R1 change. | `template-governance-base` |
| 8 | LOW | estate-scan roll-up (`repo-hygiene` deferred check) | "Deferred until ≥2 marker repos" | Deferred (one repo today). | Materializing a second marker-carrying repo **activates** the prerequisite — build the deferred roll-up then. | estate-scan |

## 9. Naming (WS-7)

- **Repo names (`template-*`):** `template-governance-base`, `template-py-uv-workspace`, `template-mcp-capability` — all
  fit; no collision. These are git-repo names, outside the skill/workflow kebab taxonomy (governance §9.2), so no conflict.
  Keep `template-ai-monorepo` as the **composition reference** (the realized exemplar pulling the three overlays).
- **Scaffold workflow (verb-based, §9.2):** introduce a **distinct** copier-backed `scaffold-repo` (with `--stack`) or the
  per-stack trio (`scaffold-py-repo` / `scaffold-mcp-capability` / `scaffold-governance-base`). `manage-repo-structure`
  scaffolds the **PowerShell pillar/verb taxonomy** + prunes empty dirs — different mechanism and target → **no functional
  collision**, but a scope-overlap to call out. **Operator decision flagged:** new `scaffold-repo` workflow vs extending
  `manage-repo-structure` (manager-scope). No collision with `manage-project-planning`.

## 10. This-Repo Link-Back (WS-11 / R-B)

**Recommendation: `.copier-answers.base.yml` link. Confidence: HIGH. Reversibility: HIGH.**

| Option | Verdict | Why |
|---|---|---|
| Standalone hand-mirror | Reject | Governance updates must be hand-re-copied — reintroduces exactly the drift this partition exists to kill. |
| **`.copier-answers.base.yml` link** | **Choose** | `copier update` pulls governance via 3-way merge. This repo stays an ordinary working repo — **not Jinja-ified** — so its own `.github/workflows/*.yml` keep literal `${{ }}` with no `{% raw %}` hazard. Propagation without templating the consumer. |
| Full dogfood-regenerate | Defer (don't reject) | Highest integrity but requires Jinja-ifying the working repo's CI (the empirically-confirmed `${{ }}` hard-fail). Belongs in a *separate* generate-from-scratch smoke repo, not by converting the live reference impl. |

R-B already decided the base is a **copy** (extract, don't move), so this repo keeps its files; the link is metadata only.
De-linking = delete the single `.copier-answers.base.yml` — no content rewrite, no merge to unwind.

## 11. Planning-Taxonomy (WS-0)

**Recommendation: R2 — ratify `docs/planning/` as the AI-monorepo archetype's canonical home; amend the standard to the
reference impl, not the reference impl to the standard.**

- **Reference-impl-first is the deciding lens.** REF-PLANNING's `docs/registers/tracker.md` was distilled from *one client
  engagement*, not the AI-monorepo archetype. For *this* archetype the built exemplar is this template; the materialized
  exemplar outranks a generic default carried from a different archetype. R1 relitigates a working layout for cosmetic
  conformance.
- **REF-PLANNING already sanctions it** ("an optional single roadmap/plan doc" alongside `docs/adr/`; "adapt file names,
  keep the structure"). `docs/planning/{PLAN,TRACKER,DONE}` keeps the rate-of-change separation and co-locates the trio —
  more legible for a cloner than scattering the tracker next to the debt register.
- **R1 is high-churn, low-gain** — it relocates four files, rewrites `docs/planning/README.md`, and edits **two signed
  ADRs** for a folder-name preference.
- **R2's cost is contained** — the amendment is additive (allows a co-location, weakens nothing); the probe-widening is
  mechanical.

**deferred-vs-DEBT tension — resolved as a non-conflict.** repo-hygiene §3's "ONE register (`deferred-hardening.md` OR
`DEBT.md`)" names the single *debt* register; REF-PLANNING's distinct "Deferred (scoped-out *features*) + DEBT" bullet
(lines 76-77) fires *"as applicable"* — only when scoped-out features exist. The template has one debt register and no
feature backlog, so it is compliant with both. Note the latent token-collision the amendment must avoid: REF-PLANNING
reserves the `deferred` token for the *features* role, while repo-hygiene's `deferred-hardening.md` uses it for the *DEBT*
role — the diff above names the register by role to keep REF-PLANNING internally consistent. **Do not add a second file**;
add only the one-line reconciliation note.

Surgical, **unsigned** diff (R2 branch — minimal lines only; the spike does NOT apply it):

```diff
--- a/.claude/rules-library/project-planning-artifacts.md
+++ b/.claude/rules-library/project-planning-artifacts.md
@@ Tier 0 — Core (EVERY agentic repo)
-- **Lean tracker (open work)** -> `docs/registers/tracker.md`. One line + terse why + pointer to the owning
-  ADR/design; remove-on-done; stable IDs; phased; size-disciplined. Row status vocabulary: **`OPEN` /
+- **Lean tracker (open work)** -> `docs/registers/tracker.md` (archetype carve-out: an AI-monorepo that
+  co-locates the Tier-0 PLAN/TRACKER/DONE trio uses `docs/planning/TRACKER.md` — see the `template-ai-monorepo`
+  reference impl). One line + terse why + pointer to the owning
+  ADR/design; remove-on-done; stable IDs; phased; size-disciplined. Row status vocabulary: **`OPEN` /
   `IN-PROGRESS` / `BLOCKED`** (BLOCKED stays in the tracker).
@@ Tier 0 — Core (EVERY agentic repo)
-- **Deferred + DEBT** -> as applicable, carrying IDs so a `# DEFERRED: <ID>` marker resolves. **Deferred**
-  (scoped-out features w/ IDs) and **DEBT** (non-feature debt/constraints) stay **distinct**.
+- **Deferred + DEBT** -> as applicable, carrying IDs so a `# DEFERRED: <ID>` marker resolves. **Deferred**
+  (scoped-out features w/ IDs) and **DEBT** (non-feature debt/constraints) stay **distinct** — but a repo with
+  only non-feature debt carries the single `repo-hygiene §3` **DEBT register**, whether named `deferred-hardening.md`
+  or `DEBT.md` (the filename `deferred-hardening.md` denotes the DEBT *role* despite the `deferred` token — it is NOT
+  the scoped-out-features artifact); the distinct Deferred-features file is created only when such features accrue.
```

Companion (workflow edit, post-spike): broaden `end-session`'s tracker-discovery to resolve both homes — glob
`docs/{registers,planning}/{TRACKER,tracker}.md` instead of the single `docs/registers/tracker.md`. Verified location:
the `REGISTER_ACTIVE` probe row at `~/.gemini/workflows/end-session.md:27`.

## 12. Per-Stack Realization + Contract Schema (WS-13 / R-A)

**base + Python = materialized** (Python earned it — a working tree exists). **PowerShell / M365 / projects / generic =
declarative `*-structure-repo.md` contract**, NOT a speculative tree. An un-built stack ships a contract (a hypothesis the
first real build corrects), stays `status: EXPERIMENTAL`, and is promoted to `VERIFIED` when its reference impl
materializes. **No speculative per-stack contract authored here** — only the schema every such file must satisfy:

| # | Field | Pins | Notes |
|---|---|---|---|
| 1 | Frontmatter | `id`, `type: REFERENCE`, `status`, `gist` | `EXPERIMENTAL` while contract-only; `VERIFIED` once materialized. |
| 2 | Stack + archetype | Stack name + archetype realized | One line. |
| 3 | Materialization status | `CONTRACT-ONLY` or `MATERIALIZED → <repo>` | The reference-impl-first gate, machine-readable. |
| 4 | structure-version | The `CONFORMS_TO_STRUCTURE_VERSION` integer pinned | Join to the standard; surfaces the stack for re-audit on a bump. |
| 5 | Required roots | Allowlisted top-level entries | **Data list, not a drawn tree** (a tree is the speculative form forbidden). |
| 6 | Member roots | Member-container dirs (the `packages/`+`services/` analogue) or `single-root` | Drives the member-allowlist rule. |
| 7 | Test layout | Test root; mirrored-tree rule; gate-safe vs excluded split + marker | E.g. `tests/` `unit/` gate-safe vs `integration/` excluded. |
| 8 | Gate runner | The single quality-gate entry command | One source of truth, invoked identically dev/hook/CI. |
| 9 | Linter + settings | Linter + committed settings path | ruff+`pyproject.toml`; PSScriptAnalyzer+`PSScriptAnalyzerSettings.psd1`. |
| 10 | Hook + CI mirror | Pre-commit mechanism + the mirroring CI job | per repo-hygiene §2.4. |
| 11 | Frontmatter enums | A **pointer** to the canonical enum source — never re-declared | DRY; cite repo-hygiene §3 / `FRONTMATTER_TYPES`. |
| 12 | Deployable rule | Per-service containerisation Iron Law (or stack equivalent), or `N/A` | Only if the stack ships runnable services. |

**Can the WS-2 config-driven floor enforce a contract-only stack? Yes — for the declaration; not tree-shape (correct).**
A CONTRACT-ONLY stack is enforceable on everything that is *data*: structure-version match (4), required-/member-roots
well-formedness (5-6), frontmatter-enum validity (1, 11). Tree-shape conformance (5-7 against real files) activates only on
materialization — forcing it earlier is the speculative tree R-A prohibits. The two states map cleanly onto the two
enforcement surfaces, no special-casing.

## 13. Independent-review verdict

Two independent Tier-0 adversarial reviewers (diverse lenses: governance/standards correctness; technical/architecture
soundness), each verifying load-bearing claims against the live files rather than the report's own citations.

**Verdict: GO-WITH-CHANGES (both lenses) — no NO-GO; the partition design is sound.** Both independently confirmed
`git ls-files = 59`, that every cited `file:line` resolves exact against the live tree, that the §11 unsigned diff matches
`project-planning-artifacts.md` verbatim, that the WS-0 deferred-vs-DEBT "non-conflict" framing is substantively correct,
and that the spike **edits no standard** (every amendment is an unsigned recommendation deferred to a separately-signed pass).

Findings folded into this report (this revision):
- **MAJOR (governance, convergent-credible) — config-hoist floor gap.** The original single base floor omitted the python-uv
  rows, so a consumer could shrink `root_required` below today's hard guarantee. **Fixed:** §4.3 is now a **two-tier floor**
  (base furniture + a python-stack overlay floor over `uv.lock`/`pyproject.toml`/`.pre-commit-config.yaml`/`.python-version`
  + a `member_roots` membership floor); §4.4 reworded to scope the guarantee honestly (defends shrinkage; widening layout
  sets is acceptable because security gates stay base-hardcoded).
- **MAJOR (technical) — `agent.py` is wholly MCP-coupled.** Verified from source (imports `MCPToolset`/`fastmcp`, launches
  `example_mcp_server`). **Fixed:** §3 row re-labelled with the ‡ footnote (not region-splittable); the WS-4 "done" gate in
  §5/§15 now requires *authoring a de-MCP'd `agent.py` variant* and a green no-MCP render, not merely "a subset render."
- **MINORs folded:** §4.2/§4.3 `.editorconfig` floor reconciled; TEST-2 wording softened to "diverged-merge corrupts TOML"
  (not categorically un-mergeable); `repo-structure-standard:119` Dockerfile anchor corrected; §11 `§77`→"lines 76-77" and the
  deferred/DEBT token-collision named by role; §3 exhaustiveness note added for the spike's own two meta-docs; the WS-6 drift
  punch list (previously inline-only) promoted to a dedicated §8.5 pinning #1/#2.

No finding rose to NO-GO; all are corrections to framing/coverage, not design defects.

## 14. Decision Gate

Decision-ready per the plan's criteria: every tracked file has a four-column WS-1 row (no `TBD`); every
`test_structure.py` constant has a hoist verdict + owner + the non-overridable floor specified; the tool matrix has a
verdict with the multi-overlay independent-update claim **empirically** confirmed; the dry-run recorded outcomes for all
three claims; WS-0 produced an R1/R2 recommendation + surgical unsigned diff; every decision-gate axis has a recommendation
+ confidence + reversibility cost. The two HIGH silent-failure couplings (WS-6 #1, #2) are the load-bearing build-time
must-fix items but do **not** block the go/no-go.

## 15. Build Sequencing (post-spike, separately signed)

1. Extract `template-governance-base` (copy, per R-B) — the base harness + furniture + the floor test; give it its **own
   CI gate before it may push** (locked prior). Ship the answers-file template (§6 build requirement).
2. Extract `template-py-uv-workspace` — python-stack data + lint constants + uv/ruff/pyright/pytest content; raw-guard CI.
3. Extract `template-mcp-capability` — the MCP service + config template + roundtrip test. **Gate "done" on authoring a
   bare non-MCP `agent.py` variant and proving the no-MCP render passes `pytest`/`pyright`/structure** (the §3 ‡ / §5 caveat).
4. Hoist `[tool.structure_lint]` data + add the floor test (WS-2) — prerequisite for multi-overlay.
5. Link this repo via `.copier-answers.base.yml` (R-B); resolve WS-6 #1 (tracker probe) and #2 (version-marker ownership).
6. Apply the WS-0 R2 standards amendment + the tracker-probe widening via `/manage-rules` (separately signed).
7. File the deferred items: composite versioning (WS-5), `.copier-answers` in `ROOT_REQUIRED` for linked repos (WS-12).

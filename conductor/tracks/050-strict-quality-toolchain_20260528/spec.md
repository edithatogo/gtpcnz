# Strict Quality Toolchain

## Problem

The repo has useful checks, but the current quality posture is not yet fully strict. The type-checker configuration exists, but the strict type gate is not enforced in CI. Dependency automation exists through Dependabot, but Renovate is not configured. Coverage, mutation testing, property-based testing, edge-case fuzzing, and profiling are not yet standard release gates.

## Current Status

| Area | Current status | Verdict |
|---|---|---|
| Pydantic v2 | `pydantic>=2,<3` is present in `pyproject.toml` and `requirements.txt`; contracts use v2 APIs such as `ConfigDict`, `TypeAdapter`, and `model_validator`. | Present |
| mypy | Strict config exists in `pyproject.toml`, but CI and `scripts/dev_check.py` do not run mypy. | Configured, not enforced |
| basedpyright | No config or CI gate found. | Missing |
| ty | No config or CI canary found. | Missing |
| Renovate | No Renovate config found; Dependabot config exists. | Missing |
| Coverage threshold | No `pytest-cov` dependency or `--cov-fail-under=90` gate found. | Missing |
| Edge tests | Some targeted edge tests exist, but no explicit edge-test inventory/gate. | Partial |
| Property-based tests | Hypothesis is documented as a possible improvement, but not installed or enforced. | Missing |
| Mutation testing | No `mutmut`, `cosmic-ray`, or equivalent config found. | Missing |
| Scalene profiling | No Scalene dependency, workflow, profile artifact, or recorded run found. | Missing |
| GitHub enforcement | CI workflows exist, but `main` is not protected and no rulesets/required checks are configured. | Missing |

## Type Checker Decision

Use a three-lane posture:

| Lane | Role | Recommendation |
|---|---|---|
| `basedpyright` | Primary strict static gate | Make this the blocking type gate once configured, because it is strict by default and better suited to modern editor/CI feedback than mypy alone. |
| `mypy` | Compatibility and library-ecosystem gate | Keep initially, because it is mature and catches issues differently; remove later only if the duplicate cost becomes high. |
| `ty` | Fast forward-looking canary | Add as non-blocking at first because it is a fast Astral type checker, but still young enough that it should not be the only blocking gate yet. |

## Target Quality Stack

| Capability | Target tool |
|---|---|
| Fast package/runtime management | `uv` |
| Lint/format/import hygiene | `ruff` |
| Blocking static typing | `basedpyright` strict |
| Secondary static typing | `mypy --strict` |
| Type-checker canary | `ty check` |
| Runtime contracts | Pydantic v2 |
| Tabular/schema validation | Pandera and Arrow schemas |
| Coverage | `pytest-cov` with `--cov-fail-under=90` |
| Property tests | Hypothesis strategies derived from contracts/registries |
| Mutation tests | `mutmut` against pure calculation and engine modules |
| Profiling | Scalene profile of Streamlit-free calculation and engine paths |
| Dependency automation | Renovate plus Dependabot security where available |
| Security | `pip-audit`, CodeQL, secret scanning, branch rulesets |

## Acceptance Criteria

- CI runs `ruff`, `basedpyright`, `mypy`, tests with coverage threshold, concern-boundary scan, no-patient-data scan, dependency audit, Quarto render, and Streamlit import smoke test.
- `ty` runs as a scheduled or manual non-blocking canary until promoted.
- `renovate.json` exists and Renovate is either installed as a GitHub App or run through a scheduled self-hosted workflow.
- Coverage threshold is at least 90 percent for the model package or an explicit ratchet is documented.
- Property tests cover registry validation, runtime clamps, engine input/output contracts, and stochastic reproducibility.
- Mutation testing is configured for pure calculation and engine modules, with an initial survivorship baseline and ratchet.
- Scalene is installed, has a documented command, and has at least one committed profile summary or artifact path.
- GitHub `main` has branch protection or a ruleset with required checks before merge.

## Non-Goals

- Do not make `ty` the only type checker until the repo proves it catches the same project-critical issues as the blocking checker.
- Do not apply mutation testing to Streamlit UI code first; start with pure model logic.
- Do not require 90 percent coverage over generated site output, local caches, or public mirrored artifacts.
- Do not claim strict CI/CD until GitHub branch rules or rulesets enforce required checks.

## Verification

```powershell
rg -n "basedpyright|ty check|mypy|ruff|pytest-cov|cov-fail-under|hypothesis|mutmut|scalene|renovate|pip-audit|codeql" .github pyproject.toml requirements.txt scripts conductor docs models
python scripts/dev_check.py
gh api repos/edithatogo/gtpcnz/branches/main/protection
gh api repos/edithatogo/gtpcnz/rulesets?includes_parents=true
```

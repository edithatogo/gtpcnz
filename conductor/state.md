# Conductor State

GTPCNZ is a public-data anchored benchmark and educational explainer. It is not linked-data calibrated and not a patient-level forecast.

Current active tracks:

- `043-concern-extraction-strict-validation_20260526`: extracts contracts, registries, validation boundaries and Streamlit UI bindings into typed layers. All 7 phases completed.
- `044-game-theory-formula-validation_20260527`: game formula nonlinearity audit, regression tests, educational-language docs.
- `045-inputs-calibration-provenance_20260527`: provenance registry, OIA component map, data-freshness gate.
- `046-public-website-visual-contract_20260527`: wording contract, visual gallery contract, public mirror sync.
- `047-streamlit-deployment-experience_20260527`: UI polish, accessibility captions, deployment runbook.
- `048-equilibrium-solver-exploration_20260528`: decided — keep heuristic Nash, do NOT add analytical solver lane. Documented in `docs/decisions/solver-posture-v1.8.5.md`.
- `049-bleeding-edge-analytical-enhancements_20260528`: MoSCoW shortlist complete. First-wave: tornado sensitivity, equity/rural stratification, seeded Monte Carlo, waterfall charts, heatmap matrix. Documented in `docs/decisions/enhancement-shortlist-v1.8.5.md`.
- `050-strict-quality-toolchain_20260528`: hardens type checking, dependency automation, coverage, property/mutation tests, profiling, security scans and GitHub enforcement. Local gates passed on 2026-05-28 with repo health 11/11, bleeding-edge scorecard 17/17, 134 tests passed, and 91.68% model-package coverage. Remote enforcement now has active default-branch ruleset `main baseline protection` requiring PR flow, resolved review threads, linear history, no deletion/force-push, and both `test-and-render` and `Quality / python-quality` CI checks.

Completed subagent workstreams:

| Workstream | Outputs | Status |
|---|---|---|
| A - Contracts | `contracts/*` (parameters, inputs, scenarios, results, engine protocol), schema tests | Done |
| B - Registries | `registries/parameters.v1.yaml` (24 params), `registries/inputs.v1.yaml` (7 datasets), loader tests | Done |
| C - Pandera/Arrow | `validation/arrow_schemas.py`, `validation/runtime_checks.py`, schema alignment | Done |
| D - Engines | `engines/*` (7 typed adapters: ABM, SD, JAX-MC, sensitivity, diffusion, MPC, Nash opt) | Done |
| E - UI/Visuals | Live validation badges, calculation panel, stochastic replay, result-manifest badges | Done |
| F - CI/Audit | basedpyright strict config, mypy strict compatibility gate, Ruff, pip-audit, CodeQL workflow, concern-boundary scanner (5 gates), check_no_patient_data.py | Done |
| G - Tests | 134 passing tests with 91.68% model-package coverage, Hypothesis property tests, mutation-test workflow | Done |

Current public gates:

- `python scripts/check_repo_health.py`
- `python scripts/check_concern_boundaries.py`
- `python scripts/check_no_patient_data.py`
- `python -m pytest -q --cov=models.primarycare_model --cov-report=term-missing --cov-fail-under=90`
- `python -m basedpyright --pythonpath <current-python>`
- `python -m mypy models/primarycare_model/contracts models/primarycare_model/validation/pandera_schemas.py`
- `python -m ruff check .`
- `python -m pip_audit -r requirements.txt`
- `quarto render --to html`

Claim boundary:

The repo may describe public-data anchored model-generated indices, deterministic calculations and seeded stochastic demonstrations. It must not claim patient-level forecast accuracy, linked-data calibration, realised fiscal savings, realised hospital-demand reductions, or implementation effects without a documented calibration upgrade.

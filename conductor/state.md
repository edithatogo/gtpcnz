# Conductor State

GTPCNZ is a public-data anchored benchmark and educational explainer. It is not linked-data calibrated and not a patient-level forecast.

Current active tracks:

- `042-simulation-engine-evolution_20260526`: Rust-core DES, VOI, MARS, diffusion, ABM/GNN/WASM/privacy/formal-check follow-through, and final integration gates remain active.

Recently completed tracks:

- `043-concern-extraction-strict-validation_20260526`: contracts, registries, validation boundaries and Streamlit UI bindings extracted into typed layers.
- `044-game-theory-formula-validation_20260527`: nonlinear payoff logic, best-response curves, gaming-risk frontier and regression tests.
- `045-inputs-calibration-provenance_20260527`: provenance registry, OIA component map, data-freshness gate and calibration-boundary metadata.
- `046-public-website-visual-contract_20260527`: public wording contract, visual gallery contract and public mirror sync.
- `047-streamlit-deployment-experience_20260527`: app structure, tabs, controls, smoke tests, deployment entrypoint and accessibility/performance polish.
- `048-equilibrium-solver-exploration_20260528`: decided to keep heuristic Nash and not add an analytical solver lane. Documented in `docs/decisions/solver-posture-v1.8.5.md`.
- `049-bleeding-edge-analytical-enhancements_20260528`: three analytical waves completed, including sensitivity, subgroup, uncertainty, stress, interaction, VOI, diffusion, clustering, composite, evidence and UI wiring work.
- `050-strict-quality-toolchain_20260528`: strict type/lint/test/security/dependency/profile toolchain and CI controls completed.
- `051-dashboard-ui-methodology-completion_20260530`: Methodology & evidence tab, linked definitions, evidence exports, lazy analytical views and focused tests completed.
- `052-dashboard-lab-enhancements-deep-dive_20260530`: all seven lab explainers, combined analyses, clustering, row highlighting, linked Substack cross-references and focused tests completed.

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

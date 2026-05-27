# Conductor State

GTPCNZ is a public-data anchored benchmark and educational explainer. It is not linked-data calibrated and not a patient-level forecast.

Current active tracks:

- `043-concern-extraction-strict-validation_20260526`: extracts contracts, registries, validation boundaries and Streamlit UI bindings into typed layers. All 7 phases completed.
- `048-equilibrium-solver-exploration_20260528`: decides whether to keep Nash as an educational heuristic or add a separate analytical solver lane.
- `049-bleeding-edge-analytical-enhancements_20260528`: ranks additional inputs, subgroup analyses, secondary analyses, visualisations, and simulation modes worth promoting without breaking the public-data boundary.

Completed subagent workstreams:

| Workstream | Outputs | Status |
|---|---|---|
| A - Contracts | `contracts/*` (parameters, inputs, scenarios, results, engine protocol), schema tests | Done |
| B - Registries | `registries/parameters.v1.yaml` (24 params), `registries/inputs.v1.yaml` (7 datasets), loader tests | Done |
| C - Pandera/Arrow | `validation/arrow_schemas.py`, `validation/runtime_checks.py`, schema alignment | Done |
| D - Engines | `engines/*` (7 typed adapters: ABM, SD, JAX-MC, sensitivity, diffusion, MPC, Nash opt) | Done |
| E - UI/Visuals | Live validation badges, calculation panel, stochastic replay, result-manifest badges | Done |
| F - CI/Audit | mypy strict config, concern-boundary scanner (5 gates), check_no_patient_data.py | Done |
| G - Tests | 113 passing tests (engine adapters, registries, validation, concern boundaries) | Done |

Current public gates:

- `python scripts/check_repo_health.py`
- `python scripts/check_concern_boundaries.py`
- `python scripts/check_no_patient_data.py --verbose`
- `pytest -q`
- `quarto render --to html`

Claim boundary:

The repo may describe public-data anchored model-generated indices, deterministic calculations and seeded stochastic demonstrations. It must not claim patient-level forecast accuracy, linked-data calibration, realised fiscal savings, realised hospital-demand reductions, or implementation effects without a documented calibration upgrade.

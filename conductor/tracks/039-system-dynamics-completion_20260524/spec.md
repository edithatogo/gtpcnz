# Spec: System Dynamics Stub Completion

## Problem

`models/primarycare_model/sd_stub.py` is still a placeholder. It advances a simple unmet-need and hospital-pressure state, but it does not provide a complete stock-flow model, does not expose calibrated-ready parameter contracts, and cannot honestly support a "no stubs" model-status claim.

## Goal

Replace the system-dynamics placeholder with a completed, tested, public-data anchored stock-flow simulation layer for unmet need, primary-care capacity, ambulance diversion/resolution, hospital pressure, fiscal-risk pressure and policy-control feedback.

The completed layer must remain explicitly non-calibrated unless real linked data and validation evidence are added later.

## Owned Files

Primary:

- `models/primarycare_model/sd_stub.py` or its successor module name;
- `models/tests/test_model_stubs.py` or successor system-dynamics tests;
- `docs/calibration/model-card-v1.7.2.md`;
- `docs/contracts/repo-github-streamlit-contracts-v1.8.3.md`;
- `scripts/check_repo_health.py`.

Supporting:

- `models/primarycare_model/full_parameterised_model_v170.py`;
- `models/primarycare_model/uncertainty.py`;
- `models/primarycare_model/scenario_service.py`;
- `reports/primary_care_architecture.qmd`.

## Requirements

1. Replace the stub with a real stock-flow module or rename it to a non-stub module and update imports.
2. Model at least generated need, unmet need, primary-care capacity, resolved primary contacts, ambulance-resolved care, hospital pressure, fiscal-risk pressure and control/audit feedback.
3. Support scenario runs over multiple periods with deterministic outputs.
4. Accept parameters from the existing full-parameterised model surface rather than hard-coded demo constants.
5. Return documented time-series outputs suitable for Quarto and Streamlit.
6. Include sensitivity hooks and bounded-state safeguards.
7. Add tests for mass-balance/intuitive invariants, non-negative stocks, deterministic reproducibility, output schema and claim-boundary text.
8. Update model cards/docs to say the stock-flow layer is completed but public-data anchored/bounded.
9. Extend repo-health checks so any remaining tracked `*_stub.py` system-dynamics placeholder or stub import fails the health gate.

## Bleeding-Edge Completion Bar

During implementation, run a short library-selection spike against current official documentation and choose between:

- a proven system-dynamics or differential-equation framework if it improves correctness and auditability;
- a small internal stock-flow engine if the model is clearer, lighter and easier to validate.

The selected approach must support current Python 3.11+, deterministic tests, clear parameter schemas, tabular time-series output and direct Streamlit/Quarto integration. Avoid dependencies that obscure the stock-flow equations.

## Acceptance Criteria

1. No tracked system-dynamics module or import is named `sd_stub`.
2. `SystemState`/`step` behaviour is preserved or superseded by a tested equivalent.
3. Multi-period simulation outputs are documented and deterministic.
4. Non-negative stock and pressure invariants are tested.
5. `pytest -q` passes.
6. `python scripts/check_repo_health.py` passes with a no-stub check.
7. Model communication distinguishes "completed public-data anchored stock-flow layer" from "linked-data calibrated prediction."

## Out Of Scope

- Claiming calibrated hospital-demand or fiscal forecasts.
- Replacing stakeholder validation, OIA inputs or real-data calibration.
- Weakening existing caveats, claim boundaries, or deployment gates.

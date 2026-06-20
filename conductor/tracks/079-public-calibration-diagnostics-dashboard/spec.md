# Track 079 - Public calibration diagnostics dashboard

Build a public-safe calibration and validation diagnostics surface in Dash that explains what has passed, what is readiness-only, and what evidence is still missing.

## Scope

- Surface public aggregate calibration, posterior predictive checks, holdout validation, temporal holdout, policy-shock plausibility, calibration target readiness, source freshness, and validation-source acquisition status.
- Add a calibration diagnostics route or expand the existing Dash calibration route with:
  - observed-vs-benchmark readiness panels;
  - posterior predictive check visuals where public aggregate data are available;
  - holdout and temporal validation status;
  - policy-shock plausibility status;
  - source freshness/provenance panel;
  - missing evidence queue.
- Keep all diagnostics bounded to public aggregate validation and readiness language.

## Non-Goals

- Do not upgrade calibration claims beyond passed public gates.
- Do not infer linked-data or patient-level calibration.
- Do not use private data.
- Do not convert readiness diagnostics into precise outcome predictions.

## Required Checks

```powershell
python -m pytest -q models/tests/test_public_aggregate_calibration.py models/tests/test_posterior_predictive_checks.py
python -m pytest -q models/tests/test_public_holdout_validation.py models/tests/test_public_temporal_holdout_validation.py
python -m pytest -q models/tests/test_public_policy_shock_plausibility.py models/tests/test_calibration_target_readiness.py
python -m pytest -q models/tests/test_dashboard_claims.py models/tests/test_dash_app.py
python scripts/check_public_only_boundary.py
python scripts/check_concern_boundaries.py
```

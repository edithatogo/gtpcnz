# Inputs, Assumptions, and Calibration Report

## Findings

The repo is clear that this is a public-data anchored benchmark and educational explainer, not a linked-data calibrated or patient-level forecast. That boundary is repeated across the homepage, the dashboard, the report, and the deployment docs. The inputs layer is therefore mostly a controlled public-source and scenario-override layer rather than a production data pipeline.

The main input surfaces are:
- scenario CSVs and scenario registries in `outputs/`, `models/primarycare_model/registries/`, and `data/evidence/`
- public caveat and claim-boundary text in `models/primarycare_model/scenario_service.py`
- calibration-readiness documentation in `build_calibration_readiness_table()`
- validation schema helpers in `models/primarycare_model/validation/pandera_schemas.py`

The strongest remaining gap is provenance depth. The code tells the reader what is missing for calibration, but it does not yet trace every public assumption to a machine-readable provenance chain or a freshness policy. For a public/student audience, that is acceptable. For bleeding-edge use, it is not enough.

## Evidence

- `models/primarycare_model/scenario_service.py:77-105` defines the claim boundary and educational settings boundary.
- `models/primarycare_model/scenario_service.py:155-173` loads scenarios, validates them, and appends the `claim_boundary`.
- `models/primarycare_model/scenario_service.py:265-281` exposes `build_calibration_readiness_table()` for the missing-data map.
- `docs/audit/oia-request-tracker.csv` and `data/evidence/oia_request_tracker.csv` list the OIA/data gaps that still block calibration.
- `docs/REPORTS-AND-DASHBOARD.md:1-50` and `docs/STREAMLIT-DEPLOYMENT.md:1-45` restate the public-data benchmark boundary.
- `models/tests/test_scenario_service.py:39-105` checks schema acceptance, claim-boundary addition, and nonlinear educational scoring.

## Completion Assessment

Completed as a public explainer layer. Not completed as a calibration-grade input stack.

What is finished:
- public inputs are enumerated
- caveats are consistent across surfaces
- scenario loading has validation and a boundary label
- calibration readiness is documented

What is not finished:
- no live linked-data pipeline
- no automatic provenance graph
- no freshness/version policy for public inputs
- no empirical calibration dataset

## Bleeding-edge Recommendations

1. Add a typed provenance manifest that records source, date, transform, and license for every public input.
2. Add a calibration-readiness scorecard with machine-readable statuses, not just prose.
3. Add a source freshness check that flags stale OIA/data entries automatically.
4. Separate public assumptions from empirical assumptions so a reader can see which statements are structural and which are measured.
5. Add a reproducible ingestion note for every CSV that feeds a public-facing table or chart.

## Risks

- Readers may over-read the scenario outputs as forecasts.
- Static calibration-readiness prose can drift away from actual data availability.
- Public summaries can conceal the difference between “documented” and “verified”.
- The repo still depends on manual discipline to keep caveat language aligned across mirrored surfaces.

# Spec: Agent-Based Model Stub Completion

## Problem

`models/primarycare_model/abm_stub.py` is still a placeholder. It defines patient and provider data classes, but it does not run a genuine agent-based simulation, does not consume the full parameterised scenario surface, and cannot honestly support a "no stubs" model-status claim.

## Goal

Replace the ABM placeholder with a completed, tested, public-data anchored agent-based simulation layer that models patient demand, provider capacity, scope rules, eligibility, unmet need, contact resolution, and gaming/fiscal-risk signals across the existing scenario architecture.

The completed layer must remain explicitly non-calibrated unless real linked data and validation evidence are added later.

## Owned Files

Primary:

- `models/primarycare_model/abm_stub.py` or its successor module name;
- `models/tests/test_model_stubs.py` or successor ABM tests;
- `docs/calibration/model-card-v1.7.2.md`;
- `docs/contracts/repo-github-streamlit-contracts-v1.8.3.md`;
- `scripts/check_repo_health.py`.

Supporting:

- `models/primarycare_model/full_parameterised_model_v170.py`;
- `models/primarycare_model/scenario_service.py`;
- `docs/calibration/full-parameterised-model-build-report-v1.7.0.md`;
- `reports/primary_care_architecture.qmd`.

## Requirements

1. Replace the stub with a real ABM module or rename it to a non-stub module and update imports.
2. Model at least patient agents, provider agents, contact demand, provider capacity, scope eligibility, activity payment/control settings, unmet need, resolved contacts, unresolved contacts, fiscal-risk proxy and gaming-risk proxy.
3. Support deterministic seeded runs for tests and reproducible examples.
4. Accept scenario/parameter inputs from the existing public-data calibration surface rather than hard-coded demo values.
5. Return tabular outputs with explicit schema suitable for dashboard/report integration.
6. Include sensitivity hooks for key parameters without claiming empirical prediction.
7. Add tests for deterministic reproducibility, capacity constraints, scope rules, equity/co-payment sensitivity, output schema and claim-boundary text.
8. Update model cards/docs to say ABM is completed but public-data anchored/bounded.
9. Extend repo-health checks so any remaining tracked `*_stub.py` ABM placeholder or stub import fails the health gate.

## Bleeding-Edge Completion Bar

During implementation, run a short library-selection spike against current official documentation and choose between:

- a proven ABM framework if it materially reduces scheduler/agent risk;
- a small internal engine if the domain logic is clearer and easier to audit.

The selected approach must support current Python 3.11+, deterministic testing, typed dataclass or Pydantic-style inputs, vectorisable/tabular output, and straightforward Streamlit/Quarto integration. Do not introduce a heavy dependency only for style.

## Acceptance Criteria

1. No tracked ABM module or import is named `abm_stub`.
2. `ProviderAgent`-level scope behaviour is preserved or superseded by a tested equivalent.
3. ABM runs complete under a deterministic seed and return documented outputs.
4. Dashboard/report surfaces can use ABM outputs without changing the evidence boundary.
5. `pytest -q` passes.
6. `python scripts/check_repo_health.py` passes with a no-stub check.
7. Model communication distinguishes "completed public-data anchored ABM layer" from "linked-data calibrated prediction."

## Out Of Scope

- Claiming real-world effect sizes.
- Using synthetic ABM output as empirical validation.
- Adding private or restricted patient-level data.
- Weakening existing caveats, claim boundaries, or deployment gates.

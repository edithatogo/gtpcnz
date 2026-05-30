# Plan: Agent-Based Model Stub Completion

**Status:** Complete

## Phase 1: Discovery And Design

- [x] Read `abm_stub.py`, `full_parameterised_model_v170.py`, `scenario_service.py`, and current ABM tests.
- [x] Review current official ABM/library options and document the selected implementation approach.
- [x] Define ABM input and output schemas.
- [x] Map existing scenario parameters to patient, provider, contact, control, equity and risk mechanisms.

## Phase 2: Implementation

- [x] Implement completed ABM engine or successor module.
- [x] Preserve or migrate `PatientAgent` and `ProviderAgent` concepts into the completed model.
- [x] Add seeded simulation runner and scenario adapter.
- [x] Add output tables for contacts, unmet need, capacity use, fiscal-risk proxy, gaming-risk proxy and equity-sensitive access.

## Phase 3: Tests And Health Gates

- [x] Replace stub tests with completed ABM tests.
- [x] Add deterministic reproducibility tests.
- [x] Add capacity, scope, co-payment/equity and output-schema tests.
- [x] Add a repo-health no-stub check for ABM.
- [x] Run `pytest -q`.
- [x] Run `python scripts/check_repo_health.py`.

## Phase 4: Documentation And Claim Boundary

- [x] Update model card and relevant docs from "ABM stub" to "completed public-data anchored ABM layer."
- [x] Preserve non-calibrated caveats in README, report and dashboard surfaces.
- [x] Add a short ABM interpretation note explaining what the completed layer can and cannot support.

## Phase 5: Release Decision

- [x] Confirm no tracked `abm_stub` import or filename remains.
- [x] Confirm no stronger empirical claim was introduced.
- [x] Commit the ABM completion separately from other workspace cleanup. `fb998b5`

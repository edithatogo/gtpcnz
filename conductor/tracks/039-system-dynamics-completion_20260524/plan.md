# Plan: System Dynamics Stub Completion

**Status:** Completed

## Phase 1: Discovery And Design

- [x] Read `sd_stub.py`, `full_parameterised_model_v170.py`, `uncertainty.py`, `scenario_service.py`, and current system-dynamics tests.
- [x] Review current official system-dynamics/numerical simulation options and document the selected implementation approach.
- [x] Define stock, flow, parameter and time-series output schemas.
- [x] Map existing scenario parameters to need generation, capacity, ambulance resolution, hospital pressure and control feedback.

## Phase 2: Implementation

- [x] Implement completed stock-flow engine or successor module.
- [x] Preserve or migrate `SystemState` and `step` concepts into the completed model.
- [x] Add multi-period scenario runner.
- [x] Add output tables for stocks, flows, pressure, capacity, ambulance resolution and policy-control feedback.

## Phase 3: Tests And Health Gates

- [x] Replace stub tests with completed stock-flow tests.
- [x] Add deterministic reproducibility tests.
- [x] Add non-negative stock, bounded pressure and output-schema tests.
- [x] Add a repo-health no-stub check for system dynamics.
- [x] Run `pytest -q`.
- [x] Run `python scripts/check_repo_health.py`.

## Phase 4: Documentation And Claim Boundary

- [x] Update model card and relevant docs from "system dynamics stub" to "completed public-data anchored stock-flow layer."
- [x] Preserve non-calibrated caveats in README, report and dashboard surfaces.
- [x] Add a short stock-flow interpretation note explaining what the completed layer can and cannot support.

## Phase 5: Release Decision

- [x] Confirm no tracked `sd_stub` import or filename remains.
- [x] Confirm no stronger empirical claim was introduced.
- [x] Commit the system-dynamics completion separately from other workspace cleanup.

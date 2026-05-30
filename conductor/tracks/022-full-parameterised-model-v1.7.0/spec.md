# Track 022 — Full parameterised model v1.7.0

## Purpose

Continue building the fully parameterised model without claiming empirical calibration.

## Acceptance criteria

- Every major modelling mechanism has an explicit parameter, bounds, source status, real-data requirement and estimation strategy.
- A data-input contract identifies the real tables required for later calibration.
- The model includes current reform, uncapped scheduled medical fee-for-service, controlled hybrid, weak-control, ACC shock, urgent/ambulance, scope-only and place-only scenarios.
- The model runs monthly dynamics for access, supply, unmet need, ambulance conveyance, emergency department demand, admissions, hospital pressure and public cost.
- Outputs include CSV tables, sensitivity analysis and plots.
- Existing tests pass and new tests verify parameter coverage, bounds, scenario logic and sensitivity outputs.

## Non-goals

- Do not claim real-data calibration.
- Do not claim precise predicted reductions in ED demand, admissions or cost.
- Do not replace stakeholder validation or OIA/data acquisition.

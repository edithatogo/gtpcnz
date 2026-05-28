# Game Theory Formula Validation

## Problem

The public game-theory modules are supposed to show strategic behaviour, not simple linear trend lines. The current code has already been corrected away from the worst linear forms, but the repo still needs a dedicated track to keep payoff logic, best-response curves, and gaming-risk frontiers nonlinear, bounded, and explainable.

## Goal

Ensure the public game-theory layer remains a genuine strategic explainer:

- payoff curves must stay nonlinear and bounded;
- best-response logic must be readable in code and tests;
- gaming-risk frontier curves must expose tradeoffs instead of flat lines;
- assumptions must be explicit in the UI and report;
- formula changes must be protected by regression tests.

## Current State

| Concern | Current locations | Gap |
|---|---|---|
| Claims audit game | `models/primarycare_model/app.py` | Formulae exist, but the logic needs a dedicated track so later edits do not revert to linear payoff curves. |
| Coordination game | `models/primarycare_model/app.py` | Strategic response is present, but the curve shape and parameter choices need explicit guardrails. |
| Gaming-risk frontier | `models/primarycare_model/app.py` | Frontier is illustrative only and should be kept clearly nonlinear and bounded. |
| Mathematical helpers | `models/primarycare_model/runtime_lab.py`, `models/primarycare_model/scenario_service.py` | Shared strategic-response helpers need to remain the single source of behavioural curvature. |
| Regression tests | `models/tests/test_runtime_lab.py`, `models/tests/test_scenario_service.py` | Nonlinearity is tested in one place, but game-specific payoff surfaces still need direct coverage. |

## Target State

- Game modules present a clear strategic story, not a pseudo-forecast.
- Each payoff curve has a documented threshold or diminishing-return rationale.
- Best-response and frontier outputs are backed by tests that fail if the curve becomes linear or flat.
- The report and dashboard language makes clear that these are pedagogical game-theory surfaces.

## Acceptance Criteria

- payoff curves remain nonlinear under representative parameter sweeps;
- curve-crossing and frontier tests exist for each game module;
- the dashboard copy continues to say these are educational or illustrative surfaces, not empirical estimates;
- the game modules keep using shared helper functions instead of duplicating curvature logic in multiple places;
- no new linearised payoffs are introduced without an explicit design note.

## Non-Goals

- Do not add a full Nash solver unless the repo explicitly decides to promote this layer from explainer to analytical engine.
- Do not change the public calibration boundary.
- Do not add linked-data claims.

## Verification

```powershell
python -m pytest -q models/tests/test_app.py models/tests/test_streamlit_post_labs.py models/tests/test_scenario_service.py
python -c "from models.primarycare_model.runtime_lab import strategic_response, diminishing_return; print(strategic_response(0.5), diminishing_return(0.5))"
rg -n \"strategic_response|diminishing_return|gaming-risk frontier|best-response|payoff\" models/primarycare_model/app.py models/primarycare_model/runtime_lab.py models/primarycare_model/scenario_service.py models/tests
```

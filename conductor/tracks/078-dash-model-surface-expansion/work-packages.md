# Work Packages

## WP1 - Model Inventory

- Map runtime helpers, engine adapters, calibration modules, uncertainty modules, VOI modules, and standalone Streamlit pages.
- Define status values: `surfaced`, `partial`, `deferred_public_boundary`, `deferred_runtime`, `retired`.

## WP2 - Service Payloads

- Add Streamlit-free service helpers for ABM, Bass diffusion, Nash convergence, Monte Carlo/JAX, MPC, SD, and sensitivity outputs.
- Ensure all payloads produce Plotly figure, table, interpretation, warning, and CSV filename.

## WP3 - Dash UI

- Add route/section layout for model coverage and each surfaced model family.
- Keep navigation usable on mobile and desktop.

## WP4 - Tests and Gates

- Add coverage tests for model-surface status.
- Run focused Dash, runtime, engine-adapter, and public-boundary checks.

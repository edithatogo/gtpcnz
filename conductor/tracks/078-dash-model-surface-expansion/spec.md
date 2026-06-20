# Track 078 - Dash model surface expansion

Expose the existing modelling engines more fully in the Plotly Dash/Hugging Face public surface while preserving the public-data claim boundary.

This track turns the Dash app from a Streamlit-parity surface into a model-coverage surface. It should show which engines exist, which public routes use them, what each output is valid for, and what remains unsupported.

## Scope

- Add a model coverage matrix covering runtime helpers, engine adapters, calibration modules, uncertainty modules, VOI modules, and standalone Streamlit pages.
- Surface the currently underused modelling assets in Dash:
  - ABM playback from `models/primarycare_model/pages/2_kairos_abm_playback.py` and `engines/abm_adapter.py`;
  - Bass diffusion from `pages/3_bass_diffusion.py` and `engines/diffusion_adapter.py`;
  - Nash convergence from `pages/4_nash_convergence.py`, `nash_opt.py`, and `engines/nash_opt_adapter.py`;
  - Monte Carlo histogram/JAX Monte Carlo from `pages/5_monte_carlo_histogram.py` and `engines/jax_mc_adapter.py`;
  - MPC, system dynamics, and sensitivity adapters where public-safe table/chart payloads already exist or can be added without stronger claims.
- Add Dash routes or sections with table fallbacks and CSV downloads for each surfaced model.
- Add tests that fail if a public model engine has no documented Dash status.

## Non-Goals

- Do not claim patient-level prediction.
- Do not claim precise fiscal savings, ED reductions, hospital-demand reductions, workforce effects, implementation impacts, or causal effects.
- Do not add private, linked, or confidential data.
- Do not remove Streamlit until Dash model-surface gates and browser checks pass.

## Required Checks

```powershell
python -m pytest -q models/tests/test_dashboard_service.py models/tests/test_dash_app.py
python -m pytest -q models/tests/test_engine_adapters.py models/tests/test_runtime_lab.py
python scripts/check_public_only_boundary.py
python scripts/check_concern_boundaries.py
```

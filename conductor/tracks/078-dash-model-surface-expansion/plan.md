# Plan

1. Inventory model assets and produce a canonical `dashboard_model_surface_matrix()` service table.
2. Add Dash route sections for model coverage, ABM playback, Bass diffusion, Nash convergence, Monte Carlo/JAX, MPC, system dynamics, and sensitivity where public-safe payloads exist.
3. Convert standalone Streamlit page logic into Streamlit-free service helpers before using it in Dash.
4. Add chart/table/download fallbacks for each surfaced model.
5. Add tests that assert every model engine is either surfaced in Dash or explicitly marked as deferred with a reason.
6. Run focused Dash, runtime, engine-adapter, public-boundary, and concern-boundary gates.

## Implementation Notes

- Prefer framework-neutral helpers in `models/primarycare_model/dashboard_service.py` or a new `dashboard_model_surface.py`.
- Keep Dash callbacks light and bounded for Hugging Face CPU Basic.
- Use seeded deterministic runs for examples.
- Keep model outputs labelled as model-generated indices, educational simulations, calibration readiness, or evidence-priority analysis.

# Streamlit Deployment

Canonical Streamlit URL: https://gtpcnz.streamlit.app/

This is a public-data anchored benchmark and educational explainer. It is not linked-data calibrated and not a patient-level forecast. The dashboard surfaces the modelling views and links out to the Substack post sequence. It should not be used to claim precise fiscal savings, hospital-demand reductions, workforce effects, or implementation impacts.

GTPCNZ remains prepared for Streamlit Community Cloud as a compatibility surface. The future interactive dashboard target is the Dash Hugging Face Space documented in `docs/DASH-HUGGINGFACE-DEPLOYMENT.md`.

## Entrypoint

Use:

```text
streamlit_app.py
```

The root entrypoint imports and runs `models.primarycare_model.app.render_app`.

## Required Files

- `pyproject.toml` and `uv.lock` declare and lock Python dependencies.
- `.streamlit/config.toml` stores public app configuration.
- `.streamlit/secrets.toml.example` documents that no secrets are required.
- `models/tests/test_app.py` uses `streamlit.testing.v1.AppTest` for headless dashboard checks.

## Local Verification

```bash
uv sync --frozen --all-groups
uv run pytest -q models/tests/test_app.py tests/test_app.py
uv run streamlit run streamlit_app.py
```

## Community Cloud Settings

- Repository: `edithatogo/gtpcnz`
- Branch: `main`
- Main file path: `streamlit_app.py`
- Python version: `3.11`

## Caveat

The dashboard is a public-data anchored benchmark and educational explainer. It is not a linked-data calibrated or patient-level forecast.

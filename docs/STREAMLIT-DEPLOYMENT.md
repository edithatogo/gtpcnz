# Streamlit Deployment

GTPCNZ is prepared for Streamlit Community Cloud.

Public app URL:

<https://gtpcnz.streamlit.app/>

## Entrypoint

Use:

```text
streamlit_app.py
```

The root entrypoint imports and runs `models.primarycare_model.app.render_app`.

## Required Files

- `requirements.txt` declares Python dependencies.
- `.streamlit/config.toml` stores public app configuration.
- `.streamlit/secrets.toml.example` documents that no secrets are required.
- `models/tests/test_app.py` uses `streamlit.testing.v1.AppTest` for headless dashboard checks.

## Local Verification

```bash
pip install -r requirements.txt
pytest -q models/tests/test_app.py
streamlit run streamlit_app.py
```

## Community Cloud Settings

- Repository: `edithatogo/gtpcnz`
- Branch: `main`
- Main file path: `streamlit_app.py`
- Python version: `3.11`

## Caveat

The dashboard is an educational explainer. It is not a calibrated simulator or real-data calibrated policy forecast.

> This is a source-informed parameterised scaffold and educational explainer. It is not a real-data calibrated forecast and should not be used to claim precise fiscal savings, hospital-demand reductions, workforce effects, or implementation impacts.

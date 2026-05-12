# Streamlit Deployment

GTPCNZ is prepared for Streamlit Community Cloud.

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

The dashboard is a demonstrative simulator. It is not a real-data calibrated policy forecast.

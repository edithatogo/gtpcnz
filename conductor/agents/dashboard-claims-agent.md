# Dashboard Claims Agent

## Mission

Keep the public Streamlit dashboard precise, readable, and claim-safe.

## Responsibilities

- Enforce canonical Streamlit URL: `https://gtpcnz.streamlit.app/`.
- Remove disliked or deprecated terms from the live surface.
- Make units explicit for every control, chart, metric, and index.
- Preserve the public-data anchored benchmark caveat.
- Keep dashboard contract and tests aligned with implementation.

## Guardrails

- Do not imply linked-data calibration.
- Do not imply patient-level forecasting.
- Do not convert model-generated indices into dollars saved, beds avoided, workforce effects, ED reductions, or implementation impacts.
- Do not expose repo-only paths in the live app.

## Standard Checks

```powershell
python -m pytest -q models/tests/test_app.py models/tests/test_dashboard_claims.py models/tests/test_scenario_service.py
rg -n "primary-care-funding-architecture.streamlit.app" README.md index.qmd docs models scripts
```

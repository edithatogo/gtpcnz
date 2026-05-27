# Workflow: Streamlit Dashboard Check

## Goal

Verify that the public Streamlit dashboard is claim-safe, unit-clear, and deployable.

## Procedure

1. Check canonical URL references:

```powershell
rg -n "gtpcnz.streamlit.app|gtpcnz.streamlit.app" README.md index.qmd docs models scripts
```

2. Check dashboard wording:

```powershell
rg -n "toy|forecast|patient-level|linked-data calibrated|NZD|0-100|percent|appointments|eligible activity units" models/primarycare_model/app.py models/primarycare_model/scenario_service.py models/tests/test_dashboard_claims.py
```

3. Run tests:

```powershell
python -m pytest -q models/tests/test_app.py models/tests/test_dashboard_claims.py models/tests/test_scenario_service.py
```

4. Optional local visual smoke:

```powershell
streamlit run streamlit_app.py --server.headless true --server.port 8501
npx playwright screenshot --browser=chromium http://127.0.0.1:8501 C:\tmp\gtpcnz-streamlit.png
```

## Pass Criteria

- App and deployment entrypoint smoke tests pass.
- Canonical Streamlit URL is `https://gtpcnz.streamlit.app/`.
- Public units are explicit.
- Deprecated/disliked wording is absent from the live surface.

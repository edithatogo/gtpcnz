# Track Template: Streamlit Dashboard Surface Change

## Metadata

- Track ID: `<next-id>-streamlit-dashboard-<date>`
- Owner: `dashboard-claims-agent`
- Status: `pending`
- Scope: `streamlit_app.py`, `models/primarycare_model/app.py`, dashboard services, dashboard tests, public dashboard contract docs.

## Problem

The Streamlit surface is public-facing. Wording, units, claim boundaries, and URL references must stay precise and testable.

## Goals

- Keep the dashboard limited to GTPCNZ modelling, dashboard views, and links to Substack posts.
- Keep the canonical public Streamlit URL as `https://gtpcnz.streamlit.app/`.
- State units next to sliders, charts, metrics, and model-generated indices.
- Keep claim boundaries visible and test-enforced.

## Non-Goals

- Do not add private data.
- Do not introduce stronger predictive or linked-data claims.
- Do not change GitHub Pages content unless the track explicitly includes it.

## Required Checks

```powershell
python -m pytest -q models/tests/test_app.py models/tests/test_dashboard_claims.py models/tests/test_scenario_service.py
python -c "import ast, pathlib; [ast.parse(pathlib.Path(p).read_text(encoding='utf-8')) for p in ['streamlit_app.py','models/primarycare_model/app.py']]"
rg -n "primary-care-funding-architecture.streamlit.app|toy" models/primarycare_model/app.py models/primarycare_model/scenario_service.py models/tests/test_dashboard_claims.py
```

## Acceptance Criteria

- Streamlit app smoke tests pass.
- Dashboard claim tests pass.
- All public units are explicit: 0-100 indices, percentages, counts, months, seeds, NZD-like illustrative values, or labelled model-generated scores.
- Public copy does not use deprecated or disliked terms listed in the track.
- Canonical URL remains `https://gtpcnz.streamlit.app/`.

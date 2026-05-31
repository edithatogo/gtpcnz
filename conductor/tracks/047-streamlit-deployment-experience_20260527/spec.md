# Streamlit Deployment Experience

**Status:** Complete

## Problem

The Streamlit app already works as a public explainer, but it still reads like a competent dashboard rather than a fully polished public product. The deployment and UX layer needs sharper control labelling, stronger accessibility, and a cleaner release story.

## Goal

Improve the Streamlit surface so it is:

- easy for a general audience to browse;
- explicit about what is educational versus model-generated;
- stable under smoke tests;
- aligned with the canonical public URL and deployment docs;
- accessible enough that the charts and tables are not the only reading path.

## Current State

| Concern | Current locations | Gap |
|---|---|---|
| App entrypoint | `streamlit_app.py` | Works, but needs a more explicit deployment lifecycle story. |
| Main app | `models/primarycare_model/app.py` | Strong surface, but control labels and reading aids can still be tightened. |
| Smoke tests | `models/tests/test_app.py`, `models/tests/test_streamlit_post_labs.py` | Good coverage, but UI readability and interaction depth can still improve. |
| Deployment docs | `docs/STREAMLIT-DEPLOYMENT.md`, `docs/public-site/streamlit-dashboard-contract-v1.8.1.md` | Good contract, but not yet a full release/ops story. |
| Accessibility | App charts and tables | Needs better text summaries and keyboard-first affordances. |

## Target State

- the app is obviously public-explainer first, not forecast-first;
- the app’s controls, tabs, and charts are easier to navigate;
- accessibility summaries appear alongside the main visual elements;
- deployment docs and tests match the actual public surface;
- canonical URL handling stays stable.

## Acceptance Criteria

- `streamlit_app.py` still launches the app cleanly;
- smoke tests pass;
- the dashboard contract remains in sync with the actual app;
- the public URL stays canonical;
- the app exposes enough text description that the figures are not the only route through the content.

## Non-Goals

- Do not add private data or a stronger empirical claim.
- Do not rewrite the model logic just to change the UI.
- Do not remove the current public caveat.

## Verification

```powershell
python -m pytest -q models/tests/test_app.py models/tests/test_dashboard_claims.py models/tests/test_streamlit_post_labs.py
python -c "from streamlit_app import render_app"
rg -n \"gtpcnz.streamlit.app|Educational explainer|Public-data anchored benchmark|What the educational sliders are for|How to read this dashboard\" streamlit_app.py models/primarycare_model/app.py docs
```
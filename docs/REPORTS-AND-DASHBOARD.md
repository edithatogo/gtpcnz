# GTPCNZ Interactive Reporting & Visualization Suite

Canonical Streamlit URL: https://gtpcnz.streamlit.app/

This is a public-data anchored benchmark and educational explainer. It is not linked-data calibrated and not a patient-level forecast. The Streamlit surface now focuses on the modelling and dashboard views, then links readers to the Substack posts. It should not be used to claim precise fiscal savings, hospital-demand reductions, workforce effects, or implementation impacts.

This project includes a reproducible reporting layer and an interactive dashboard designed to make the primary care funding model accessible to both policy experts and non-specialist readers.

The GitHub Pages site now also has a canonical site map and release manifest at `docs/public-site/site-map-and-release-manifest-v1.8.4.md` so the public bundle has one explicit index.

## 1. Quarto Report: `reports/primary_care_architecture.qmd`

The Quarto report is a reproducible document that combines technical thesis writing with live Python data analysis.

### How to Render
To generate the HTML or PDF version, ensure you have [Quarto](https://quarto.org/) installed and run:

```bash
quarto render reports/primary_care_architecture.qmd
```

### Design Philosophy
- **Narrative first:** Explains the "Game Theory" of healthcare using relatable metaphors (e.g., video games, subscription services).
- **Traceable model outputs:** Pulls directly from `outputs/full-parameterised-summary-results-v1.7.0.csv`.

## 2. Streamlit Dashboard: `streamlit_app.py`

**GTPCNZ** is a public-data anchored benchmark and dashboard for comparing funding architecture scenarios and reading paths.

### How to Run
Ensure you have the dependencies installed:

```bash
uv sync --frozen --all-groups
```

Then launch the dashboard:

```bash
uv run streamlit run streamlit_app.py
```

### Features
- **Interactive Sliders:** Adjust Capitation vs. FFS weights.
- **Educational Tooltips:** Instant definitions for complex healthcare terms.
- **Real-time Plotting:** Shows qualitative changes in model-generated supply and hospital-pressure index values.
- **Deployment-ready Entry Point:** `streamlit_app.py` is the Streamlit Community Cloud entrypoint.

## Technical Standards
- **Modularity:** The dashboard leverages the existing project data structure.
- **Accessibility:** Content is simplified without losing technical rigor.
- **Transparency:** All visualisations are generated from traceable project outputs.
- **Automated Testing:** `models/tests/test_app.py` uses Streamlit's native `AppTest` API.

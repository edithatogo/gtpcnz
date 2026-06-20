# GTPCNZ Interactive Reporting & Visualization Suite

Canonical GitHub Pages front door: https://edithatogo.github.io/gtpcnz/

Hugging Face interactive lab: https://edithatogo-gtpcnz-dashboard.hf.space/

Legacy Streamlit compatibility URL: https://gtpcnz.streamlit.app/

This is a public-data anchored benchmark and educational explainer. It is not linked-data calibrated and not a patient-level forecast. The Dash lab is the canonical interactive surface; the Streamlit app is retained only for legacy compatibility while the migration is checked. It should not be used to claim precise fiscal savings, ED reductions, hospital-demand reductions, workforce effects, implementation impacts, or causal effects.

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

## 2. Dash model lab: `dash_app/app.py`

The future interactive dashboard target is a Plotly Dash app deployed to Hugging Face Spaces. GitHub Pages remains the polished public front door.

### How to Run

Use the repo-local Prefix.dev Pixi wrapper:

```bash
python scripts/bootstrap_prefix_pixi.py
python scripts/run_pixi.py run dash
```

If the bare `pixi` command resolves to another executable, keep using the wrapper:

```bash
python scripts/run_pixi.py --version
```

### Features

- Scenario comparison with Plotly charts, table fallback, interpretation, and CSV download.
- Bounded uncertainty, stock-flow, agent-lens, and educational simulation views.
- Public caveat strip and GitHub/Hugging Face topology links, with Streamlit labelled as legacy compatibility where shown.
- Hugging Face Space packaging under `dash_app/`.

## 3. Streamlit compatibility dashboard: `streamlit_app.py`

**GTPCNZ** retains this Streamlit app as a legacy compatibility surface for comparing migration parity against the Dash lab.

### How to Run
Ensure the repo-local Pixi runtime is installed:

```bash
python scripts/bootstrap_prefix_pixi.py
```

Then launch the dashboard:

```bash
python scripts/run_pixi.py run -e dev streamlit run streamlit_app.py
```

### Features
- **Interactive Sliders:** Adjust Capitation vs. FFS weights.
- **Educational Tooltips:** Instant definitions for complex healthcare terms.
- **Real-time Plotting:** Shows qualitative changes in model-generated supply and hospital-pressure index values.
- **Compatibility Entry Point:** `streamlit_app.py` remains the Streamlit Community Cloud entrypoint only while the Dash migration is checked.

## Technical Standards
- **Modularity:** The dashboard leverages the existing project data structure.
- **Accessibility:** Content is simplified without losing technical rigor.
- **Transparency:** All visualisations are generated from traceable project outputs.
- **Automated Testing:** `models/tests/test_app.py` uses Streamlit's native `AppTest` API; `models/tests/test_dash_app.py` covers the Dash shell.

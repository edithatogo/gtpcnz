# Interactive Reporting & Visualization Suite

This project includes a state-of-the-art (SOTA) reporting layer and an interactive dashboard to make the primary care funding model accessible to both policy experts and citizens (calibrated for a 14-year-old audience).

## 1. Quarto Report: `reports/primary_care_architecture.qmd`

The Quarto report is a reproducible document that combines technical thesis writing with live Python data analysis.

### How to Render
To generate the HTML or PDF version, ensure you have [Quarto](https://quarto.org/) installed and run:

```bash
quarto render reports/primary_care_architecture.qmd
```

### Design Philosophy
- **Narrative first:** Explains the "Game Theory" of healthcare using relatable metaphors (e.g., video games, subscription services).
- **Embedded Evidence:** Pulls directly from `outputs/full-parameterised-summary-results-v1.7.0.csv`.

## 2. Streamlit Dashboard: `models/primarycare_model/app.py`

**"Primary Care Pulse"** is an interactive tool allowing users to simulate the impact of different funding rules.

### How to Run
Ensure you have the dependencies installed:

```bash
pip install streamlit pandas matplotlib
```

Then launch the dashboard:

```bash
streamlit run models/primarycare_model/app.py
```

### Features
- **Interactive Sliders:** Adjust Capitation vs. FFS weights.
- **Educational Tooltips:** Instant definitions for complex healthcare terms.
- **Real-time Plotting:** Immediate feedback on how your settings impact "Doctor Supply" and "Hospital Pressure".

## Technical Standards (SOTA)
- **Modularity:** The dashboard leverages the existing project data structure.
- **Accessibility:** Content is simplified without losing technical rigor.
- **Transparency:** All visualisations are generated from traceable project outputs.

# GTPCNZ reports and dashboard

GTPCNZ has two public reading surfaces: a Quarto report and a Streamlit dashboard.

## Public report

`reports/primary_care_architecture.qmd` explains the funding architecture model. Read it with:

- `docs/calibration/model-card-v1.7.2.md`
- `docs/launch/claim-boundaries-v1.7.2.md`
- `docs/public-site/streamlit-dashboard-contract-v1.8.1.md`
- `docs/public-site/streamlit-dashboard-audit-v1.8.1.md`
- `docs/public-site/evidence-tracker-public-v1.8.1.md`
- `docs/public-site/calibration-readiness-page-v1.8.1.md`

## Streamlit dashboard

Public URL:

<https://gtpcnz.streamlit.app/>

Entrypoint:

```bash
streamlit run streamlit_app.py
```

The dashboard is an **interactive explainer**, not a calibrated simulator. It keeps two kinds of output separate:

1. **Reference scenarios** loaded from `outputs/full-parameterised-summary-results-v1.7.0.csv`.
2. **Toy explainer slider scores** from a simple teaching formula.

Do not describe the toy slider outputs as forecasts.

## Public claim boundary

Use this wording:

> This is a source-informed parameterised scaffold and educational explainer. It is not a real-data calibrated forecast and should not be used to claim precise fiscal savings, hospital-demand reductions, workforce effects, or implementation impacts.

## Plain-language phrase

> Uncapped does not mean uncontrolled; it means scheduled, rules-based, audited, clinically governed and place-accountable.

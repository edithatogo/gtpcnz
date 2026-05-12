# GTPCNZ reports and dashboard

GTPCNZ includes a Quarto public report and a Streamlit dashboard.

## Public report

`reports/primary_care_architecture.qmd` is the public-facing explanation of the funding architecture model. It should be read alongside:

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

The dashboard is an **interactive explainer**, not a calibrated simulator. It has two different types of output:

1. **Reference scenarios** loaded from `outputs/full-parameterised-summary-results-v1.7.0.csv`.
2. **Toy explainer slider scores** generated from a simple educational formula.

Do not describe the toy slider outputs as forecasts.

## Public claim boundary

Use this wording:

> This is a source-informed parameterised scaffold and educational explainer. It is not a real-data calibrated forecast and should not be used to claim precise fiscal savings, hospital-demand reductions, workforce effects, or implementation impacts.

## Key phrase

> Uncapped does not mean uncontrolled; it means scheduled, rules-based, audited, clinically governed and place-accountable.

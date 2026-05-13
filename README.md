# GTPCNZ

[![CI](https://github.com/edithatogo/gtpcnz/actions/workflows/ci.yml/badge.svg)](https://github.com/edithatogo/gtpcnz/actions/workflows/ci.yml)
[![Quarto Pages](https://github.com/edithatogo/gtpcnz/actions/workflows/pages.yml/badge.svg)](https://github.com/edithatogo/gtpcnz/actions/workflows/pages.yml)

GTPCNZ is a public policy-research package about primary care funding in Aotearoa New Zealand, with comparative material for Australia.

Website: https://edithatogo.github.io/gtpcnz/

## What this is

- A source-informed model scaffold for exploring primary care funding architecture.
- A Quarto website and reproducible report.
- A Streamlit dashboard for interactive explanation of scenario logic.
- A public audit trail of assumptions, caveats, and launch materials.

## What this is not

- It is not an endorsed policy position.
- It is not a real-data calibrated forecasting model.
- It should not be used to claim precise fiscal savings, hospital-demand reductions, workforce effects, or implementation impacts.

## Current thesis

The thesis is specific: keep capitation for continuity, enrolment, baseline viability, and population responsibility. Add an uncapped, scheduled, rules-based fee-for-service stream for eligible primary medical activity, controlled through item rules, provider scope, clinical governance, documentation, audit, co-payment protections, and place-based accountability.

Short version:

> Uncapped does not mean uncontrolled.

## Public pages

- Quarto website: https://edithatogo.github.io/gtpcnz/
- Interactive explainer (Streamlit): https://gtpcnz.streamlit.app/
- Quarto source report: `reports/primary_care_architecture.qmd`
- Streamlit dashboard entrypoint: `streamlit_app.py`
- Dashboard implementation: `models/primarycare_model/app.py`
- Model card: `docs/calibration/model-card-v1.7.2.md`
- Claim boundaries: `docs/launch/claim-boundaries-v1.7.2.md`
- Evidence tracker: `docs/public-site/evidence-tracker-public-v1.8.1.md`
- Calibration readiness: `docs/public-site/calibration-readiness-page-v1.8.1.md`

## Run locally

Install dependencies:

```bash
pip install -r requirements.txt
```

Run tests:

```bash
pytest -q
```

Render the Quarto website:

```bash
quarto render --to html
```

Run the Streamlit dashboard:

```bash
streamlit run streamlit_app.py
```

## Deploy

GitHub Pages is deployed from `.github/workflows/pages.yml`.

Streamlit Community Cloud can deploy this app with:

- Repository: `edithatogo/gtpcnz`
- Branch: `main`
- Entrypoint: `streamlit_app.py`

## License and citation

See `LICENSE` for the mixed code/content licensing terms and `CITATION.cff` for citation metadata.

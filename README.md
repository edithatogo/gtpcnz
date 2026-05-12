# GTPCNZ

[![CI](https://github.com/edithatogo/gtpcnz/actions/workflows/ci.yml/badge.svg)](https://github.com/edithatogo/gtpcnz/actions/workflows/ci.yml)
[![Quarto Pages](https://github.com/edithatogo/gtpcnz/actions/workflows/pages.yml/badge.svg)](https://github.com/edithatogo/gtpcnz/actions/workflows/pages.yml)

GTPCNZ is a public policy-research and translation package on primary care funding architecture in Aotearoa New Zealand and Australia.

Website: https://edithatogo.github.io/gtpcnz/

## What This Is

- A source-informed model scaffold for exploring primary care funding architecture.
- A Quarto website and reproducible report.
- A Streamlit dashboard for interactive scenario exploration.
- A public audit trail of assumptions, caveats, and launch materials.

## What This Is Not

- It is not an endorsed policy position.
- It is not a real-data calibrated forecasting model.
- It should not be used to claim precise fiscal savings, hospital-demand reductions, or workforce effects.

## Current Thesis

Capitation should be retained for continuity, enrolment, baseline viability, and population responsibility. Eligible primary medical activity should also have an uncapped, scheduled, rules-based fee-for-service stream, controlled through item rules, provider scope, clinical governance, documentation, audit, co-payment protections, and place-based accountability.

Short version:

> Uncapped does not mean uncontrolled.

## Public Surfaces

- Quarto website: https://edithatogo.github.io/gtpcnz/
- Quarto source report: `reports/primary_care_architecture.qmd`
- Streamlit dashboard entrypoint: `streamlit_app.py`
- Dashboard implementation: `models/primarycare_model/app.py`
- Model card: `docs/calibration/model-card-v1.7.2.md`
- Claim boundaries: `docs/launch/claim-boundaries-v1.7.2.md`

## Run Locally

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

## License And Citation

See `LICENSE` for the mixed code/content licensing terms and `CITATION.cff` for citation metadata.

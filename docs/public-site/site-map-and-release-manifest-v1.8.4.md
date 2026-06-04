# Site map and release manifest v1.8.4

Canonical index for the GTPCNZ GitHub Pages site.

This page is the single place to check what the public site contains, how it is
rendered, and what it is for. It complements the homepage by making the public
release bundle explicit instead of leaving readers to infer the structure from
multiple companion docs.

## Public surfaces

| Surface | File | Purpose |
|---|---|---|
| Home | `index.qmd` | Front door, reading map, and public caveat |
| Public report | `reports/primary_care_architecture.qmd` | Static Quarto report and argument map |
| Dashboard guide | `docs/REPORTS-AND-DASHBOARD.md` | How the report and dashboard fit together |
| Deployment guide | `docs/STREAMLIT-DEPLOYMENT.md` | Streamlit deployment and public boundary notes |
| Model card | `docs/calibration/model-card-v1.7.2.md` | Model scope, evidence tiers, and claim boundaries |
| Claim boundaries | `docs/launch/claim-boundaries-v1.7.2.md` | Public-data versus linked-data boundary |
| Evidence tracker | `docs/public-site/evidence-tracker-public-v1.8.1.md` | OIA and calibration readiness tracker |
| Calibration readiness | `docs/public-site/calibration-readiness-page-v1.8.1.md` | Data gaps and validation pathway |
| Dashboard contract | `docs/public-site/streamlit-dashboard-contract-v1.8.1.md` | Required dashboard surfaces and wording |
| Dashboard audit | `docs/public-site/streamlit-dashboard-audit-v1.8.1.md` | Pass/fail audit for the dashboard contract |
| Post crosswalk | `docs/public-site/post-surface-crosswalk-contract-v1.8.2.md` | Links posts to public surfaces |
| Visual gallery contract | `docs/public-site/visual-gallery-contract-v1.8.4.md` | Required figures, tables, and diagrams |
| Public wording contract | `docs/public-site/public-wording-contract-v1.8.4.md` | Canonical public phrasing |
| What is calculated now | `docs/public-site/what-is-calculated-now.md` | Plain-English explanation of benchmark modes |

## Release rules

1. `quarto render` must succeed before Pages deployment.
2. `github-pages` deployment uses `.github/workflows/pages.yml`.
3. `public/gtpcnz` is a mirror for deployment-critical root files, not the site source.
4. Public wording must stay aligned with the benchmark boundary: public-data anchored by default, empirically supported where valid, and never a patient-level forecast.

## Canonical checks

- `python scripts/check_repo_health.py`
- `python scripts/check_concern_boundaries.py`
- `python scripts/check_no_patient_data.py`
- `quarto render --to html`


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
| Dash/Hugging Face deployment guide | `docs/DASH-HUGGINGFACE-DEPLOYMENT.md` | Dash Space deployment, Pixi runtime, and public topology |
| Streamlit deployment guide | `docs/STREAMLIT-DEPLOYMENT.md` | Streamlit compatibility deployment and public boundary notes |
| Release model card | `docs/release/model-card-v1.8.1.md` | Generated release model card with aggregate validation status and claim boundaries |
| Release manifest | `docs/release/release-manifest-v1.8.1.json` | Generated release hashes, validation status, and not-valid-for warnings |
| Track 071 regeneration evidence | `docs/release/track-071-release-regeneration-v1.md` | Commands, outputs, hashes, Quarto render proof, and blockers |
| Historical model card | `docs/calibration/model-card-v1.7.2.md` | Earlier model scope, evidence tiers, and claim boundaries |
| Claim boundaries | `docs/launch/claim-boundaries-v1.7.2.md` | Public-data versus linked-data boundary |
| Evidence tracker | `docs/public-site/evidence-tracker-public-v1.8.1.md` | OIA and calibration readiness tracker |
| Calibration readiness | `docs/public-site/calibration-readiness-page-v1.8.1.md` | Data gaps and validation pathway |
| Dashboard contract | `docs/public-site/streamlit-dashboard-contract-v1.8.1.md` | Required dashboard surfaces and wording; Streamlit remains compatibility during Dash migration |
| Dashboard audit | `docs/public-site/streamlit-dashboard-audit-v1.8.1.md` | Pass/fail audit for the dashboard contract |
| Post crosswalk | `docs/public-site/post-surface-crosswalk-contract-v1.8.2.md` | Links posts to public surfaces |
| Visual gallery contract | `docs/public-site/visual-gallery-contract-v1.8.4.md` | Required figures, tables, and diagrams |
| Public wording contract | `docs/public-site/public-wording-contract-v1.8.4.md` | Canonical public phrasing |
| What is calculated now | `docs/public-site/what-is-calculated-now.md` | Plain-English explanation of benchmark modes |

## Release rules

1. `quarto render` must succeed before Pages deployment.
2. `github-pages` deployment uses `.github/workflows/pages.yml`.
3. The Dash/Hugging Face deployment uses `.github/workflows/huggingface-space.yml`.
4. `public/gtpcnz` is a mirror for deployment-critical root files, not the site source.
5. Public wording must stay aligned with the benchmark boundary: public-data anchored by default, empirically supported where aggregate gates pass, and never a patient-level forecast.
6. Aggregate validation status is `public_aggregate_validated` only for registered public aggregate validation gates; it does not authorize precise fiscal, ED, hospital-demand, workforce, implementation-impact, or causal effects.

## Canonical checks

- `python scripts/check_repo_health.py`
- `python scripts/check_concern_boundaries.py`
- `python scripts/check_no_patient_data.py`
- `python scripts/generate_release_model_card.py --check-only`
- `python scripts/generate_release_manifest.py --check-only`
- `python -m pytest -q models/tests/test_dashboard_service.py models/tests/test_dash_app.py`
- `quarto render --to html`


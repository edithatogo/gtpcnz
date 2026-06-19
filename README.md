# GTPCNZ

[![CI](https://github.com/edithatogo/gtpcnz/actions/workflows/ci.yml/badge.svg)](https://github.com/edithatogo/gtpcnz/actions/workflows/ci.yml)
[![Quarto Pages](https://github.com/edithatogo/gtpcnz/actions/workflows/pages.yml/badge.svg)](https://github.com/edithatogo/gtpcnz/actions/workflows/pages.yml)

GTPCNZ is a public policy-research and translation package on primary care funding architecture in Aotearoa New Zealand and Australia.

Repository: https://github.com/edithatogo/gtpcnz

Website: https://edithatogo.github.io/gtpcnz/

Substack series: https://rareinsights.substack.com/

## What This Is

- A public-data anchored benchmark for exploring primary care funding architecture.
- A Quarto website and reproducible report.
- A Plotly Dash interactive model lab for Hugging Face Spaces, with Streamlit retained as a compatibility surface during migration.
- A public audit trail of assumptions, caveats, and launch materials.

## What This Is Not

- It is not an endorsed policy position.
- It is a public-data anchored benchmark, not a linked-data calibrated or patient-level forecast.
- In repo-health terms, the aggregate validation lane is `public_aggregate_validated` / `empirically_supported_if_gated`, and remains bounded by the documented claim boundaries.
- It should not be used to claim precise fiscal savings, ED reductions, hospital-demand reductions, workforce effects, implementation impacts, or causal effects.
- Full caveat: This is a public-data anchored benchmark and educational explainer. It is not linked-data calibrated and not a patient-level forecast. It should not be used to claim precise fiscal savings, ED reductions, hospital-demand reductions, workforce effects, implementation impacts, or causal effects.

## Design Option Explored Here

The design option explored here retains capitation for continuity, enrolment, baseline viability, and population responsibility. It also tests an uncapped, scheduled, rules-based fee-for-service stream for eligible primary medical activity, controlled through item rules, provider scope, clinical governance, documentation, audit, co-payment protections, and place-based accountability.

Short version:

> Uncapped does not mean uncontrolled.

## Public Surfaces

- Quarto website: https://edithatogo.github.io/gtpcnz/
- Hugging Face interactive model lab: https://edithatogo-gtpcnz-dashboard.hf.space/
- Streamlit compatibility dashboard and modelling views: https://gtpcnz.streamlit.app/
- Substack series: https://rareinsights.substack.com/
- Quarto source report: [reports/primary_care_architecture.qmd](reports/primary_care_architecture.qmd)
- Dash app entrypoint: [dash_app/app.py](dash_app/app.py)
- Streamlit dashboard entrypoint: [streamlit_app.py](streamlit_app.py)
- Dashboard implementation: [models/primarycare_model/app.py](models/primarycare_model/app.py)
- Framework-neutral dashboard service: [models/primarycare_model/dashboard_service.py](models/primarycare_model/dashboard_service.py)
- Current release model card: [docs/release/model-card-v1.8.1.md](docs/release/model-card-v1.8.1.md)
- Historical v1.7.2 model card: [docs/calibration/model-card-v1.7.2.md](docs/calibration/model-card-v1.7.2.md)
- Claim boundaries: [docs/launch/claim-boundaries-v1.7.2.md](docs/launch/claim-boundaries-v1.7.2.md)
- Evidence tracker: [docs/public-site/evidence-tracker-public-v1.8.1.md](docs/public-site/evidence-tracker-public-v1.8.1.md)
- Calibration readiness: [docs/public-site/calibration-readiness-page-v1.8.1.md](docs/public-site/calibration-readiness-page-v1.8.1.md)
- MoSCoW requirements: [docs/requirements-moscow-v1.8.3.md](docs/requirements-moscow-v1.8.3.md)
- Architecture/design diagrams: [docs/design/repo-github-streamlit-design-v1.8.3.md](docs/design/repo-github-streamlit-design-v1.8.3.md)
- Repo/GitHub/Streamlit contracts: [docs/contracts/repo-github-streamlit-contracts-v1.8.3.md](docs/contracts/repo-github-streamlit-contracts-v1.8.3.md)
- Dependency policy: [docs/dependency-policy-v1.8.3.md](docs/dependency-policy-v1.8.3.md)
- Experimental edge lane: [.github/workflows/dependency-edge.yml](.github/workflows/dependency-edge.yml), resolved through the uv dependency graph in [pyproject.toml](pyproject.toml)
- Bleeding-edge scorecard: [docs/bleeding-edge-scorecard-v1.0.md](docs/bleeding-edge-scorecard-v1.0.md)
- Release-note handling: [docs/release/bleeding-edge-sota-release-handling.md](docs/release/bleeding-edge-sota-release-handling.md)
- Edge triage note: [docs/operations/dependency-edge-triage-v1.0.md](docs/operations/dependency-edge-triage-v1.0.md)
- GitHub Actions recovery runbook: [docs/operations/github-actions-recovery-v1.8.3.md](docs/operations/github-actions-recovery-v1.8.3.md)

## Run Locally

Install dependencies:

```bash
uv sync --frozen --all-groups
```

Run tests:

```bash
uv run pytest -q
```

Check the auditable repo-health score:

```bash
uv run python scripts/check_repo_health.py
```

Render the Quarto website:

```bash
quarto render --to html
```

Run the Streamlit dashboard:

```bash
uv run streamlit run streamlit_app.py
```

Run the Dash model lab:

```bash
pixi run dash
```

If the local `pixi` executable is not Prefix.dev Pixi, use the existing uv environment for local checks until the correct Pixi binary is installed:

```bash
uv run python -m dash_app.app
```

## Deploy

GitHub Pages is deployed from `.github/workflows/pages.yml` and remains the public front door.

The Hugging Face Dash Space is deployed from `.github/workflows/huggingface-space.yml` to:

- Space: `edithatogo/gtpcnz-dashboard`
- URL: https://edithatogo-gtpcnz-dashboard.hf.space/
- Runtime: Prefix.dev Pixi via Docker

Streamlit Community Cloud can deploy this app with:

- Repository: `edithatogo/gtpcnz`
- Branch: `main`
- Entrypoint: `streamlit_app.py`

If GitHub Actions jobs fail before a runner starts, use `docs/operations/github-actions-recovery-v1.8.3.md` before changing workflow code.

## License And Citation

See `LICENSE` for the mixed code/content licensing terms and `CITATION.cff` for citation metadata.


## Public calibrated-model programme

The current public runtime remains a public-data anchored benchmark and educational explainer. The public aggregate lane now reports `public_aggregate_validated` / `empirically_supported_if_gated` for registered aggregate gates only. The programme separates public registries, source snapshots, calibration targets, structural uncertainty, VOI, cockpit, and release gates from future/private templates. Unsupported precision and causal claims remain out of bounds: precise fiscal savings, ED reductions, hospital-demand reductions, workforce effects, implementation impacts, and causal effects.

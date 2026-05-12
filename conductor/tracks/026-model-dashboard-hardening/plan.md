# Track 026 — implementation plan

## Step 1 — Model-service layer

Add `models/primarycare_model/scenario_service.py` with schema validation, expected scenario IDs, reference scenario loading, toy setting scoring and calibration-readiness helpers.

## Step 2 — Dashboard hardening

Replace `models/primarycare_model/app.py` so the app:

- calls itself an explainer;
- separates reference scenarios from toy scores;
- includes model status and claim-boundary text;
- includes evidence/OIA and calibration-readiness tabs;
- avoids forecast language.

## Step 3 — Public site hardening

Update `_quarto.yml`, `index.qmd`, and `reports/primary_care_architecture.qmd` so the public site renders the relevant model-card, claim-boundary, evidence and calibration-readiness pages.

## Step 4 — Evidence tracker

Add `docs/audit/oia-request-tracker.csv` and `data/evidence/oia_request_tracker.csv` as default public tracker inputs.

## Step 5 — Tests

Add tests for:

- scenario schema;
- toy scoring range;
- dashboard caveat language;
- Quarto render targets;
- weak-control scenario gaming-risk ordering.

## Step 6 — Validation

Run:

```bash
python -m compileall models
pytest -q
quarto render --to html
python -m py_compile streamlit_app.py models/primarycare_model/app.py models/primarycare_model/scenario_service.py
```

## Step 7 — Commit

Use commit message:

```text
feat(site): harden model dashboard and public report v1.8.1
```

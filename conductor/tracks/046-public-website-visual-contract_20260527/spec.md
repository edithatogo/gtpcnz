# Public Website and Visual Contract

## Problem

The public website layer is useful, but it is spread across the homepage, the Quarto report, several docs, and a mirrored `public/gtpcnz` bundle. The reader can follow the story, but the site still needs a cleaner governing contract for visuals, tables, and public wording.

## Goal

Create a stable public-site contract that:

- keeps the homepage useful for a general audience;
- makes the visual gallery and reading map explicit;
- keeps the report, docs, and mirrored public bundle aligned;
- preserves the claim boundary consistently across all public surfaces;
- makes visual and table intent easy to scan.

## Current State

| Concern | Current locations | Gap |
|---|---|---|
| Homepage reading map | `index.qmd` | Strong start, but should be governed by a clearer release contract. |
| Quarto report | `reports/primary_care_architecture.qmd` | Good narrative structure, but needs stronger surface-level release governance. |
| Dashboard/report docs | `docs/REPORTS-AND-DASHBOARD.md`, `docs/STREAMLIT-DEPLOYMENT.md` | Clear, but split across multiple documents. |
| Public visual spec | `docs/public-site/*.md` | Useful, but still a collection of companion docs rather than a single contract spine. |
| Mirrored public bundle | `public/gtpcnz/` | Helpful for review, but easy to drift from the root source of truth. |

## Target State

- the public homepage and report speak with one voice;
- the visual gallery and table inventory are easy to scan;
- root and mirrored public content stay in sync;
- visuals and tables are labelled plainly enough for a general audience;
- the site makes it obvious what is educational, what is model-generated, and what is readiness material.

## Acceptance Criteria

- the main public surfaces remain readable without repo context;
- the report and homepage preserve the same caveat and reading order;
- the visual contract is consistent across `index.qmd`, `reports/primary_care_architecture.qmd`, and `docs/public-site/*`;
- no public surface silently reintroduces stale claim-boundary wording;
- mirrored public content can be regenerated from the root sources.

## Non-Goals

- Do not add stronger empirical claims.
- Do not change the dashboard model logic unless the contract needs it.
- Do not make the site more decorative at the expense of clarity.

## Verification

```powershell
python -m pytest -q models/tests/test_public_site_visual_contract.py models/tests/test_dashboard_claims.py models/tests/test_streamlit_post_labs.py
rg -n \"Visual reading map|GTPCNZ visual gallery|Public report|Streamlit dashboard|Model card and tracker|Calibration readiness|Uncapped does not mean uncontrolled\" index.qmd reports/primary_care_architecture.qmd docs public/gtpcnz
```

# Specification: Public Dashboard Deployment and Release Polish

**Track ID:** 027-public-dashboard-deployment_20260512
**Type:** Feature
**Created:** 2026-05-12
**Status:** Complete

## Summary

Complete the remaining public-release polish after the GTPCNZ GitHub Pages and Streamlit hardening pass. This track turns the follow-on recommendations into an auditable delivery path: deploy the Streamlit app publicly, add visual proof to the repository and site, control repository growth, and add a formal validation page before any stronger policy claims are made.

## Context

The repository is now public at `edithatogo/gtpcnz`, GitHub Pages is live, CI and Pages workflows pass, and the Streamlit app has a Community Cloud-ready root entrypoint. The remaining gap is not basic setup; it is public-facing release maturity.

The model remains a public-data anchored benchmark, not a linked-data calibrated or patient-level forecast. This track must preserve that boundary.

## User Story

As a public reader, reviewer, or policy stakeholder, I want the website, dashboard, and repository to be easy to inspect and clearly caveated so that I can understand the model without mistaking it for validated policy evidence.

## Acceptance Criteria

- [x] **Streamlit Public Deployment:** Streamlit Community Cloud app is deployed from `edithatogo/gtpcnz`, branch `main`, entrypoint `streamlit_app.py`.
- [x] **Stable Dashboard URL:** A memorable Streamlit subdomain is configured if available, preferably `https://gtpcnz.streamlit.app/`.
- [x] **README Visual Proof:** README includes current GitHub Pages and Streamlit screenshots or a short GIF.
- [x] **Website Visual Proof:** Quarto site includes a dashboard preview and direct Streamlit launch link.
- [x] **Repository Size Audit:** Large/generated outputs are reviewed and a decision is recorded on keeping in Git, moving to releases, or using Git LFS.
- [x] **Validation Page:** A formal model-validation page exists before any stronger policy claims are added.
- [x] **Claim Boundary Preserved:** All new public surfaces repeat that the model is a public-data anchored benchmark and not a linked-data calibrated or patient-level forecast.
- [x] **Quality Gates:** CI and Pages pass after all changes.

## Dependencies

- Existing public GitHub repository: `https://github.com/edithatogo/gtpcnz`
- Existing GitHub Pages site: `https://edithatogo.github.io/gtpcnz/`
- Existing Streamlit entrypoint: `streamlit_app.py`
- Streamlit Community Cloud access for deployment.

## Out of Scope

- Adding real-data empirical calibration.
- Publishing stronger fiscal, workforce, or hospital-demand effect estimates.
- Changing the core v1.7.2 policy thesis.
- Live Substack publication.

## Technical Notes

- Keep Streamlit deployment configuration at the repo root.
- Continue using `streamlit.testing.v1.AppTest` for headless tests.
- Prefer lightweight screenshots or compressed GIFs; do not commit large media without the repository size audit.
- If large artifacts are needed, prefer GitHub Releases or Git LFS rather than ordinary Git blobs.

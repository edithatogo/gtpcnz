# Track 026 — model and dashboard hardening spec

## Problem

The deployed site is a useful public demo, but the Streamlit app and Quarto report need to better reflect the model's real status and avoid overclaiming. The dashboard currently risks implying that sliders rerun the full model. The public site does not yet render enough of the model card, claim boundaries, evidence tracker or calibration-readiness material.

## Goal

Make the public model/dashboard layer safe, credible and useful without expanding the Substack layer.

## In scope

- Add a scenario-service module.
- Distinguish reference scenarios from toy explainer scores.
- Rename dashboard as an explainer.
- Add evidence/OIA and calibration-readiness public pages.
- Expand Quarto public report.
- Add source-confidence labels and claim-boundary wording.
- Add tests.

## Out of scope

- Substack series edits.
- Real-data calibration.
- New policy claims.
- Government implementation business case.

## Acceptance criteria

1. Dashboard first screen says it is not a real-data calibrated forecast.
2. Sliders are labelled toy/explainer levers.
3. Reference scenario charts use model-generated index wording.
4. Quarto renders model card, claim boundaries, evidence tracker and calibration-readiness pages.
5. Tests pass.

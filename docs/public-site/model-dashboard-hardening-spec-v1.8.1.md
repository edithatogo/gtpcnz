# Model and dashboard hardening spec v1.8.1

## Purpose

Make the GTPCNZ public dashboard and GitHub Pages site clear about what the model can and cannot do.

## Required changes

1. Present the dashboard as an **explainer**, not a forecast simulator.
2. Separate reference scenario outputs from toy slider scores.
3. Render model card and claim boundaries on GitHub Pages.
4. Render evidence tracker and calibration-readiness pages.
5. Rewrite the public report so the current reform pathway is the comparator.
6. Add source-confidence labels to the public report sections.
7. Add tests that enforce the caveat: source-informed scaffold, not a real-data calibrated forecast.

## Acceptance criteria

- The dashboard warning appears on first load.
- The sliders are described as toy/explainer levers.
- Reference scenario charts are labelled as model-generated indices.
- The public report says results are not observed outcomes.
- Quarto renders model card, claim boundaries, evidence tracker and calibration-readiness pages.
- Tests pass.

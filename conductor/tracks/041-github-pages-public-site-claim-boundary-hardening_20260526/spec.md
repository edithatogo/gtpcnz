# GitHub Pages Public Site Claim-Boundary Hardening

## Problem

The live GTPCNZ GitHub Pages site still used older public wording: source-informed scaffold, not a real-data calibrated forecast. That wording was also enforced by local tests, which made the stale contract durable.

## Goal

Update the public site, dashboard copy, documentation contracts and tests to use the current public boundary:

> This is a public-data anchored benchmark and educational explainer. It is not linked-data calibrated and not a patient-level forecast. It should not be used to claim precise fiscal savings, hospital-demand reductions, workforce effects, or implementation impacts.

## Owned Files

- `public/gtpcnz` public website, dashboard source and public tests.
- This Conductor track directory and the parent `conductor/tracks.md` registry entry.

## Requirements

- Replace first-screen and contract-level old caveats with the canonical caveat.
- Remove public-facing `source-informed scaffold` and `not a real-data calibrated forecast` language from public source surfaces.
- Preserve weaker-but-accurate language such as model-generated index, demonstrative explainer, not linked-data calibrated, and not a patient-level forecast.
- Keep the public site readable for a general audience without implying patient-level, fiscal, hospital-demand, workforce or implementation-effect precision.
- Add tests that fail if stale public claim-boundary language returns.

## Acceptance Criteria

- Public source surfaces contain the canonical caveat.
- Public source surfaces do not contain the stale caveat phrases.
- Streamlit dashboard text and scenario-service claim boundary use the canonical wording.
- Public tests pass under `pytest -q -p no:cacheprovider models/tests`.
- Quarto render succeeds, or any render blocker is documented as environmental rather than source-related.

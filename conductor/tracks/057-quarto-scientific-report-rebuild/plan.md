# Plan

Execution wave: `3`.

Depends on:
- `052-public-source-ingestion-and-snapshots`
- `053-public-aggregate-calibration-engine`
- `054-structural-uncertainty-ensemble`
- `055-full-value-of-information-engine`

Blocks:
- `059-release-engineering-and-model-cards`

Safe parallel tracks:
- `056-streamlit-policy-cockpit-and-visual-grammar`
- `061-visual-regression-accessibility-and-browser-tests`

Work packages:

| Work package | Subagent role | Task | Contract | Required gate |
|---|---|---|---|---|
| WP-057-A | `report-structure` | Cover methods, sources, parameters, calibration, uncertainty, VOI, limitations and claim boundaries. | CON-REL-001 | python scripts/render_public_model_report.py, python -m pytest -q models/tests/test_report_artifacts.py |
| WP-057-B | `generated-figures` | Read figures/tables from reproducible outputs, not manual copies. | CON-REL-001 | python scripts/render_public_model_report.py, python -m pytest -q models/tests/test_report_artifacts.py |
| WP-057-C | `model-card-template` | Keep model-card template aligned with release manifest fields. | CON-REL-001 | python scripts/render_public_model_report.py, python -m pytest -q models/tests/test_report_artifacts.py |
| WP-057-D | `report-tests` | Assert expected report artefacts exist and are render-addressable. | CON-REL-001 | python scripts/render_public_model_report.py, python -m pytest -q models/tests/test_report_artifacts.py |

Completion sequence:

1. Confirm dependencies have passed their gates.
2. Assign work packages only within the allowed file globs.
3. Run every required gate listed in `acceptance.md`.
4. Update `implementation-log.md` with files changed, commands run, residual blockers, and claim-boundary status.
5. Run `python scripts/check_conductor_parallel_tracks.py` before marking the track ready for release-wave coordination.

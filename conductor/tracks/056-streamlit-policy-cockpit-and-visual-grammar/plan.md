# Plan

Execution wave: `3`.

Depends on:
- `050-public-only-registry-purification`
- `053-public-aggregate-calibration-engine`
- `054-structural-uncertainty-ensemble`
- `055-full-value-of-information-engine`

Blocks:
- `061-visual-regression-accessibility-and-browser-tests`
- `059-release-engineering-and-model-cards`

Safe parallel tracks:
- `057-quarto-scientific-report-rebuild`

Work packages:

| Work package | Subagent role | Task | Contract | Required gate |
|---|---|---|---|---|
| WP-056-A | `chart-contract` | Every chart exposes title, unit, claim, calibration, uncertainty, source, interpretation, warning, download and table fallback. | CON-VIS-001 | python scripts/run_accessibility_audit.py --check-only, python -m pytest -q models/tests/test_streamlit_cockpit_contracts.py models/tests/test_app.py::test_app_expander_exists |
| WP-056-B | `cockpit-payload` | Build modular cockpit payloads from calibration, structural and VOI engines. | CON-VIS-001 | python scripts/run_accessibility_audit.py --check-only, python -m pytest -q models/tests/test_streamlit_cockpit_contracts.py models/tests/test_app.py::test_app_expander_exists |
| WP-056-C | `app-integration` | Integrate cockpit surfaces without hiding existing public caveats. | CON-VIS-001 | python scripts/run_accessibility_audit.py --check-only, python -m pytest -q models/tests/test_streamlit_cockpit_contracts.py models/tests/test_app.py::test_app_expander_exists |
| WP-056-D | `accessibility` | Validate table fallbacks, labels, contrast warnings and non-colour-only encodings. | CON-VIS-001 | python scripts/run_accessibility_audit.py --check-only, python -m pytest -q models/tests/test_streamlit_cockpit_contracts.py models/tests/test_app.py::test_app_expander_exists |

Completion sequence:

1. Confirm dependencies have passed their gates.
2. Assign work packages only within the allowed file globs.
3. Run every required gate listed in `acceptance.md`.
4. Update `implementation-log.md` with files changed, commands run, residual blockers, and claim-boundary status.
5. Run `python scripts/check_conductor_parallel_tracks.py` before marking the track ready for release-wave coordination.

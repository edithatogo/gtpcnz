# Streamlit Dashboard Live QA - v1

**Date:** 2026-06-04
**Track:** 063-release-readiness-parallel-closeout
**Scope:** Local browser QA of `streamlit_app.py` on `http://localhost:8505`.

## Result

The Streamlit app was launched locally and returned HTTP 200. Microsoft Edge opened the dashboard and the first viewport rendered with the public claim boundary visible.

The live first viewport now shows:

- `This is a public-data anchored benchmark and educational explainer.`
- `It is not linked-data calibrated and not a patient-level forecast.`
- `It should not be used to claim precise fiscal savings, hospital-demand reductions, workforce effects, or implementation impacts.`
- `Claim boundary Public benchmark`
- `Calibration Readiness only`
- `The dashboard is a public-data anchored benchmark and teaching explainer; it is not linked-data calibrated.`

## Defect Found And Fixed

The first browser pass exposed an incorrect public-facing caption:

`Linked-data calibration and validation checks have cleared the core outcomes and core subgroups.`

That contradicted the public-only claim boundary. The fix:

- Changed `models/primarycare_model/empirical_calibration.py` so the supported calibration helper refers to published aggregate calibration gates, not linked-data clearance.
- Changed `models/primarycare_model/scenario_service.py` so the public runtime uses the static public benchmark boundary and does not upgrade claims automatically when local calibration artefacts exist.
- Removed public-runtime `scenario_service.py` imports/invocation of linked calibration helpers for the readiness table; the table now describes public aggregate readiness inputs only.
- Updated tests in `models/tests/test_empirical_calibration.py` and `models/tests/test_scenario_service.py`.

## Verification Commands

Passed:

```powershell
python scripts/check_public_only_boundary.py
python scripts/check_concern_boundaries.py
python -m pytest -q models/tests/test_empirical_calibration.py::test_build_claim_boundary_text_supports_boundary_states models/tests/test_scenario_service.py::test_load_scenario_results_adds_claim_boundary models/tests/test_dashboard_claims.py
python -m pytest -q models/tests/test_scenario_service.py models/tests/test_dashboard_claims.py models/tests/test_streamlit_dashboard_app.py models/tests/test_app.py models/tests/test_streamlit_post_labs.py models/tests/test_streamlit_cockpit_contracts.py
```

The focused dashboard/scenario suite passed with 31 tests. Python printed a temp cleanup traceback after the pytest result, but the process exit code was 0.

A broader empirical-calibration run reached 33 passed tests and then hit the known Windows temp-directory blocker when pytest tried to create `tmp_path`:

```text
PermissionError: [WinError 5] Access is denied: 'C:\\Users\\60217257\\AppData\\Local\\Temp\\pytest-of-60217257'
```

This is consistent with the existing environment blocker classification. The failure occurred at fixture setup, not in a dashboard assertion.

## Browser Coverage

Confirmed through Microsoft Edge and Windows UI Automation:

- Local app opens at `http://localhost:8505`.
- First viewport renders.
- Public caveat is visible.
- Claim boundary status strip is visible.
- Tab strip is visible and scrollable.
- Hidden tabs including `Explainer`, `Evidence/OIA`, and `Calibration` are discoverable after tab-strip scroll.

Not yet confirmed:

- Reliable UI Automation switching into every Streamlit tab. The automation bridge detected tab items but did not reliably change the active Streamlit page.
- Full visual regression screenshots. Python Playwright failed in this environment with Windows subprocess/temp permission errors before browser launch.
- End-to-end interaction of every slider, button, and download control in a real browser.

## Release Status

This QA pass is sufficient to confirm the first public-facing viewport and to catch a material claim-boundary defect. It is not sufficient to claim that the dashboard has been thoroughly browser-tested. Before merge/release, rerun browser QA from a clean non-OneDrive checkout or a CI runner with stable browser automation.

## Local Environment Notes

- The Edge QA window was closed after inspection.
- A local listener on `http://localhost:8505` continued to return HTTP 200 after the original Streamlit execution session lost stdin. Windows denied command-line process inspection, and multiple unrelated `python.exe` processes were present, so the coordinator did not kill an unidentified process.
- The generated `.streamlit-qa-screenshots` directory is empty but could not be removed because the filesystem returned `Access denied`.

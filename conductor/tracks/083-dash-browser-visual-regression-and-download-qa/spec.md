# Track 083 - Dash browser visual regression and download QA

Add browser-level confidence for the Dash/Hugging Face surface, especially dense tables, heatmaps, downloads, guided mode, shareable URLs, and future 3D/animated visuals.

## Scope

- Add Playwright/browser smoke tests for Dash routes at desktop and mobile widths.
- Verify:
  - first viewport content and caveat strip;
  - navigation across all public routes;
  - scenario comparison;
  - live simulation run;
  - table fallbacks;
  - CSV downloads;
  - custom scenario export once Track 081 lands;
  - provenance panels once Track 082 lands;
  - dense heatmaps and any 3D/animated visuals once Track 080 lands.
- Add screenshot comparison or stable visual contract snapshots where practical.
- Add nonblank chart/canvas checks for heavy visuals.
- Keep tests runnable locally and in CI without paid services.

## Non-Goals

- Do not depend on live Hugging Face availability for core local CI.
- Do not require visual perfection snapshots that create brittle noise.
- Do not add browser tests that require secrets or authenticated sessions.

## Required Checks

```powershell
python -m pytest -q models/tests/test_dashboard_service.py models/tests/test_dash_app.py
python scripts/run_accessibility_audit.py --check-only
python scripts/check_public_only_boundary.py
python scripts/check_concern_boundaries.py
```

If Playwright is available:

```powershell
npx playwright test
```

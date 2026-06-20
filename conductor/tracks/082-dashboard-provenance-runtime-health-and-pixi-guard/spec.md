# Track 082 - Dashboard provenance runtime health and Pixi guard

Add operational and provenance features that make every public chart traceable and make deployment/runtime/toolchain status visible.

## Scope

- Add a run provenance panel for every chart or chart bundle:
  - app version;
  - Git SHA/build identifier where available;
  - model version;
  - data source/snapshot;
  - calculation mode: precomputed, cached, live deterministic, seeded stochastic, educational;
  - seed, caps, and runtime bounds;
  - claim boundary and not-valid-for wording.
- Add a deployment/runtime health route or footer panel:
  - Hugging Face Space URL/status placeholder;
  - GitHub Pages front door;
  - app version;
  - build time/Git SHA if provided by environment variables;
  - dependency/runtime posture;
  - cache/precompute status.
- Add a Prefix.dev Pixi guard:
  - detect when `pixi` on PATH is the wrong Pixiv downloader;
  - document expected Prefix.dev Pixi command shape;
  - add a test/script that fails with a clear message when Pixi is not the package manager.
- Keep uv compatibility where it already exists.

## Non-Goals

- Do not add paid monitoring.
- Do not require network calls for local tests.
- Do not expose secrets, tokens, or private deployment metadata.
- Do not change model claims based on operational health.

## Required Checks

```powershell
python -m pytest -q models/tests/test_dashboard_service.py models/tests/test_dash_app.py
python -m pytest -q models/tests/test_release_engineering.py models/tests/test_dashboard_claims.py
python scripts/check_public_only_boundary.py
python scripts/check_concern_boundaries.py
```

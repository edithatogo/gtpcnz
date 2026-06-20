# Track 081 - Dash shareable guided scenario experience

Improve the public Dash/Hugging Face user experience so readers can follow a guided path, share exact dashboard states, and export bounded educational scenarios.

## Scope

- Add shareable scenario URLs that encode selected route, scenarios, sliders, seed, months, population size, and selected view.
- Add a guided reader mode:
  - comparator/current state;
  - reference scenarios;
  - mechanism labs;
  - uncertainty/live model;
  - evidence gaps and calibration readiness.
- Add a bounded scenario builder:
  - create a custom educational scenario;
  - compare it with F0, F4, and F8;
  - export JSON and CSV;
  - preserve clear labels that custom scenarios are educational/model-index only.
- Add copy-link controls, reset controls, and state validation.
- Add tests for URL parse/serialize round trips and claim-boundary wording.

## Non-Goals

- Do not create patient-level forecasts.
- Do not persist user-created scenarios server-side.
- Do not add accounts, databases, Redis, paid workers, or paid hardware.
- Do not let shared URLs bypass runtime caps or validation.

## Required Checks

```powershell
python -m pytest -q models/tests/test_dashboard_service.py models/tests/test_dash_app.py
python -m pytest -q models/tests/test_runtime_lab.py models/tests/test_scenario_service.py models/tests/test_dashboard_claims.py
python scripts/check_public_only_boundary.py
python scripts/check_concern_boundaries.py
```

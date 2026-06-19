# Plan

1. Add `models/primarycare_model/dashboard_service.py` as the framework-neutral payload layer.
2. Add `dash_app/` with layout, callbacks, CSS, and a Hugging Face Space Docker bundle.
3. Add Dash smoke/service tests and keep public claim-boundary tests in force.
4. Update README, Quarto homepage, dashboard contract/audit, and deployment docs to name GitHub Pages plus Hugging Face as the canonical topology.
5. Keep Streamlit documented as a compatibility surface until the Dash Space is live and validated.

Required checks:

```powershell
python -m pytest -q models/tests/test_dashboard_service.py models/tests/test_dash_app.py
python -m pytest -q models/tests/test_runtime_lab.py models/tests/test_scenario_service.py models/tests/test_dashboard_claims.py
python scripts/check_public_only_boundary.py
python scripts/check_concern_boundaries.py
python scripts/run_accessibility_audit.py --check-only
```


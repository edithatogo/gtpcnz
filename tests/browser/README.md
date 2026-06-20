# Browser Tests

Browser smoke tests verify that public dashboard surfaces render the required sections.

- `test_streamlit_smoke.py` keeps the Streamlit cockpit contract visible while Streamlit remains a compatibility surface.
- `test_dash_browser_contract.py` keeps the Dash/Hugging Face route contract browser-runtime-free so it can run in ordinary pytest.
- `python scripts/check_dash_browser_smoke.py` runs the real Playwright smoke against a local Dash server. The default pass checks Start, Reference scenarios, Model surface, Calibration diagnostics and Runtime health at desktop and mobile widths; pass `--full` for the heavier live-model, scenario-builder and advanced-visual routes.
- Add `--screenshot-dir <path>` to write first-viewport screenshots for visual-regression review without making screenshots part of every quick test run.

Future visual-regression checks should add reviewed screenshot baselines and image-diff thresholds for release gates.

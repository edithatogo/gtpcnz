# Streamlit Cloud live deployment blocker - 2026-06-04

## Status

The repository-side release state is green on `origin/main`, but the hosted
Streamlit Community Cloud app at <https://gtpcnz.streamlit.app/> still renders
Streamlit's generic startup failure page:

```text
Oh no.

Error running app. If this keeps happening, please contact support.
```

## Evidence

Post-merge GitHub Actions for `origin/main` passed:

- CI, including public-only, parameter traceability, public snapshot,
  dependency lock, calibration, VOI, repo health, concern boundaries, tests,
  Quarto render, Streamlit import verification, visual regression,
  accessibility, release model card, and release manifest.
- Publish Quarto site.
- Quality.
- CodeQL.
- Automatic dependency submission.

Live browser checks with Playwright/Chromium after the final merge still showed
the generic Streamlit Cloud error and did not show the repository's guarded
startup fallback text. This means the hosted app is not yet executing the
current `main` entrypoint, or it is failing before the Python script is pulled
and run.

## Repo-side fixes already merged

- `scikit-learn` was added to `pyproject.toml` and `requirements.txt` because
  the app runs outcome clustering during initial render.
- `streamlit_app.py` now defers importing the dashboard app until inside a
  guarded `main()` function and renders a public-boundary fallback if startup
  fails after the script begins executing.

## Required external action

Open Streamlit Community Cloud for the `gtpcnz` app and verify:

1. Repository: `edithatogo/gtpcnz`.
2. Branch: `main`.
3. Main file path: `streamlit_app.py`.
4. The app has redeployed commit `2da974c3ed7c3a9152c0b9677581290852e795a7`
   or later.
5. If still failing, use the Streamlit Cloud logs to identify whether the
   failure is dependency installation, repository checkout, branch mismatch, or
   Python runtime startup.

After reboot/redeploy, rerun:

```powershell
python -m pytest -q models/tests/test_streamlit_dashboard_app.py models/tests/test_app.py models/tests/test_streamlit_post_labs.py models/tests/test_streamlit_cockpit_contracts.py
```

Then re-check the live app at <https://gtpcnz.streamlit.app/>.

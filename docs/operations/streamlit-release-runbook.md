# Streamlit Release Runbook

## Pre-release Checklist

- [ ] Run `python -m pytest -q models/tests/` (all pass)
- [ ] Run `python scripts/check_concern_boundaries.py` (5/5 pass)
- [ ] Run `python scripts/check_no_patient_data.py --verbose` (clean)
- [ ] Run `python scripts/check_data_freshness.py` (fresh)
- [ ] Run `python scripts/sync_public_mirror.py --check` (no drift)
- [ ] Run `python scripts/check_repo_health.py` (pass)
- [ ] Build Quarto: `quarto render --to html`
- [ ] Verify canonical URL references are `https://gtpcnz.streamlit.app/`

## Deployment Steps

1. Commit all changes with a scoped message
2. Push to `origin/main`
3. Wait for GitHub Actions to complete
4. Check GitHub Pages deploy
5. Verify Streamlit Community Cloud auto-deploys from `main`

## Post-deployment Verification

- [ ] Open https://gtpcnz.streamlit.app/
- [ ] Run app smoke test: `streamlit run streamlit_app.py`
- [ ] Verify all tabs load
- [ ] Check sidebar sliders render
- [ ] Run `python -m pytest -q models/tests/test_app.py`

## Rollback

1. `git revert HEAD --no-edit`
2. `git push origin main`
3. Streamlit Cloud auto-reverts from the previous commit

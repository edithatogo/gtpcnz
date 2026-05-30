# Plan: Public Repo Submodule Boundary

**Status:** Complete

## Steps

1. Detach the parent workspace from the public GitHub remote.
2. Replace the public repository contents with a minimal dashboard/site repository.
3. Verify the public repository is public and contains only the intended files.
4. Add `public/gtpcnz` as a submodule in the parent workspace.
5. Validate the Streamlit app by serving it locally and checking HTTP 200.
6. Validate the Quarto site by rendering in a clean temp/cache environment.
7. Configure GitHub Pages for the public repository.
8. Keep GitHub Actions workflows present, but record any account-level runner blocker separately from code validation.

## Current Execution Notes

- Parent remote to `edithatogo/gtpcnz` was removed to avoid accidental full-workspace pushes.
- Public repository `edithatogo/gtpcnz` was made public after replacing `main` with a minimal public history.
- GitHub Actions did not start because GitHub reported an account billing/spending-limit block, not a workflow or code failure.
- A `gh-pages` branch fallback is used for Pages so the site can deploy without Actions while that account-level blocker exists.
- This track is reconciled from existing evidence in the repository; no new live repository or deployment action is being performed in this turn.

## Verification Evidence

- Parent repo has no configured remote.
- Parent repo records `public/gtpcnz` as gitlink `094c9e0606c2607dd1fffa819ae5a7b56272383e`.
- Public repo `main` root contains only dashboard/site/support files.
- Streamlit smoke test: `python -m streamlit run streamlit_app.py --server.headless true --server.port 8507 --browser.gatherUsageStats false`, then `Invoke-WebRequest http://localhost:8507/` returned HTTP 200.
- Public Streamlit URL: `https://gtpcnz.streamlit.app/` returned HTTP 200.
- Tests: `pytest -q -p no:cacheprovider` returned `5 passed`.
- Quarto: rendered successfully from a clean `C:\tmp\gtpcnz-render` copy with explicit `TEMP`, `TMP` and `DENO_DIR`.
- GitHub Pages: `gh-pages` branch deployment completed successfully and `https://edithatogo.github.io/gtpcnz/` returned HTTP 200.
- GitHub Actions blocker: run `25712203966` and run `25712203963` failed before job start with GitHub's account billing/spending-limit error.

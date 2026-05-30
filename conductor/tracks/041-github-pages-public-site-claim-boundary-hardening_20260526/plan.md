# Plan — COMPLETE

## Phase 1. Public Claim Language

- Update homepage, footer, public report, model card, claim-boundaries page, dashboard guide, Streamlit deployment note and public-site contract docs to use the canonical caveat.
- Replace stale scaffold phrasing with public-data anchored benchmark language where it is visible to public readers.
- Keep current reform, toy explainer, model-generated index and validation-readiness boundaries intact.

## Phase 2. Dashboard Runtime Surfaces

- Update `scenario_service.py` so scenario output rows carry the canonical claim boundary.
- Update the Streamlit dashboard guide, caveat box, status tables, captions, glossary and runtime lab copy.
- Preserve the pre-existing cleanup that removed repo-only document paths from the Streamlit app.

## Phase 3. Tests and Guardrails

- Update dashboard and scenario-service tests to assert the canonical caveat.
- Add stale-phrase guardrails for public source surfaces.
- Update homepage visual-contract tests to require the new caveat and reject old wording.

## Phase 4. Validation and Release Evidence

- Run `pytest -q -p no:cacheprovider models/tests` in `public/gtpcnz`.
- Run `git diff --check` in the parent repo and the public submodule.
- Render the Quarto site with `quarto render --to html`; use a clean copy if OneDrive locks interfere.
- Before deployment closeout, check the live homepage, report, model card, claim-boundaries page and Streamlit app for the canonical caveat and absence of stale wording.

## Current Notes

- Track number `040` was already present for the bleeding-edge experimental lane, so this work uses `041`.
- This track depends on `036-visual-contract-validation-release_20260513`, which last published the public GitHub Pages and Streamlit release evidence.
- Local validation passed on 2026-05-26: `pytest -q -p no:cacheprovider models/tests` in `public/gtpcnz` reported `31 passed`.
- Direct Quarto render in OneDrive was blocked by a locked `pytest-cache-files-*` directory; clean-copy render from `C:\tmp\gtpcnz-render-041-20260526` passed and produced `_site\index.html`.
- Generated-site text audit found the canonical caveat on the homepage, report, model card and claim-boundaries page, and found no stale `source-informed parameterised scaffold`, `source-informed model scaffold` or `not a real-data calibrated forecast` phrase in `_site`.
- Public source commit pushed to `edithatogo/gtpcnz` `main`: `872efce` (`fix(site): enforce full benchmark caveat`).
- Rendered Pages commit pushed to `edithatogo/gtpcnz` `gh-pages`: `f8a0bed` (`Publish rendered Quarto site`).
- GitHub Pages latest build is tied to `f8a0bed` and reports `building` with no error as of 2026-05-26T12:02:33Z; live URL still returned the older cached/stale wording during the immediate post-push audit.
- **Deployment verification (2026-05-26):** Source code and `gh-pages` branch confirmed correct with canonical caveat. The first rebuilt branch (`302b93e`) had the hardened caveat but not the current visual-gallery homepage. Rebuilt current `main` (`79651d2`) in `C:\tmp\gtpcnz-republish-041\repo`, verified `pytest -q -p no:cacheprovider models/tests` (`31 passed`) and `quarto render --to html`, then pushed `gh-pages` `feab13d` (`fix(site): publish current visual gallery artifact`). Raw `gh-pages/index.html` now contains `GTPCNZ visual gallery` and the full public-data benchmark caveat, and does not contain the stale scaffold wording.
- **Publication verification (2026-05-26):** Retried GitHub Pages run `26448953499`; the build, report-build-status and deploy jobs completed successfully. GitHub Pages build status for `feab13d` is `built` as of `2026-05-26T12:53:15Z`. Live `https://edithatogo.github.io/gtpcnz/` now contains `GTPCNZ visual gallery` and `public-data anchored benchmark`, and no longer contains `source-informed model scaffold` or `not a real-data calibrated forecast`.

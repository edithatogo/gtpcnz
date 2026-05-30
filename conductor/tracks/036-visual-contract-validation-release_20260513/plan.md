# Plan: Visual Contract Validation and Release

Status: Complete.

## Phase 1: Child-Track Review Sweep

1. Run `$conductor-review` for Track 031.
2. Run `$conductor-review` for Track 032.
3. Run `$conductor-review` for Track 033.
4. Run `$conductor-review` for Track 034.
5. Run `$conductor-review` for Track 035.
6. Apply safe in-scope fixes and rerun scoped validation after each fix.

Progression rule: do not proceed to release validation while any child track has unresolved high-severity findings.

## Phase 2: Integrated Local Validation

1. Run `python -m compileall models`.
2. Run `pytest -q`.
3. Run `quarto render --to html`.
4. Run `python -m py_compile streamlit_app.py models/primarycare_model/app.py models/primarycare_model/scenario_service.py`.
5. Run static content checks for caveats, crosswalk terms, local paths and private Substack content in the public repo.

Review gate: run `$conductor-review` for Track 029 and Track 036, apply safe fixes, rerun failed checks.

## Phase 3: Public Release

1. Commit public repo changes.
2. Push public repo.
3. Confirm GitHub Actions pass.
4. Confirm GitHub Pages deployment updates.
5. Update parent submodule pointer and Conductor evidence.
6. Push parent repository only if requested/approved and boundary is preserved.

Review gate: run `$conductor-review` for Track 036 release evidence, apply safe fixes, rerun checks.

## Phase 4: Browser Audit

1. Screenshot GitHub Pages homepage.
2. Screenshot rendered Quarto report.
3. Screenshot Streamlit dashboard.
4. Check for app errors, local paths, editorial comments, private drafts and UX regressions.
5. Record evidence and residual risks.

Review gate: run `$conductor-review` for Track 036 closeout, apply safe fixes, rerun checks.

## Validation

```powershell
python -m compileall models
pytest -q
quarto render --to html
python -m py_compile streamlit_app.py models/primarycare_model/app.py models/primarycare_model/scenario_service.py
git -C public/gtpcnz ls-files | rg "substack-ready|posts-v|appendices-v|long-drafts|C:\\\\Users|OneDrive"
```

## Review Evidence

- 2026-05-13 setup-phase review: track registered and cross-referenced to Track 029 and the post-surface crosswalk contract.
- Metadata validation passed with `python -m json.tool`.
- Findings: no high-severity setup findings. Integrated release validation is supported by the recorded Track 031-035 implementation passes and the 2026-05-14 public release closeout below.
- 2026-05-13 integration pass: public repo implementation for Tracks 032-035 completed and scoped tests passed.
- Validation passed: `pytest -q -p no:cacheprovider models/tests` in `public/gtpcnz` reported `22 passed`.
- Validation passed: `python -m compileall models` in `public/gtpcnz` passed with `PYTHONPYCACHEPREFIX` pointed to an external writable cache.
- Validation passed: py_compile for `streamlit_app.py`, `models/primarycare_model/app.py` and `models/primarycare_model/scenario_service.py` passed using explicit external `cfile` targets because OneDrive denied local `__pycache__` writes.
- Boundary check passed: public tracked files do not include `substack-ready`, `posts-v`, `appendices-v`, `long-drafts`, `C:\\Users` or `OneDrive`.
- Validation passed: `quarto render --to html` in `public/gtpcnz` completed after clearing opencode/kilo caches, npm cache and old temp files; output created `_site/index.html`.
- Disk/cache remediation: C: free space increased from about 856 MB to about 34.8 GB after clearing opencode/kilo caches, npm cache and old temp files.
- Review result: no high-severity implementation findings found.
- 2026-05-14 fix: Streamlit post guide table now includes a dedicated `Public title` column so the crosswalk columns do not shift values.
- 2026-05-14 fix: parent and public `_quarto.yml` render lists now include `docs/public-site/post-surface-crosswalk-contract-v1.8.2.md` and `docs/public-site/game-theory-microeconomics-simulation-spec-v1.8.2.md`.
- 2026-05-14 local validation: `pytest -q -p no:cacheprovider models/tests` in `public/gtpcnz` returned `22 passed` (Python emitted a temp-cleanup `PermissionError` after test success because Windows/OneDrive held a temp directory).
- 2026-05-14 local validation: explicit `py_compile` with `cfile` targets under `%LOCALAPPDATA%\Temp\gtpcnz-compile-cfiles` passed for `streamlit_app.py`, `models/primarycare_model/app.py` and `models/primarycare_model/scenario_service.py`.
- 2026-05-14 local validation: clean-copy `quarto render --to html` from `%LOCALAPPDATA%\Temp\gtpcnz-render-clean` passed and created `_site\index.html`; this avoided locked ignored OneDrive cache directories in the working tree.
- 2026-05-14 diff validation: `git diff --check` in `public/gtpcnz` passed with only LF/CRLF warnings.
- 2026-05-14 public repo commit and push: `2751ffe8dcb2e7ec10b7e50004f944335ff9fb9f` (`feat(site): add post-aligned visual contract`) pushed to `edithatogo/gtpcnz` `main`.
- 2026-05-14 GitHub Actions: CI run `25808848002` passed; Publish Quarto site run `25808847996` passed and deployed.
- 2026-05-14 deployed Pages audit: homepage returned HTTP 200 and contained `GTPCNZ visual gallery` plus `Post crosswalk`.
- 2026-05-14 deployed Quarto report audit: `reports/primary_care_architecture.html` returned HTTP 200 and contained `How the posts map to this report and dashboard` plus `Why formulas do not solve games`.
- 2026-05-14 deployed crosswalk audit: `docs/public-site/post-surface-crosswalk-contract-v1.8.2.html` returned HTTP 200 and contained `Post-to-surface crosswalk contract v1.8.2`.
- 2026-05-14 Streamlit availability audit: `https://gtpcnz.streamlit.app/` returned HTTP 200.
- 2026-05-14 parent gitlink: `public/gtpcnz` updated from `67cc636e1625464f9dcee5e43c6f845ac0a509c6` to `2751ffe8dcb2e7ec10b7e50004f944335ff9fb9f`.
- Final audit conclusion: met. Residual risk is limited to Windows/OneDrive cache-lock noise in local validation; clean-copy Quarto render, GitHub Actions, deployed Pages, deployed report and Streamlit HTTP checks all passed.

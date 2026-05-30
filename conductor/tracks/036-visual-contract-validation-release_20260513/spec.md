# Spec: Visual Contract Validation and Release

## Problem

The public visual contract spans multiple surfaces. It needs an integrated closeout track that proves the contracts were implemented, tests pass, deployment updated and screenshots show the real public UX.

## Goal

Validate and release the combined work from Tracks 031-035.

## Owned Files

Primary:

- validation/audit docs under `docs/public-site/`;
- proof screenshots under an ignored proof folder or tracked manifest where appropriate;
- parent Conductor status updates;
- public submodule pointer after public repo push.

This track must not introduce new content features except fixes required by review or validation.

## Requirements

1. Run the full relevant validation suite.
2. Run `$conductor-review` for each child track and the integrated Track 029 contract.
3. Apply safe in-scope fixes from reviews.
4. Rerun failed or relevant validations after fixes.
5. Confirm public repo does not include private Substack posts or drafts.
6. Confirm GitHub Actions pass after push.
7. Confirm GitHub Pages updated and Quarto report is reachable.
8. Confirm Streamlit app loads without app errors.
9. Take screenshots of GitHub Pages, Quarto report and Streamlit dashboard.
10. Record release evidence and any residual risks.

## Parallelisation

This track is mostly integration, but verification can be parallelised:

- Subagent A checks static repo contract compliance.
- Subagent B checks deployed GitHub Pages and Quarto URLs.
- Subagent C checks Streamlit app behavior and screenshots.
- Main agent coordinates fixes, commits, pushes and final evidence.

## Acceptance Criteria

1. Tracks 031-035 have review evidence and no unresolved high-severity findings.
2. Tests pass or have recorded OneDrive-safe equivalents:
   - `pytest -q -p no:cacheprovider models/tests` returned `22 passed`;
   - clean-copy `quarto render --to html` passed;
   - explicit `py_compile` with external `cfile` targets passed;
   - direct `compileall` was superseded by the external-cache and explicit-cfile checks because local OneDrive cache paths were locked.
3. Public repo boundary is preserved.
4. GitHub Actions pass.
5. GitHub Pages and Quarto report are live and audited by deployed content checks.
6. Streamlit app is live and audited by HTTP availability check.
7. The final audit states whether the contract is met, partially met or blocked: **met**.

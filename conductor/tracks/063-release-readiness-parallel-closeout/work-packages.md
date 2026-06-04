# Work Packages

## WP-063-A: Diff Audit

Subagent role: `diff-auditor`

Goal:

- Classify the working tree after 050-062 into intended implementation, public mirror sync, generated/transient files, suspicious unrelated edits, and files needing manual review.

Allowed writes:

- `conductor/tracks/063-release-readiness-parallel-closeout/implementation-log.md`

Commands:

- `git status -sb`
- `git diff --stat`
- `git status --short public/gtpcnz`
- nested public mirror `git status -sb` where available

## WP-063-B: Environment Blockers

Subagent role: `environment-blocker`

Goal:

- Reproduce and isolate Windows/OneDrive blockers for full pytest, py_compile, Quarto render, and Git shell/submodule calls.

Allowed writes:

- `docs/testing/release-readiness-environment-blockers-v1.md`
- `conductor/tracks/063-release-readiness-parallel-closeout/implementation-log.md`

Commands:

- `python -m pytest -q`
- in-memory syntax compile for `streamlit_app.py` and `models/primarycare_model/app.py`
- `quarto render --to html`
- relevant temp/cache reruns with repo-local temp paths

## WP-063-C: Gate Rerun

Subagent role: `gate-runner`

Goal:

- Rerun deterministic public-only, parameter, source snapshot, VOI, accessibility, release, and mirror gates.

Allowed writes:

- `docs/release/release-readiness-gate-rerun-v1.md`
- `conductor/tracks/063-release-readiness-parallel-closeout/implementation-log.md`

Commands:

- all required gates listed in `acceptance.md`

## WP-063-D: Commit Packaging

Subagent role: `commit-packager`

Goal:

- Produce a non-destructive commit grouping plan for reviewable slices.

Allowed writes:

- `docs/release/release-readiness-commit-plan-v1.md`
- `conductor/tracks/063-release-readiness-parallel-closeout/implementation-log.md`

Constraints:

- Do not run `git reset`, `git checkout --`, recursive deletion, or submodule rewrites.

## WP-063-E: Public Source Readiness

Subagent role: `public-source-readiness`

Goal:

- Define what is needed to move public aggregate calibration beyond readiness-only using only public or published sources.

Allowed writes:

- `docs/model/public-source-readiness-closeout-v1.md`
- `conductor/tracks/063-release-readiness-parallel-closeout/implementation-log.md`

Claim boundary:

- Keep calibration at `calibration_readiness_only` until public source retrieval, licence/access metadata, checksums, transformations, and validation gates pass.

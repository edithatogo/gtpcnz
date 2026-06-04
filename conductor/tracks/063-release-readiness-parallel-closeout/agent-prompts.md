# Agent Prompts

Use these prompts with Cline and DeepSeek v4 Flash. Keep depth shallow: coordinator -> work-package subagent only.

## Coordinator Prompt

You are coordinating GTPCNZ Track 063 release-readiness closeout. Run shallow parallel work packages where file ownership does not overlap. Do not use private administrative data, patient-level data, confidential OIA responses, stakeholder analysis, or unpublished expert elicitation. Do not claim precise fiscal savings, ED reductions, hospital-demand reductions, workforce effects, implementation impacts, or causal effects unless public calibration and validation gates pass. Preserve `calibration_readiness_only` unless Track 053 source readiness changes.

Read:

- `conductor/tracks/063-release-readiness-parallel-closeout/spec.md`
- `conductor/tracks/063-release-readiness-parallel-closeout/plan.md`
- `conductor/tracks/063-release-readiness-parallel-closeout/work-packages.md`
- `conductor/tracks/063-release-readiness-parallel-closeout/contracts.md`
- `conductor/parallel-execution-matrix.json`

Run startup gate:

- `python scripts/check_conductor_parallel_tracks.py`

Assign Wave 5A in parallel:

- WP-063-A `diff-auditor`
- WP-063-B `environment-blocker`
- WP-063-E `public-source-readiness`

Then run Wave 5B:

- WP-063-C `gate-runner`

Then run Wave 5C:

- WP-063-D `commit-packager`

Close out with:

- `python scripts/check_conductor_parallel_tracks.py`
- the required gates in `acceptance.md`

## WP-063-A Prompt

Classify the working tree. Read only by default. Write findings only to `conductor/tracks/063-release-readiness-parallel-closeout/implementation-log.md`. Do not run destructive git commands. Identify intended 050-062 implementation changes, public mirror sync changes, transient/generated artifacts, suspicious unrelated edits, and manual review items.

## WP-063-B Prompt

Reproduce environment blockers and classify them. Write `docs/testing/release-readiness-environment-blockers-v1.md` and update the implementation log. Treat WinError 5 temp cleanup, pycache rename, Quarto `_site` deletion, and invalid-handle subprocess failures as environment blockers only if no code assertion failure is present.

## WP-063-C Prompt

Run the required deterministic gates from `acceptance.md`. Write `docs/release/release-readiness-gate-rerun-v1.md` and update the implementation log. Keep claim boundaries unchanged and distinguish readiness-only passes from calibrated-model passes.

## WP-063-D Prompt

Create a commit grouping plan in `docs/release/release-readiness-commit-plan-v1.md`. Do not stage, reset, checkout, delete, or rewrite files. Group changes into reviewable slices and list files that need manual review before commit.

## WP-063-E Prompt

Create `docs/model/public-source-readiness-closeout-v1.md`. Define the public/published source retrieval, licence/access, checksum, transform, and validation tasks needed before Track 053 can move beyond `calibration_readiness_only`. Do not propose private, patient-level, confidential OIA, stakeholder, or unpublished expert-elicitation inputs.

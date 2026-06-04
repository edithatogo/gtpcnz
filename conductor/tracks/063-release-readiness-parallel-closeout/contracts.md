# Contracts

## CON-063-001: Closeout Cannot Inflate Claims

Release closeout may document gate status and blocker status only. It must not claim precise fiscal savings, ED reductions, hospital-demand reductions, workforce effects, implementation impacts, or causal effects unless the relevant public-data calibration and validation gates pass.

Gate:

- `python scripts/run_public_aggregate_calibration.py --check-only`
- `python scripts/generate_release_model_card.py --check-only`

## CON-063-002: Public-Only Boundary Remains Binding

No closeout task may introduce private administrative data, patient-level data, confidential OIA responses, stakeholder analysis, linked-data runtime inputs, or unpublished expert elicitation into the public model path.

Gate:

- `python scripts/check_public_only_boundary.py`
- `python scripts/check_concern_boundaries.py`

## CON-063-003: Environment Blockers Must Be Separated From Code Failures

Windows/OneDrive filesystem failures must be recorded as environment blockers only when the failure trace is a temp/cache/delete/subprocess handle failure and no assertion or contract failure is present.

Evidence:

- exact command;
- exact error class;
- whether tests reached assertion completion;
- recommended rerun environment.

## CON-063-004: No Destructive Git Actions

Subagents may inspect and classify diffs but must not run destructive commands such as `git reset`, `git checkout --`, recursive deletion, or submodule rewrites. Any cleanup requiring deletion must be proposed for coordinator approval.

## CON-063-005: Public Mirror Status Must Be Explicit

If `public/gtpcnz` is dirty, the track must classify whether this is expected mirror sync output, nested repo drift, or unresolved submodule state.

Gate:

- `python scripts/sync_public_mirror.py --check`

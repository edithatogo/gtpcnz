# Spec

## Purpose

Close out the 050-062 implementation safely by turning the large scaffolded working tree into a reviewable, release-ready state.

The track coordinates diff audit, environment-blocker remediation, release-gate reruns, commit grouping, and public-source readiness planning. It is deliberately a closeout and hardening track, not a new modelling-claim expansion track.

## Scope

In scope:

- Audit the large 050-062 diff for accidental, unrelated, transient, or generated changes.
- Separate intended implementation changes from local filesystem artifacts and public mirror updates.
- Create a Cline/DeepSeek v4 Flash execution plan that can run shallow subagents in parallel.
- Reproduce deterministic public-only, parameter, snapshot, VOI, accessibility, release, and mirror gates.
- Diagnose and document Windows/OneDrive blockers affecting pytest temp cleanup, py_compile cache writes, Quarto `_site` deletion, and Git shell/submodule commands.
- Prepare commit grouping and review notes so the implementation can be merged in coherent slices.
- Preserve the claim boundary and keep calibration at `calibration_readiness_only` until public source readiness changes.

Out of scope:

- No private administrative data.
- No patient-level data.
- No confidential OIA response inputs.
- No stakeholder analysis.
- No unpublished expert elicitation as model input.
- No automatic evidence-monitor mutation of public parameters, outputs, or claims.
- No claim of precise fiscal savings, ED reductions, hospital-demand reductions, workforce effects, implementation impacts, or causal effects unless public calibration and validation gates pass.

## Deliverables

- Completed track artifacts in `conductor/tracks/063-release-readiness-parallel-closeout/`.
- Updated Conductor registry/state pointing to the closeout track.
- A parallel Cline/DeepSeek work-package plan with bounded file ownership.
- A gate rerun record distinguishing code failures from local Windows/OneDrive filesystem blockers.
- A commit/readiness grouping plan for the 050-062 implementation.
- A public-source readiness note that keeps Track 053 blocked at readiness-only until source checksums and validation gates pass.

## Public Claim Boundary

This track must preserve the current public claim boundary: GTPCNZ is a public-data anchored benchmark and educational explainer. It is not linked-data calibrated, not a patient-level forecast, and not a source-verified public aggregate calibrated model until the relevant public-source and validation gates pass.

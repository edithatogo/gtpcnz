# Spec: Bleeding Edge Experimental Lane And Scorecard

**Status:** Complete

## Problem

The repository already has a stable release lane and a latest-compatible canary lane, but the public documentation still describes the latest canary as the only "bleeding edge" signal. That is not enough to honestly claim a truly bleeding-edge posture, because there is no isolated experimental lane, no edge-specific triage note, and no measurable scorecard for how far the repo has moved toward current preview tooling.

## Goal

Add a third dependency lane for experimental preview packages and next-dev runtime coverage, expose a measurable bleeding-edge scorecard, and document the triage path so the repository can claim a deliberate bleeding-edge posture without weakening the stable release gate.

The stable release path must remain the release gate. The experimental lane must be isolated, explicit, and non-blocking for readers unless the maintainers choose to promote a package or runtime after review.

## Owned Files

Primary:

- `requirements-edge.txt`
- `.github/workflows/dependency-edge.yml`
- `scripts/check_repo_health.py`
- `scripts/check_bleeding_edge_scorecard.py`
- `docs/bleeding-edge-scorecard-v1.0.md`
- `docs/operations/dependency-edge-triage-v1.0.md`
- `docs/dependency-policy-v1.8.3.md`

Supporting:

- `docs/requirements-moscow-v1.8.3.md`
- `docs/contracts/repo-github-streamlit-contracts-v1.8.3.md`
- `docs/design/repo-github-streamlit-design-v1.8.3.md`
- `README.md`

## Requirements

1. Add a dedicated experimental edge dependency manifest that allows prerelease package resolution without changing `requirements.txt`.
2. Add a workflow that installs the edge manifest on a next-dev Python runtime and runs the same health, test, render and compile gates as the stable lane.
3. Publish a bleeding-edge scorecard with a 30-point rubric and a target threshold of at least 27/30.
4. Add a short triage runbook for edge-only failures so preview breakage is recorded as a controlled upgrade item.
5. Update the dependency policy, MoSCoW register, contracts and design diagram so the three-lane posture is explicit.
6. Extend repo-health output so the edge scorecard is visible in machine-readable form while release health remains the stable gate.
7. Keep the public claim boundary unchanged: the edge lane is about dependency recency and runtime coverage, not stronger model validity.

## Bleeding-Edge Completion Bar

The lane can be called truly bleeding edge when all of the following are true:

- stable release CI remains green;
- the latest canary lane exists and remains separately runnable;
- the edge lane uses prerelease dependency resolution;
- the edge lane exercises a next-dev Python runtime;
- the scorecard reaches at least 27/30;
- the triage note is committed and linked from the policy surface.

## Acceptance Criteria

1. `requirements-edge.txt` exists and is clearly experimental.
2. `.github/workflows/dependency-edge.yml` exists and runs the edge lane.
3. The repo-health JSON exposes the edge scorecard.
4. The dependency policy documents stable, canary and edge lanes.
5. The requirements, contracts and design docs all name the three-lane posture.
6. The stable release gate remains separate from the experimental lane.

## Out Of Scope

- Changing the claim boundary to imply linked-data calibration.
- Replacing the stable release lane with preview packages.
- Adding a heavy new dependency solely to look modern.
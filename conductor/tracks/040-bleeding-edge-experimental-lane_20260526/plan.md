# Plan: Bleeding Edge Experimental Lane And Scorecard

**Status:** Completed.

## Phase 1: Scorecard And Policy Baseline

- Define the six-axis bleeding-edge scorecard and the 27/30 target.
- Record the three-lane dependency posture in the policy document.
- Add the triage note that explains how to handle edge-only failures.

## Phase 2: Edge Lane Implementation

- Add `requirements-edge.txt` as the experimental dependency manifest.
- Add `.github/workflows/dependency-edge.yml` for prerelease installs on a next-dev Python runtime.
- Ensure the edge workflow runs the same health, test, render and compile gates as the stable lane.

## Phase 3: Repo-Health And Documentation

- Extend `scripts/check_repo_health.py` so the edge scorecard is emitted in machine-readable form.
- Add the scorecard doc and wire it into the repo's public policy surface.
- Update the MoSCoW register, contracts and design diagram to include the third lane.

## Phase 4: Validation

- Run `pytest -q`.
- Run `python scripts/check_repo_health.py`.
- Run the edge scorecard script against the new lane surface.
- Verify the stable release path is unchanged and still uses `requirements.txt`.

## Phase 5: Closeout

- Confirm the edge lane is isolated from release CI.
- Confirm the scorecard reaches at least 27/30.
- Commit the track with the new lane artifacts and publish the branch update.

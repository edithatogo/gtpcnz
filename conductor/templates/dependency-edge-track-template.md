# Track Template: Dependency and Runtime Edge Lane

## Metadata

- Track ID: `<next-id>-dependency-edge-<date>`
- Owner: `dependency-edge-agent`
- Status: `pending`
- Scope: dependency manifests, CI workflows, scorecards, compatibility checks.

## Problem

The repo needs to distinguish stable release confidence from experimental dependency/runtime recency.

## Goals

- Maintain stable CI as the release gate.
- Maintain latest-compatible dependency canary.
- Maintain experimental edge lane without making preview failures release-blocking.
- Keep the bleeding-edge scorecard factual and testable.

## Required Checks

```powershell
python scripts/check_repo_health.py
python -m pytest -q -p no:cacheprovider models/tests
python -m pip install --dry-run --pre -r requirements-edge.txt
rg -n "requirements-edge|dependency-edge|bleeding-edge scorecard|three-lane" .github docs scripts requirements-edge.txt
```

## Acceptance Criteria

- Stable and edge lanes are documented separately.
- Preview/pre-release dependencies are isolated to edge manifests or edge workflows.
- Stable app and model tests pass.
- Any edge failure creates a triage item, not a silent downgrade.

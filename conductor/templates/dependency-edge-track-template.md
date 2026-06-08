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
uv sync --upgrade --all-groups --prerelease allow
uv run python scripts/check_repo_health.py
uv run python -m pytest -q -p no:cacheprovider models/tests
rg -n "dependency-edge|bleeding-edge scorecard|three-lane|prerelease" .github docs scripts pyproject.toml
```

## Acceptance Criteria

- Stable and edge lanes are documented separately.
- Preview/pre-release dependencies are isolated to edge workflows.
- Stable app and model tests pass.
- Any edge failure creates a triage item, not a silent downgrade.

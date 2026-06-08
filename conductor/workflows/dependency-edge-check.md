# Workflow: Dependency Edge Check

## Goal

Keep the edge lane factual and separate from stable release confidence.

## Procedure

```powershell
uv sync --upgrade --all-groups --prerelease allow
uv run python scripts/check_repo_health.py
uv run python -m pytest -q -p no:cacheprovider models/tests
```

Review:

```powershell
rg -n "actions/checkout@|astral-sh/setup-uv@|dependency-edge|Dependabot|bleeding-edge|prerelease" .github docs scripts pyproject.toml
```

## Result Classes

- `stable-pass`: stable CI and local health pass.
- `canary-pass`: latest-compatible dependency canary passes.
- `edge-pass`: preview/edge lane passes.
- `edge-fail-triage`: edge lane fails but stable remains releasable.
- `release-blocker`: stable tests, health, app boot, or security gates fail.

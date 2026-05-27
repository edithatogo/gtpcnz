# Workflow: Dependency Edge Check

## Goal

Keep the edge lane factual and separate from stable release confidence.

## Procedure

```powershell
python scripts/check_repo_health.py
python -m pytest -q -p no:cacheprovider models/tests
python -m pip install --dry-run --pre -r requirements-edge.txt
```

Review:

```powershell
rg -n "actions/checkout@|actions/setup-python@|requirements-edge|dependency-edge|Dependabot|bleeding-edge" .github docs scripts requirements*.txt pyproject.toml
```

## Result Classes

- `stable-pass`: stable CI and local health pass.
- `canary-pass`: latest-compatible dependency canary passes.
- `edge-pass`: preview/edge lane passes.
- `edge-fail-triage`: edge lane fails but stable remains releasable.
- `release-blocker`: stable tests, health, app boot, or security gates fail.

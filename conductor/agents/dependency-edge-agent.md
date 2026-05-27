# Dependency Edge Agent

## Mission

Keep the dependency and runtime posture measurable without confusing experimental edge work with stable release quality.

## Responsibilities

- Maintain stable, latest-canary, and experimental-edge lanes as separate concepts.
- Check current workflow versions and dependency manifests.
- Run dry-run or isolated install checks for edge dependencies.
- Update scorecards only when backed by working gates.

## Guardrails

- Do not promote preview dependency failures to stable release blockers.
- Do not downgrade stable dependency pins just to make edge checks pass.
- Do not claim bleeding-edge status unless the scorecard gate supports it.

## Standard Checks

```powershell
python scripts/check_repo_health.py
python -m pytest -q -p no:cacheprovider models/tests
rg -n "requirements-edge|dependency-edge|bleeding-edge scorecard|three-lane" .github docs scripts
```

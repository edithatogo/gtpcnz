# Plan

1. Baseline `scripts/run_scalene_profile.py` and focused runtime tests.
2. Profile Dash service calls for comparison, uncertainty, stock-flow, and agent-lens paths.
3. Optimize hot loops only where profiling shows material cost.
4. Add bounded regression tests for deterministic outputs after each optimization.
5. Verify `pytest-goblin` before adding it; if no trusted package exists, use established pytest stress/repeat tooling instead.

Required checks:

```powershell
python scripts/run_scalene_profile.py
python -m pytest -q models/tests/test_runtime_lab.py models/tests/test_dashboard_service.py
```


# Acceptance

Required gates:
- `python scripts/build_public_source_snapshot.py`
- `python scripts/check_public_source_snapshot.py`
- `python -m pytest -q models/tests/test_public_source_snapshot.py`
- `python scripts/check_conductor_parallel_tracks.py`

Track is accepted only when:

- all required files listed in the task pack exist or are explicitly marked blocked in `implementation-log.md`;
- every required gate passes, or a not-ready gate returns a non-inflated readiness status without public claim upgrade;
- public outputs remain bounded as benchmark, calibration-readiness, or decision-uncertainty material unless calibration gates pass;
- root/public mirror drift is checked with `python scripts/sync_public_mirror.py --check` when files under `models/primarycare_model/**` changed;
- implementation-log includes subagent handoff notes and residual blockers.

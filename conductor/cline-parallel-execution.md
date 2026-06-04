# Cline Parallel Execution Matrix

Purpose: execute GTPCNZ tracks 050-063 with Cline using DeepSeek v4 Flash while maximizing safe parallelism and minimizing collision risk.

## Scheduling Rule

Maximize breadth inside dependency waves. Do not maximize delegation depth. The recommended maximum is:

- Level 0: coordinator
- Level 1: track lead
- Level 2: work-package subagent

A deeper chain is allowed only when the coordinator creates a new gated work package.

## Waves

- Wave 0: run `python scripts/check_conductor_parallel_tracks.py`, public-only boundary, concern-boundary, and dependency lock gates.
- Wave 1: tracks 050, 051, 052, 058, 062.
- Wave 2: tracks 053, 054, 055, 060.
- Wave 3: tracks 056, 057, 061.
- Wave 4: track 059, release manifest/model card, mirror sync, full gate sweep.
- Wave 5: track 063 release-readiness parallel closeout. Run internal work-package waves 5A, 5B and 5C after 050-062 are complete.

## Collision Rules

- Only one subagent may own a file at a time.
- Shared docs require a track-lead handoff note before editing.
- Any edit under `models/primarycare_model/**` requires `python scripts/sync_public_mirror.py --check` after mirror sync.
- Any output that changes claim level must run calibration, VOI, visual grammar, and release gates.

## Non-Negotiable Claim Boundary

Do not claim precise fiscal savings, ED reductions, hospital-demand reductions, workforce effects, implementation impacts, or causal effects unless the relevant public-data calibration and validation gates pass. Readiness-only outputs must stay labelled readiness-only.

## Coordinator Startup Command Set

```powershell
python scripts/check_conductor_parallel_tracks.py
python scripts/check_public_only_boundary.py
python scripts/check_concern_boundaries.py
python scripts/check_dependency_lock.py
```

## Coordinator Closeout Command Set

```powershell
python scripts/check_conductor_parallel_tracks.py
python scripts/check_public_only_boundary.py
python scripts/check_parameter_traceability.py
python scripts/check_public_source_snapshot.py
python scripts/run_public_aggregate_calibration.py --check-only
python scripts/run_voi.py --check-only
python scripts/run_accessibility_audit.py --check-only
python scripts/generate_release_manifest.py --check-only
python scripts/sync_public_mirror.py --check
python -m pytest -q models/tests/test_conductor_parallel_tracks.py models/tests/test_public_only_boundary.py models/tests/test_parameter_traceability.py models/tests/test_public_source_snapshot.py models/tests/test_public_aggregate_calibration.py models/tests/test_structural_ensemble.py models/tests/test_full_voi.py models/tests/test_streamlit_cockpit_contracts.py models/tests/test_report_artifacts.py models/tests/test_jurisdiction_claims.py models/tests/test_release_engineering.py models/tests/test_public_evidence_monitor.py models/tests/test_dependency_files.py
```

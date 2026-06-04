# Acceptance

Required gates:

- `python scripts/check_conductor_parallel_tracks.py`
- `python scripts/check_public_only_boundary.py`
- `python scripts/check_parameter_traceability.py`
- `python scripts/check_public_source_snapshot.py`
- `python scripts/check_dependency_lock.py`
- `python scripts/check_concern_boundaries.py`
- `python scripts/run_public_aggregate_calibration.py --check-only`
- `python scripts/run_voi.py --check-only`
- `python scripts/run_accessibility_audit.py --check-only`
- `python scripts/generate_release_model_card.py --check-only`
- `python scripts/generate_release_manifest.py --check-only`
- `python scripts/sync_public_mirror.py --check`
- `python -m pytest -q models/tests/test_conductor_parallel_tracks.py models/tests/test_public_only_boundary.py models/tests/test_parameter_traceability.py models/tests/test_public_source_snapshot.py models/tests/test_public_aggregate_calibration.py models/tests/test_structural_ensemble.py models/tests/test_full_voi.py models/tests/test_streamlit_cockpit_contracts.py models/tests/test_report_artifacts.py models/tests/test_jurisdiction_claims.py models/tests/test_release_engineering.py models/tests/test_public_evidence_monitor.py models/tests/test_dependency_files.py`

Acceptance criteria:

- Every work package in `work-packages.md` has a log entry with subagent role, files read or changed, gates run, result, blockers, and follow-on owner.
- Public outputs remain bounded as public benchmark, calibration-readiness, or decision-uncertainty material.
- Full pytest, Quarto, py_compile, and repo-health failures are either passing or classified with exact filesystem/environment errors.
- `public/gtpcnz` status is classified as expected mirror sync, unresolved nested repo drift, or blocker.
- Commit grouping exists and does not require destructive git commands.
- Calibration remains `calibration_readiness_only` unless Track 053 public source readiness and validation gates pass.

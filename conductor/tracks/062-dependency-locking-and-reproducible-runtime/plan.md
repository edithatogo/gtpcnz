# Plan

Execution wave: `1`.

Depends on:
- None

Blocks:
- `059-release-engineering-and-model-cards`

Safe parallel tracks:
- `050-public-only-registry-purification`
- `051-parameter-ontology-and-distributions`
- `052-public-source-ingestion-and-snapshots`
- `058-australia-scope-decision`

Work packages:

| Work package | Subagent role | Task | Contract | Required gate |
|---|---|---|---|---|
| WP-062-A | `lock-surface` | Keep requirements, edge requirements, uv lock, Dockerfile and devcontainer present and consistent. | CON-REL-001 | python scripts/check_dependency_lock.py, python -m pytest -q models/tests/test_dependency_files.py |
| WP-062-B | `dependency-gate` | Fail when dependency files referenced by workflows are absent. | CON-REL-001 | python scripts/check_dependency_lock.py, python -m pytest -q models/tests/test_dependency_files.py |
| WP-062-C | `edge-workflow` | Keep edge workflow non-blocking unless explicitly promoted. | CON-REL-001 | python scripts/check_dependency_lock.py, python -m pytest -q models/tests/test_dependency_files.py |
| WP-062-D | `runtime-docs` | Document reproducible local, CI and deployment runtime expectations. | CON-REL-001 | python scripts/check_dependency_lock.py, python -m pytest -q models/tests/test_dependency_files.py |

Completion sequence:

1. Confirm dependencies have passed their gates.
2. Assign work packages only within the allowed file globs.
3. Run every required gate listed in `acceptance.md`.
4. Update `implementation-log.md` with files changed, commands run, residual blockers, and claim-boundary status.
5. Run `python scripts/check_conductor_parallel_tracks.py` before marking the track ready for release-wave coordination.

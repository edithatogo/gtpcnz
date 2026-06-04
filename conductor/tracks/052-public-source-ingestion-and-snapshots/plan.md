# Plan

Execution wave: `1`.

Depends on:
- `050-public-only-registry-purification`

Blocks:
- `053-public-aggregate-calibration-engine`
- `057-quarto-scientific-report-rebuild`
- `059-release-engineering-and-model-cards`

Safe parallel tracks:
- `051-parameter-ontology-and-distributions`
- `058-australia-scope-decision`
- `062-dependency-locking-and-reproducible-runtime`

Work packages:

| Work package | Subagent role | Task | Contract | Required gate |
|---|---|---|---|---|
| WP-052-A | `source-contracts` | Require URL/reference, retrieval date, licence/access status, checksum, transform and claim boundary. | CON-PUBLIC-001 | python scripts/build_public_source_snapshot.py, python scripts/check_public_source_snapshot.py, python -m pytest -q models/tests/test_public_source_snapshot.py |
| WP-052-B | `snapshot-builder` | Build deterministic snapshot manifests from public registry files only. | CON-PUBLIC-001 | python scripts/build_public_source_snapshot.py, python scripts/check_public_source_snapshot.py, python -m pytest -q models/tests/test_public_source_snapshot.py |
| WP-052-C | `checksum-readiness` | Keep pending checksums as readiness blockers, not calibration success. | CON-PUBLIC-001 | python scripts/build_public_source_snapshot.py, python scripts/check_public_source_snapshot.py, python -m pytest -q models/tests/test_public_source_snapshot.py |
| WP-052-D | `processed-schema` | Document schemas and hash manifests for processed public datasets. | CON-PUBLIC-001 | python scripts/build_public_source_snapshot.py, python scripts/check_public_source_snapshot.py, python -m pytest -q models/tests/test_public_source_snapshot.py |

Completion sequence:

1. Confirm dependencies have passed their gates.
2. Assign work packages only within the allowed file globs.
3. Run every required gate listed in `acceptance.md`.
4. Update `implementation-log.md` with files changed, commands run, residual blockers, and claim-boundary status.
5. Run `python scripts/check_conductor_parallel_tracks.py` before marking the track ready for release-wave coordination.

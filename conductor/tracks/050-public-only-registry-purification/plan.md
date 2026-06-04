# Plan

Execution wave: `1`.

Depends on:
- None

Blocks:
- `051-parameter-ontology-and-distributions`
- `052-public-source-ingestion-and-snapshots`
- `053-public-aggregate-calibration-engine`
- `056-streamlit-policy-cockpit-and-visual-grammar`

Safe parallel tracks:
- `062-dependency-locking-and-reproducible-runtime`

Work packages:

| Work package | Subagent role | Task | Contract | Required gate |
|---|---|---|---|---|
| WP-050-A | `registry-classifier` | Classify every model-facing registry value as public-runtime or excluded-template without changing public claims. | CON-PUBLIC-001 | python scripts/check_public_only_boundary.py, python -m pytest -q models/tests/test_public_only_boundary.py |
| WP-050-B | `quarantine-migration` | Move sensitive/confidential/linked-data/stakeholder examples into templates marked excluded from public runtime. | CON-PUBLIC-001 | python scripts/check_public_only_boundary.py, python -m pytest -q models/tests/test_public_only_boundary.py |
| WP-050-C | `boundary-gate` | Harden `scripts/check_public_only_boundary.py` against forbidden values and self-reference false positives. | CON-PUBLIC-001 | python scripts/check_public_only_boundary.py, python -m pytest -q models/tests/test_public_only_boundary.py |
| WP-050-D | `mirror-and-tests` | Synchronise public registries into the public mirror and prove the gate/test pair passes. | CON-PUBLIC-001 | python scripts/check_public_only_boundary.py, python -m pytest -q models/tests/test_public_only_boundary.py |

Completion sequence:

1. Confirm dependencies have passed their gates.
2. Assign work packages only within the allowed file globs.
3. Run every required gate listed in `acceptance.md`.
4. Update `implementation-log.md` with files changed, commands run, residual blockers, and claim-boundary status.
5. Run `python scripts/check_conductor_parallel_tracks.py` before marking the track ready for release-wave coordination.

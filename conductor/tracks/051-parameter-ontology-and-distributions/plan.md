# Plan

Execution wave: `1`.

Depends on:
- `050-public-only-registry-purification`

Blocks:
- `053-public-aggregate-calibration-engine`
- `054-structural-uncertainty-ensemble`
- `055-full-value-of-information-engine`

Safe parallel tracks:
- `052-public-source-ingestion-and-snapshots`
- `058-australia-scope-decision`
- `062-dependency-locking-and-reproducible-runtime`

Work packages:

| Work package | Subagent role | Task | Contract | Required gate |
|---|---|---|---|---|
| WP-051-A | `ontology-contract` | Expand strict parameter fields, distributions, bounds, formula refs, and claim-boundary metadata. | CON-PARAM-001 | python scripts/check_parameter_traceability.py, python -m pytest -q models/tests/test_parameter_traceability.py |
| WP-051-B | `loader-defaults` | Keep public runtime defaults loaded only from `registries/public/parameters.public.v1.yaml`. | CON-PARAM-001 | python scripts/check_parameter_traceability.py, python -m pytest -q models/tests/test_parameter_traceability.py |
| WP-051-C | `formula-trace` | Link every formula coefficient to a public parameter id and document gaps as not-ready. | CON-PARAM-001 | python scripts/check_parameter_traceability.py, python -m pytest -q models/tests/test_parameter_traceability.py |
| WP-051-D | `traceability-tests` | Add failing tests for any missing distribution, source, bound, or formula reference. | CON-PARAM-001 | python scripts/check_parameter_traceability.py, python -m pytest -q models/tests/test_parameter_traceability.py |

Completion sequence:

1. Confirm dependencies have passed their gates.
2. Assign work packages only within the allowed file globs.
3. Run every required gate listed in `acceptance.md`.
4. Update `implementation-log.md` with files changed, commands run, residual blockers, and claim-boundary status.
5. Run `python scripts/check_conductor_parallel_tracks.py` before marking the track ready for release-wave coordination.

# Plan

Execution wave: `1`.

Depends on:
- None

Blocks:
- `056-streamlit-policy-cockpit-and-visual-grammar`
- `057-quarto-scientific-report-rebuild`

Safe parallel tracks:
- `051-parameter-ontology-and-distributions`
- `052-public-source-ingestion-and-snapshots`
- `062-dependency-locking-and-reproducible-runtime`

Work packages:

| Work package | Subagent role | Task | Contract | Required gate |
|---|---|---|---|---|
| WP-058-A | `scope-decision` | State whether AU is first-class or comparative context only. | CON-PUBLIC-001 | python -m pytest -q models/tests/test_jurisdiction_claims.py |
| WP-058-B | `jurisdiction-registry` | Register jurisdiction status and claim boundary. | CON-PUBLIC-001 | python -m pytest -q models/tests/test_jurisdiction_claims.py |
| WP-058-C | `unsupported-claim-scan` | Remove or downgrade unsupported Australia model claims. | CON-PUBLIC-001 | python -m pytest -q models/tests/test_jurisdiction_claims.py |
| WP-058-D | `scope-tests` | Test AU comparative-only status unless AU-specific public artefacts exist. | CON-PUBLIC-001 | python -m pytest -q models/tests/test_jurisdiction_claims.py |

Completion sequence:

1. Confirm dependencies have passed their gates.
2. Assign work packages only within the allowed file globs.
3. Run every required gate listed in `acceptance.md`.
4. Update `implementation-log.md` with files changed, commands run, residual blockers, and claim-boundary status.
5. Run `python scripts/check_conductor_parallel_tracks.py` before marking the track ready for release-wave coordination.

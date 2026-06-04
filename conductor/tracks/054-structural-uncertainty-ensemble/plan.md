# Plan

Execution wave: `2`.

Depends on:
- `050-public-only-registry-purification`
- `051-parameter-ontology-and-distributions`

Blocks:
- `056-streamlit-policy-cockpit-and-visual-grammar`
- `057-quarto-scientific-report-rebuild`

Safe parallel tracks:
- `053-public-aggregate-calibration-engine`
- `055-full-value-of-information-engine`
- `060-self-learning-public-evidence-monitor`

Work packages:

| Work package | Subagent role | Task | Contract | Required gate |
|---|---|---|---|---|
| WP-054-A | `dag-registry` | Maintain at least eight structural DAG entries with edges, exclusions, weights and source basis. | CON-UNC-001 | python -m pytest -q models/tests/test_structural_ensemble.py |
| WP-054-B | `ensemble-runner` | Report structural intervals as assumption sensitivity only. | CON-UNC-001 | python -m pytest -q models/tests/test_structural_ensemble.py |
| WP-054-C | `diagram-docs` | Keep Mermaid DAG docs aligned with registry structures. | CON-UNC-001 | python -m pytest -q models/tests/test_structural_ensemble.py |
| WP-054-D | `uncertainty-tests` | Test required models, interval shape, and claim-boundary labels. | CON-UNC-001 | python -m pytest -q models/tests/test_structural_ensemble.py |

Completion sequence:

1. Confirm dependencies have passed their gates.
2. Assign work packages only within the allowed file globs.
3. Run every required gate listed in `acceptance.md`.
4. Update `implementation-log.md` with files changed, commands run, residual blockers, and claim-boundary status.
5. Run `python scripts/check_conductor_parallel_tracks.py` before marking the track ready for release-wave coordination.

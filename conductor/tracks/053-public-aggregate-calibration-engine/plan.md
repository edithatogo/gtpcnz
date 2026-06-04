# Plan

Execution wave: `2`.

Depends on:
- `050-public-only-registry-purification`
- `051-parameter-ontology-and-distributions`
- `052-public-source-ingestion-and-snapshots`

Blocks:
- `056-streamlit-policy-cockpit-and-visual-grammar`
- `057-quarto-scientific-report-rebuild`
- `059-release-engineering-and-model-cards`

Safe parallel tracks:
- `054-structural-uncertainty-ensemble`
- `055-full-value-of-information-engine`
- `060-self-learning-public-evidence-monitor`

Work packages:

| Work package | Subagent role | Task | Contract | Required gate |
|---|---|---|---|---|
| WP-053-A | `target-registry` | Define public aggregate targets and validation gates by family. | CON-CAL-001 | python scripts/run_public_aggregate_calibration.py --check-only, python -m pytest -q models/tests/test_public_aggregate_calibration.py |
| WP-053-B | `calibration-runner` | Implement transparent public-only calibration that downgrades when public source readiness fails. | CON-CAL-001 | python scripts/run_public_aggregate_calibration.py --check-only, python -m pytest -q models/tests/test_public_aggregate_calibration.py |
| WP-053-C | `ppc-and-holdouts` | Add baseline, temporal, subgroup/geographic, and PPC hooks where public data permit. | CON-CAL-001 | python scripts/run_public_aggregate_calibration.py --check-only, python -m pytest -q models/tests/test_public_aggregate_calibration.py |
| WP-053-D | `claim-downgrade` | Prove failed or missing gates force `public_benchmark` status and not-valid-for warnings. | CON-CAL-001 | python scripts/run_public_aggregate_calibration.py --check-only, python -m pytest -q models/tests/test_public_aggregate_calibration.py |

Completion sequence:

1. Confirm dependencies have passed their gates.
2. Assign work packages only within the allowed file globs.
3. Run every required gate listed in `acceptance.md`.
4. Update `implementation-log.md` with files changed, commands run, residual blockers, and claim-boundary status.
5. Run `python scripts/check_conductor_parallel_tracks.py` before marking the track ready for release-wave coordination.

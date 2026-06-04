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
- `054-structural-uncertainty-ensemble`
- `060-self-learning-public-evidence-monitor`

Work packages:

| Work package | Subagent role | Task | Contract | Required gate |
|---|---|---|---|---|
| WP-055-A | `normative-net-benefit` | Keep weights editable and labelled as normative assumptions, not stakeholder preferences. | CON-VOI-001 | python scripts/run_voi.py --check-only, python -m pytest -q models/tests/test_full_voi.py |
| WP-055-B | `voi-metrics` | Implement EVPI, EVPPI, EVSI, ENBS, decision-error probability and rankings. | CON-VOI-001 | python scripts/run_voi.py --check-only, python -m pytest -q models/tests/test_full_voi.py |
| WP-055-C | `seeded-reproducibility` | Make stochastic VOI deterministic under a fixed seed. | CON-VOI-001 | python scripts/run_voi.py --check-only, python -m pytest -q models/tests/test_full_voi.py |
| WP-055-D | `voi-tests` | Test metric completeness, reproducibility, and `not a forecast` labelling. | CON-VOI-001 | python scripts/run_voi.py --check-only, python -m pytest -q models/tests/test_full_voi.py |

Completion sequence:

1. Confirm dependencies have passed their gates.
2. Assign work packages only within the allowed file globs.
3. Run every required gate listed in `acceptance.md`.
4. Update `implementation-log.md` with files changed, commands run, residual blockers, and claim-boundary status.
5. Run `python scripts/check_conductor_parallel_tracks.py` before marking the track ready for release-wave coordination.

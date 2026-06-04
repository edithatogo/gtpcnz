# Plan

Execution wave: `4`.

Depends on:
- `052-public-source-ingestion-and-snapshots`
- `056-streamlit-policy-cockpit-and-visual-grammar`
- `057-quarto-scientific-report-rebuild`
- `061-visual-regression-accessibility-and-browser-tests`
- `062-dependency-locking-and-reproducible-runtime`

Blocks:
- None

Safe parallel tracks:
- None

Work packages:

| Work package | Subagent role | Task | Contract | Required gate |
|---|---|---|---|---|
| WP-059-A | `version-consistency` | Align VERSION, pyproject, app version and generated artefact names. | CON-REL-001 | python scripts/check_version_consistency.py, python scripts/generate_release_model_card.py --check-only, python scripts/generate_release_manifest.py --check-only, python -m pytest -q models/tests/test_release_engineering.py |
| WP-059-B | `model-card` | Generate claim-gated model card with source and not-valid-for fields. | CON-REL-001 | python scripts/check_version_consistency.py, python scripts/generate_release_model_card.py --check-only, python scripts/generate_release_manifest.py --check-only, python -m pytest -q models/tests/test_release_engineering.py |
| WP-059-C | `release-manifest` | Generate hashes for source snapshot, parameters, model, outputs and gate statuses. | CON-REL-001 | python scripts/check_version_consistency.py, python scripts/generate_release_model_card.py --check-only, python scripts/generate_release_manifest.py --check-only, python -m pytest -q models/tests/test_release_engineering.py |
| WP-059-D | `ci-release-gates` | Wire public-only, calibration, VOI, visual, accessibility and release gates into CI. | CON-REL-001 | python scripts/check_version_consistency.py, python scripts/generate_release_model_card.py --check-only, python scripts/generate_release_manifest.py --check-only, python -m pytest -q models/tests/test_release_engineering.py |

Completion sequence:

1. Confirm dependencies have passed their gates.
2. Assign work packages only within the allowed file globs.
3. Run every required gate listed in `acceptance.md`.
4. Update `implementation-log.md` with files changed, commands run, residual blockers, and claim-boundary status.
5. Run `python scripts/check_conductor_parallel_tracks.py` before marking the track ready for release-wave coordination.

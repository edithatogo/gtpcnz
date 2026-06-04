# Release Readiness Commit Plan - WP-063-D

**Track:** 063-release-readiness-parallel-closeout  
**Role:** commit-packager  
**Run date:** 2026-06-04  
**Scope:** non-destructive grouping plan only; no staging, commits, resets, checkouts, or submodule rewrites.

## Executive Summary

The working tree contains the broad 050-063 implementation set: modified tracked files, many new track/code/test/doc artifacts, and a dirty `public/gtpcnz` mirror. The plan below groups the changes into reviewable slices while preserving the current public claim boundary: `public_benchmark` and `calibration_readiness_only`.

Do not include `data/linked-nz/` in the public model commit set. Treat it as non-public/future-linked-data material unless separately quarantined and reviewed. Treat `public/gtpcnz` as mirror/submodule work requiring a separate mirror-specific review.

## Commit Group 1: Conductor Infrastructure

Purpose: commit the governance spine and parallel execution material.

Include:

- `conductor/tracks/050-*` through `conductor/tracks/063-*`
- `conductor/agents/cline-subagent-coordinator.md`
- `conductor/agents/public-calibration-agent.md`
- `conductor/agents/voi-uncertainty-agent.md`
- `conductor/prompts/deepseek-v4-flash-subagent-template.md`
- `conductor/skills/public-only-calibration-skill.md`
- `conductor/workflows/cline-deepseek-parallel.md`
- `conductor/workflows/reproduce-public-release.md`
- `conductor/parallel-execution-matrix.json`
- `conductor/cline-parallel-execution.md`

Suggested message: `feat(conductor): add public-model parallel execution tracks`

## Commit Group 2: Public Registries And Contracts

Purpose: establish the public-only runtime boundary and typed registry contracts.

Include:

- `models/primarycare_model/registries/public/`
- `models/primarycare_model/registries/templates/`
- `models/primarycare_model/contracts/calibration_targets.py`
- `models/primarycare_model/contracts/evidence_candidates.py`
- `models/primarycare_model/contracts/public_parameters.py`
- `models/primarycare_model/contracts/public_sources.py`
- `models/primarycare_model/contracts/structural_models.py`
- `models/primarycare_model/contracts/voi.py`
- `data/public_raw/README.md`
- `data/public_processed/README.md`
- `data/snapshots/`

Suggested message: `feat(registries): add public-only registries and contracts`

## Commit Group 3: Model Engines

Purpose: commit public aggregate calibration readiness, structural uncertainty, VOI, evidence monitoring, and public source snapshot code.

Include:

- `models/primarycare_model/calibration/`
- `models/primarycare_model/data/`
- `models/primarycare_model/evidence/`
- `models/primarycare_model/uncertainty/`
- `models/primarycare_model/voi/`
- `models/primarycare_model/validation/public_parameter_loader.py`
- `models/primarycare_model/version.py`

Suggested message: `feat(model): add public calibration readiness and uncertainty engines`

## Commit Group 4: UI, Scripts, And Tests

Purpose: commit the policy cockpit modules, gates, browser scaffolds, and test coverage.

Include:

- `models/primarycare_model/ui/`
- `models/tests/test_conductor_parallel_tracks.py`
- `models/tests/test_dependency_files.py`
- `models/tests/test_full_voi.py`
- `models/tests/test_jurisdiction_claims.py`
- `models/tests/test_parameter_traceability.py`
- `models/tests/test_public_aggregate_calibration.py`
- `models/tests/test_public_evidence_monitor.py`
- `models/tests/test_public_only_boundary.py`
- `models/tests/test_public_source_snapshot.py`
- `models/tests/test_release_engineering.py`
- `models/tests/test_report_artifacts.py`
- `models/tests/test_streamlit_cockpit_contracts.py`
- `models/tests/test_streamlit_dashboard_app.py`
- `models/tests/test_structural_ensemble.py`
- `scripts/build_public_source_snapshot.py`
- `scripts/check_conductor_parallel_tracks.py`
- `scripts/check_dependency_lock.py`
- `scripts/check_parameter_traceability.py`
- `scripts/check_public_only_boundary.py`
- `scripts/check_public_source_snapshot.py`
- `scripts/check_version_consistency.py`
- `scripts/generate_release_manifest.py`
- `scripts/generate_release_model_card.py`
- `scripts/monitor_public_evidence.py`
- `scripts/render_public_model_report.py`
- `scripts/run_accessibility_audit.py`
- `scripts/run_public_aggregate_calibration.py`
- `scripts/run_visual_regression.py`
- `scripts/run_voi.py`
- `tests/browser/`

Suggested message: `feat(ui,tests): add policy cockpit contracts and release gates`

## Commit Group 5: Documentation And Reports

Purpose: commit user-facing and release-facing documentation that explains the public-data-only calibration-readiness posture.

Include:

- `docs/calibration/public-aggregate-calibration-methods-v1.md`
- `docs/decisions/australia-scope-decision-v1.md`
- `docs/diagrams/`
- `docs/evidence/`
- `docs/model/`
- `docs/public-site/site-map-and-release-manifest-v1.8.4.md`
- `docs/release/`
- `docs/testing/`
- `docs/visualisation/`
- `reports/public_aggregate_model_report.qmd`

Review before including:

- `docs/review/` OpenAlex artifacts if they are unrelated to the public-model closeout.
- `docs/skills/streamlit-apptest/` and `docs/skills/streamlit-dashboard/` if they are local skill scaffolds rather than project docs.

Suggested message: `docs: add public-model readiness and release documentation`

## Commit Group 6: Modified Tracked Runtime And Governance Files

Purpose: commit modifications to existing tracked files after the new files above have been reviewed.

Include, subject to manual review:

- `.github/workflows/ci.yml`
- `.github/workflows/pages.yml`
- `.gitignore`
- `Makefile`
- `README.md`
- `_quarto.yml`
- `conductor/state.md`
- `conductor/tracks.md`
- modified existing conductor track metadata and plans
- `data/dataset-registry.json`
- modified existing docs under `docs/`
- `index.qmd`
- `models/primarycare_model/app.py`
- `models/primarycare_model/runtime_lab.py`
- `models/primarycare_model/scenario_service.py`
- `models/primarycare_model/validation/arrow_schemas.py`
- modified existing tests under `models/tests/`
- `pyproject.toml`
- `reports/primary_care_architecture.qmd`
- `scripts/check_no_patient_data.py`
- `scripts/sync_public_mirror.py`

Manual review is mandatory for:

- `models/primarycare_model/app.py` - large Streamlit restructuring and cockpit delegation.
- `conductor/state.md` - status must not overstate calibration or public-release readiness.
- `models/primarycare_model/scenario_service.py` - dynamic claim-boundary fallback must not upgrade claims.

Suggested message: `chore: wire public-model release readiness into existing surfaces`

## Commit Group 7: Runtime Reproducibility Infrastructure

Purpose: commit environment and dependency files separately because they can affect local, CI, and deployment behavior.

Include:

- `.devcontainer/`
- `Dockerfile`
- `requirements-edge.txt`
- `uv.lock`

Suggested message: `chore(runtime): add reproducible runtime and edge dependency files`

## Exclusions And Separate Handling

Exclude from initial public-model commit wave:

- `data/linked-nz/` - linked-data material; not part of the public runtime path.
- `public/gtpcnz` - dirty mirror/submodule; review and commit/publish through the mirror workflow only.
- `_site/` and other rendered/transient outputs unless release policy explicitly requires checked-in render artifacts.
- `__pycache__/`, pytest cache, local temp directories, and other generated artifacts.
- `index.html` deletion should be reviewed against the Quarto/Pages publishing strategy before committing.

## Gate Expectations Before Final Commit

Run the deterministic gates after any manual edits and before staging:

```powershell
python scripts/check_conductor_parallel_tracks.py
python scripts/check_public_only_boundary.py
python scripts/check_parameter_traceability.py
python scripts/check_public_source_snapshot.py
python scripts/check_dependency_lock.py
python scripts/check_concern_boundaries.py
python scripts/run_public_aggregate_calibration.py --check-only
python scripts/run_voi.py --check-only
python scripts/run_accessibility_audit.py --check-only
python scripts/generate_release_model_card.py --check-only
python scripts/generate_release_manifest.py --check-only
python scripts/sync_public_mirror.py --check
python -m pytest -q models/tests/test_conductor_parallel_tracks.py models/tests/test_public_only_boundary.py models/tests/test_parameter_traceability.py models/tests/test_public_source_snapshot.py models/tests/test_public_aggregate_calibration.py models/tests/test_structural_ensemble.py models/tests/test_full_voi.py models/tests/test_streamlit_cockpit_contracts.py models/tests/test_report_artifacts.py models/tests/test_jurisdiction_claims.py models/tests/test_release_engineering.py models/tests/test_public_evidence_monitor.py models/tests/test_dependency_files.py
```

All successful gate results remain readiness-only unless public source retrieval, checksums, transformations, calibration targets, and validation gates are completed.

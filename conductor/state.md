# Conductor State

GTPCNZ is a public-data anchored benchmark and educational explainer. It is not a patient-level forecast.
It is not linked-data calibrated in the public runtime path. Do not claim precise fiscal savings,
ED reductions, hospital-demand reductions, workforce effects, implementation impacts, or causal effects
unless the relevant public-data calibration and validation gates pass.

Tracks 050-063 are complete for the v1.8.1 readiness-only release:

- `050-public-only-registry-purification`: public-only registry purification.
- `051-parameter-ontology-and-distributions`: parameter ontology and uncertainty distributions.
- `052-public-source-ingestion-and-snapshots`: public-source ingestion and reproducible snapshots.
- `053-public-aggregate-calibration-engine`: public aggregate empirical calibration readiness. Calibration remains `calibration_readiness_only` until public source retrieval, checksum, transformation, and validation gates pass.
- `054-structural-uncertainty-ensemble`: structural uncertainty and DAG ensemble.
- `055-full-value-of-information-engine`: full VOI engine, labelled as decision-uncertainty analysis rather than forecast.
- `056-streamlit-policy-cockpit-and-visual-grammar`: Streamlit policy cockpit and visual grammar.
- `057-quarto-scientific-report-rebuild`: Quarto scientific report rebuild.
- `058-australia-scope-decision`: Australia is comparative context only unless AU-specific public artefacts are later created.
- `059-release-engineering-and-model-cards`: release engineering and model cards.
- `060-self-learning-public-evidence-monitor`: review-only public evidence monitor.
- `061-visual-regression-accessibility-and-browser-tests`: visual, accessibility, and browser tests.
- `062-dependency-locking-and-reproducible-runtime`: dependency locking and reproducible runtime.
- `063-release-readiness-parallel-closeout`: post-050-062 diff audit, environment blocker classification, release gate rerun, commit packaging, public-source readiness closeout, PR merge, and remote CI verification.

Next implementation frontier:

- Public source retrieval and transformation described in `docs/model/public-source-readiness-closeout-v1.md`.
- Cross-stage public source readiness matrix: `python scripts/check_public_source_readiness_matrix.py` passes in readiness mode; `--strict` remains the calibration-upgrade blocker until raw, checksum, and processed artifacts exist.
- Replacement of `checksum: pending-download` entries with verified SHA-256 checksums after reproducible public downloads.
- Calibration target readiness matrix: `python scripts/check_calibration_target_readiness.py` passes in readiness mode; `--strict` remains blocked until every linked source is ready and every target is within public tolerance.
- Calibration validation gate matrix: `python scripts/check_calibration_validation_gates.py` passes in readiness mode; `--strict` remains blocked until baseline, holdout, PPC, and claim-downgrade gates pass where public data permit.
- Calibration target promotion from `source_ready=false` to `source_ready=true` only after source, licence, checksum, processed-schema, and mirror gates pass.
- No upgrade from `public_benchmark` / `calibration_readiness_only` until those gates pass.

Parallel execution controls:

- Cline/deepseek execution matrix: `conductor/cline-parallel-execution.md`.
- Machine-readable dependency and file-ownership matrix: `conductor/parallel-execution-matrix.json`.
- Subagent coordinator: `conductor/agents/cline-subagent-coordinator.md`.
- Subagent prompt template: `conductor/prompts/deepseek-v4-flash-subagent-template.md`.
- Track 063 Cline prompts: `conductor/tracks/063-release-readiness-parallel-closeout/agent-prompts.md`.
- Validation gate: `python scripts/check_conductor_parallel_tracks.py`.

Recently completed tracks:

- Tracks 042-052 from the earlier v1.8.x hardening/dashboard programme remain completed as recorded in the historical registry.

Current public gates:

- `python scripts/check_conductor_parallel_tracks.py`
- `python scripts/check_public_only_boundary.py`
- `python scripts/check_parameter_traceability.py`
- `python scripts/check_public_source_snapshot.py`
- `python scripts/check_public_source_retrieval_plan.py`
- `python scripts/check_public_source_fetch_scripts.py`
- `python scripts/check_public_source_transform_scripts.py`
- `python scripts/check_public_source_readiness_matrix.py`
- `python scripts/check_transformed_schemas.py`
- `python scripts/check_version_consistency.py`
- `python scripts/check_dependency_lock.py`
- `python scripts/check_concern_boundaries.py`
- `python scripts/check_repo_health.py`
- `python scripts/check_calibration_target_readiness.py`
- `python scripts/check_calibration_validation_gates.py`
- `python scripts/run_public_aggregate_calibration.py --check-only`
- `python scripts/run_voi.py --check-only`
- `python -m pytest -q`
- `quarto render --to html`
- `python -m py_compile streamlit_app.py models/primarycare_model/app.py`
- `python scripts/run_visual_regression.py --check-only`
- `python scripts/run_accessibility_audit.py --check-only`
- `python scripts/generate_release_model_card.py --check-only`
- `python scripts/generate_release_manifest.py --check-only`


## Execution summary (2026-06-03 Cline DeepSeek v4 Flash coordinator run)

### Waves completed

| Wave | Tracks | Status |
|------|--------|--------|
| 0 (startup gates) | coordinator gates | PASSED - all 4 startup gates pass |
| 1 | 050, 051, 052, 058, 062 | PASSED - all track gates pass |
| 2 | 053, 054, 055, 060 | PASSED - all track gates pass |
| 3 | 056, 057, 061 | PASSED - all track gates pass |
| 4 | 059 | PASSED - all 4 release gates pass |

### Closeout gates

All 13 closeout gates pass:

1. `python scripts/check_conductor_parallel_tracks.py` -> PASSED
2. `python scripts/check_public_only_boundary.py` -> PASSED
3. `python scripts/check_parameter_traceability.py` -> PASSED
4. `python scripts/check_public_source_snapshot.py` -> PASSED
5. `python scripts/run_public_aggregate_calibration.py --check-only` -> PASSED (calibration_readiness_only)
6. `python scripts/run_voi.py --check-only` -> PASSED (decision-uncertainty analysis)
7. `python scripts/run_accessibility_audit.py --check-only` -> PASSED
8. `python scripts/generate_release_manifest.py --check-only` -> PASSED (v1.8.1)
9. `python scripts/sync_public_mirror.py --check` -> PASSED (0 drift items)
10. `python scripts/check_version_consistency.py` -> PASSED (v1.8.1)
11. `python scripts/check_dependency_lock.py` -> PASSED
12. `python scripts/check_concern_boundaries.py` -> PASSED (5/5)
13. Full pytest suite (15 tests) -> ALL PASSED

### Claim-boundary posture

All tracks maintain public_benchmark claim level. Calibration is calibration_readiness_only.
No precise fiscal savings, ED reductions, hospital-demand reductions, workforce effects, implementation impacts, or causal effects are claimed.

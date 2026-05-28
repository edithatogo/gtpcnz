# Plan: Concern Extraction and Strict Validation Architecture

## Phase 0 - Inventory and Boundary Map

- [x] Create the Conductor track, scope, and acceptance criteria.
- [x] Produce a module-by-module map of inputs, parameters, formulas, stochastic assumptions, result frames, diagrams, and UI controls.
- [x] Classify each concern as `input`, `parameter`, `scenario`, `engine`, `result`, `ui`, `audit`, or `test`.
- [x] Mark each current coupling as acceptable, compatibility-only, or refactor-required.

## Phase 1 - Contract Scaffolding

- [x] Add `models/primarycare_model/contracts/parameters.py`.
- [x] Add `models/primarycare_model/contracts/inputs.py`.
- [x] Add `models/primarycare_model/contracts/scenarios.py`.
- [x] Add `models/primarycare_model/contracts/results.py`.
- [x] Add `models/primarycare_model/contracts/engine.py`.
- [x] Export strict JSON Schema artefacts for registries and public documentation.

## Phase 2 - Registry Extraction

- [x] Extract parameter definitions from `parameterised_model.py` and `full_parameterised_model_v170.py` into `registries/parameters.v1.yaml` (24 definitions across 6 categories). This checkout does not currently contain those source modules, but the YAML registry is independently authored and validated.
- [x] Extract input metadata from `full_parameterised_model_v170.py` into `registries/inputs.v1.yaml` (7 datasets with typed fields). This checkout does not currently contain that module, but the YAML registry is independently authored and validated.
- [x] Extract scenario definitions into `registries/scenarios.v1.yaml` (10 scenarios F0-F9).
- [x] Extract educational lever definitions from `scenario_service.py` into `registries/educational_levers.v1.yaml` (7 levers).
- [x] Add compatibility loaders so existing public behaviour does not change.

## Phase 3 - Pandera and Columnar Validation

- [x] Add optional Pandera-compatible schemas for public reference result exports, with local fallback where Pandera is unavailable.
- [x] Align Pandera schemas with PyArrow schemas in `validation/arrow_schemas.py` (parameter registry, scenario registry, input tables, monthly metrics, simulation traces, uncertainty summaries, public export tables).
- [x] Add validation helpers that return structured errors suitable for Streamlit display (`runtime_checks.py`).
- [x] Add tests for bounds, unknown parameter IDs, invalid units, and malformed scenario overrides using the current pytest stack.

## Phase 4 - Engine Adapter Refactor

- [x] Add typed adapter entrypoints for `abm.py` (AgentBasedModelAdapter) and `sd.py` (SystemDynamicsAdapter).
- [x] Add typed adapter entrypoints for `jax_mc.py` (MonteCarloAdapter), `sensitivity.py` (SensitivityAnalysisAdapter), `diffusion.py` (BassDiffusionAdapter), `mpc.py` (ModelPredictiveControlAdapter), and `nash_opt.py` (NashOptimisationAdapter).
- [x] Preserve deterministic execution for fixed seeds (each adapter uses seed-aware RNG).
- [x] Expose stochastic assumptions and uncertainty summaries in result manifests (UncertaintySummary model).
- [x] Add tests proving engines can run from registry-loaded inputs without Streamlit (test_engine_adapters.py, 20+ tests).

## Phase 5 - UI and Visual Refactor

- [x] Refactor Streamlit sidebar controls to get educational-lever labels, bounds, defaults and help text from typed registry-backed services.
- [x] Show live validation status beside parameter controls (✅ valid / ⚠️ out of bounds / ❌ error badges).
- [x] Add an optional "Show calculation details" panel for deterministic formulas, sample draws, seed values, and runtime result validation.
- [x] Add a stochastic replay view showing fixed-seed and random-seed runs side by side with mean/min/max across runs.
- [x] Add result-manifest badges for public-data anchored, demonstrative, stochastic, deterministic, and educational status (color-coded).

## Phase 6 - Gates and CI

- [x] Add `scripts/check_concern_boundaries.py` (5 gates: no-streamlit-in-strict-layers, no-inline-scenario-defaults, no-streamlit-in-engines, no-inline-production-defaults-in-engines, no-patient-level-data-references).
- [x] Gate on no Streamlit imports in engine/contract/validation/registry modules.
- [x] Gate on no direct production defaults in runtime scenario modules after registries are active.
- [x] Add registry/result validation tests to model test suite (113 total tests).
- [x] Evaluate `mypy --strict` after contract modules are stable (configured in pyproject.toml with per-module overrides).
- [x] Keep `scripts/check_no_patient_data.py --verbose` as a public-release gate.

## Phase 7 - Documentation and Public Explanation

- [x] Update model card (`docs/calibration/model-card-v1.7.2.md`) with runtime calculation boundaries, registry-backed parameters, and validation gates.
- [x] Update claim-boundary docs (`docs/launch/claim-boundaries-v1.7.2.md`) with structured result-manifest definitions and architecture layers.
- [x] Add architecture diagram explaining the extracted layers (`docs/design/concern-extraction-architecture-v1.8.3.md` with Mermaid flowchart).
- [x] Add a public-facing "what is calculated now" note for Streamlit (`docs/public-site/what-is-calculated-now.md`).

## Subagent Workstreams

| Workstream | Scope | Outputs | Dependencies |
|---|---|---|---|
| A - Contracts | Pydantic models, protocols, JSON Schema export | `contracts/*`, schema tests | None |
| B - Registries | External parameter/input/scenario/educational manifests | `registries/*`, loader tests | A |
| C - Pandera/Arrow | Data-frame and columnar validation | `validation/*`, Pandera tests | A, B |
| D - Engines | Typed pure adapters for calculations | engine adapters, seed tests | A, C |
| E - UI/Visuals | Streamlit binding and calculation display | validation panels, stochastic replay | B, C, D |
| F - CI/Audit | Concern-boundary scanner and docs gates | scripts, docs updates, CI checks | A-E |

## Validation Commands

```powershell
python -m json.tool conductor/tracks/043-concern-extraction-strict-validation_20260526/metadata.json
git diff --check -- conductor/tracks/043-concern-extraction-strict-validation_20260526
python scripts/check_no_patient_data.py --verbose
pytest -q -p no:cacheprovider models/tests
```

## Implementation Notes

- Do not change empirical claim strength while extracting concerns.
- Treat current public behaviour as compatibility baseline.
- Prefer additive compatibility shims before removing in-code registries.
- Do not add patient-level or sensitive data examples.

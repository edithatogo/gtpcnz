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

- [ ] Extract parameter definitions from `parameterised_model.py` and `full_parameterised_model_v170.py` into `registries/parameters.v1.*`. This checkout does not currently contain those modules.
- [ ] Extract input metadata from `full_parameterised_model_v170.py` into `registries/inputs.v1.*`. This checkout does not currently contain that module.
- [x] Extract scenario definitions into `registries/scenarios.v1.*`.
- [x] Extract educational lever definitions from `scenario_service.py` into `registries/educational_levers.v1.*`.
- [x] Add compatibility loaders so existing public behaviour does not change.

## Phase 3 - Pandera and Columnar Validation

- [x] Add optional Pandera-compatible schemas for public reference result exports, with local fallback where Pandera is unavailable.
- [ ] Align Pandera schemas with existing PyArrow schemas in `data_layer.py`. This checkout does not currently contain that module.
- [x] Add validation helpers that return structured errors suitable for Streamlit display.
- [x] Add tests for bounds, unknown parameter IDs, invalid units, and malformed scenario overrides using the current pytest stack.

## Phase 4 - Engine Adapter Refactor

- [ ] Add typed adapter entrypoints for `abm.py` and `sd.py`.
- [ ] Add typed adapter entrypoints for `jax_mc.py`, `sensitivity.py`, `diffusion.py`, `mpc.py`, and `nash_opt.py`.
- [ ] Preserve deterministic execution for fixed seeds.
- [ ] Expose stochastic assumptions and uncertainty summaries in result manifests.
- [ ] Add tests proving engines can run from registry-loaded inputs without Streamlit.

## Phase 5 - UI and Visual Refactor

- [x] Refactor Streamlit sidebar controls to get educational-lever labels, bounds, defaults and help text from typed registry-backed services.
- [ ] Show live validation status beside parameter controls.
- [ ] Add an optional "show calculation" panel for deterministic formulas, sample draws, seed values, and runtime result validation.
- [ ] Add a stochastic replay view showing fixed-seed and random-seed runs side by side.
- [ ] Add result-manifest badges for public-data anchored, demonstrative, stochastic, deterministic, and linked-data-calibrated status.

## Phase 6 - Gates and CI

- [x] Add `scripts/check_concern_boundaries.py`.
- [x] Gate on no Streamlit imports in engine/contract/validation/registry modules.
- [x] Gate on no direct production defaults in runtime scenario modules after registries are active.
- [x] Add registry/result validation tests to model test suite.
- [ ] Evaluate `mypy --strict` or Pyright after contract modules are stable.
- [ ] Keep `scripts/check_no_patient_data.py --verbose` as a public-release gate.

## Phase 7 - Documentation and Public Explanation

- [ ] Update model card with runtime calculation, deterministic/stochastic, and validation boundaries.
- [ ] Update claim-boundary docs with structured result-manifest definitions.
- [ ] Add an architecture diagram explaining the extracted layers.
- [ ] Add a public-facing "what is calculated now" note for Streamlit.

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

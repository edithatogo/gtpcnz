# Implementation Plan: Direct SOTA Migration (Polars, PyArrow, Pydantic, JAX, Strict Typing)

This plan details the direct migration of the core codebase away from the experimental lane, directly incorporating `polars`, `pyarrow`, `pydantic` (v2), planned `jax` integration, and strict type checking.

## User Review Required

> [!WARNING]
> **API Refactoring:** Replaces `pandas` with `polars` across core components. This will require updating syntax like `.iloc`, `.loc`, and DataFrame instantiation.
> **Dependency Update:** Installs `polars`, `pyarrow`, and `pydantic` as production dependencies in `requirements.txt` and `pyproject.toml`; keeps `jax` as a planned solver dependency until the runtime code path is implemented.

---

## Proposed Changes

### 1. Dependency Configurations
#### [MODIFY] [pyproject.toml](file:///C:/Users/60217257/OneDrive%20-%20Flinders/Blog/Substack/rareinsights/primary-care-funding-architecture-v1.7.2/pyproject.toml)
- Update dependencies to require `polars`, `pyarrow`, and `pydantic`.
- Set Python version target to `>=3.11`.

#### [MODIFY] [requirements.txt](file:///C:/Users/60217257/OneDrive%20-%20Flinders/Blog/Substack/rareinsights/primary-care-funding-architecture-v1.7.2/requirements.txt)
- Add `polars`, `pyarrow`, and `pydantic`; defer `jax` until the XLA solver code path lands.

### 2. Pydantic Integration
#### [NEW] [schemas.py](file:///C:/Users/60217257/OneDrive%20-%20Flinders/Blog/Substack/rareinsights/primary-care-funding-architecture-v1.7.2/models/primarycare_model/schemas.py)
- Create `pydantic` v2 models for `Scenario` and `ToySettings` definitions with strict typing validation.

#### [MODIFY] [scenario_service.py](file:///C:/Users/60217257/OneDrive%20-%20Flinders/Blog/Substack/rareinsights/primary-care-funding-architecture-v1.7.2/models/primarycare_model/scenario_service.py)
- Refactor `ToySettings` to inherit from Pydantic's `BaseModel`.
- Integrate `polars` for CSV parsing and validations instead of `pandas`.

### 3. Polars & PyArrow Migration
#### [MODIFY] [app.py](file:///C:/Users/60217257/OneDrive%20-%20Flinders/Blog/Substack/rareinsights/primary-care-funding-architecture-v1.7.2/models/primarycare_model/app.py)
- Refactor DataFrame operations and visualization integrations (Plotly) to consume `polars` DataFrames.
- Use `pyarrow` engine for dataset handling.

#### [MODIFY] [tests](file:///C:/Users/60217257/OneDrive%20-%20Flinders/Blog/Substack/rareinsights/primary-care-funding-architecture-v1.7.2/models/tests/)
- Refactor unit/integration tests to use `polars` asserts and verify Pydantic validation behavior.

### 4. Advanced Simulation Pipelines
- **Simulation Visual Playbacks:** Implement Streamlit visualizations for ABM playbacks, Bass diffusion timelines, Nash equilibrium optimization traces, and Monte Carlo histogram sweeps.
- **Global Parameter Sensitivity (GSA):** Map first-order and total Sobol sensitivity variance grids.
- **Client-Side Wasm Compilation:** Setup compilation steps for compiling core modules via `wasm-pack`.
- **Zero-Copy IPC Streams:** Wire PyArrow IPC streams between runtime components and Streamlit.
- **Differential Privacy Guardrails:** Integrate noise generators to verify demographic boundaries.
- **Model Predictive Control:** Optimize funding parameters via differentiability paths using JAX.
- **Queue State Safety Verification:** Define formal state checks to verify deadlock-free transitions.
- **CI Security & SAST Gates:** Deploy Bandit, Semgrep, and secret scanning checks.
- **Subagent Swarms:** Partition track checklists to allow concurrent execution by subagents.
- **Data Versioning:** Set up Git LFS or DVC rules to manage large Monte Carlo dataset outcomes.
- **Cargo Build Performance Caching:** Configure caching actions for intermediate Rust outputs in CI workflows.


---

## Verification Plan

### Automated Tests
- Run `python scripts/check_repo_health.py` to verify formatting, imports, and quality gates pass.
- Run `pytest` to ensure all migrated simulation components function correctly.
- Run SAST scanners to ensure no security flags or credential disclosures are found.

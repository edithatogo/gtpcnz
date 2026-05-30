# Tech Stack

---
title: "Technical Stack"
version: "0.2.0"
status: "reviewed"
last_updated: "2026-05-26"
owner: "Dylan A Mordaunt"
---

## Repository management

- Git for version control.
- Conductor-style context/spec/plan workflow.
- Markdown for drafts and policy documents.
- CSV for extraction matrices and OIA logs.

## Modelling

### Core stack

- Python 3.11+ (targeting 3.14/3.15 for experimental edge lane)
- pandas / polars for data wrangling
- numpy for numerical operations
- networkx for game/actor maps
- scipy for calibration and sensitivity analysis
- matplotlib / plotly for charts
- pytest for tests (unit, integration, end-to-end)

### Simulation engines

- **kairos** (KairoECS bindings) — entity-based patient and provider DES ticks
- **voiage** — value-of-information (EVPI/EVSI) pipeline
- **mars** — multivariate adaptive regression spline metamodeling emulator
- **innovate** — functional Bass diffusion models for adoption curves
- Mesa — agent-based modelling (available but superseded by kairos)
- PySD — system dynamics stock-flow modelling

### Performance acceleration

- **JAX** / XLA — batch Monte Carlo simulation sweeps, compiled GPU/CPU execution
- **pyarrow** — zero-copy memory layouts, IPC streaming, telemetry serialisation
- **scalene** — integrated CPU, GPU and memory profiling

### Testing rigour

- **hypothesis** — property-based testing for entity generation fuzzing
- **mutmut** — mutation testing for assertion quality
- Standard pytest suite (unit, integration, e2e, smoke)

### Interactive visualisation

- **Streamlit** — dynamic dashboards with real-time ABM playback, Bass diffusion choropleths, Nash convergence traces, rolling Monte Carlo histograms
- Plotly — interactive charting components

### Sensitivity and optimisation

- SALib / Sobol — variance-based global sensitivity analysis
- **Bayesian optimisation** — policy parameter auto-tuning
- **jaxopt** — differentiable root-solving for Nash equilibrium convergence

### AI/ML explainability

- **SHAP** — Shapley values for agent decision-network attribution
- **jraph** (on JAX) — graph neural networks for referral bottleneck modelling

### Quality and CI/CD

- **Ruff** — linting and formatting
- **mypy** — static type checking
- **Vale** — prose linting for markdown documents
- **Renovate** — automated dependency updates (bleeding-edge pinning)
- **Bandit** / **Semgrep** — SAST security scanning
- Secret scanning in GitHub Actions
- **wasm-pack** — Rust-core WebAssembly compilation for browser-only simulation runs

### Differential privacy

- Laplace / Gaussian DP bounds on synthetic population generators — zero patient-level or confidential data permitted

### Formal verification

- Queue-safety invariants and TLA+ specifications for deadlock-free scheduler state machines

## Reporting standards

- PRISMA 2020 for review outputs.
- STRESS for empirical simulation reporting.
- ODD protocol for agent-based model description.
- CHEERS 2022 if economic evaluation is added.
- Vancouver style for NZMJ references.

## Document production

- Markdown first.
- Quarto for dynamic, reproducible policy reports (.qmd).
- Convert later to DOCX/PDF only at submission or release stage.

## Visualization

- Streamlit for interactive stakeholder dashboards.
- Plotly and Matplotlib for dynamic charting.

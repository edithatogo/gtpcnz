# Spec: Simulation Engine Evolution

**Status:** Complete

Evolve the primary care funding simulation engine from stylized Python equations to a high-performance, deterministic discrete event simulation (DES) / agent-based model (ABM) architecture incorporating state-of-the-art Python tooling and execution acceleration.

## Requirements

1. **Rust Execution Core (`kairos`):**
   - Integrate KairoECS Python bindings (`kairoecs`) for entity-based patient and provider simulation ticks.
   - Maintain strict determinism and reproducible random seeds.
2. **Value of Information Pipeline (`voiage`):**
   - Implement EVPI and EVSI calculations via the `voiage` library to evaluate parameter uncertainty and target data gaps.
3. **Metamodeling Emulator (`mars`):**
   - Use Multivariate Adaptive Regression Splines (`mars`) to emulate the simulation outcome space, ensuring Streamlit dashboard parameters respond in milliseconds.
4. **Diffusion Models (`innovate`):**
   - Use functional Bass diffusion models (`innovate`) to capture provider innovation and scope adoption rates over time.
5. **State-of-the-Art Python Runtime & Typing (Python 3.14/3.15):**
   - Target the latest Python standard (Python 3.14 / 3.15-dev) in the experimental edge lane.
   - Enforce strict typing with type hints, static code verification via `mypy`, and data model validation using `pydantic` v2.
6. **Data Engines & Telemetry (`pyarrow` & `polars`):**
   - Use Apache Arrow (`pyarrow`) for zero-copy memory layouts, logs, and telemetry serialization.
   - Migrate data wrangling from pandas to `polars` (or pandas 3.0+) for high-speed columnar data processing.
7. **Performance Compilation & Acceleration (JAX / XLA):**
   - Compile batch Monte Carlo simulation sweeps using `jax` and its XLA compiler for parallel multi-core CPU/GPU execution.
   - Profile execution hotspots using `scalene` for integrated CPU, GPU, and memory tracking.
8. **Testing Rigor (Hypothesis & Mutmut):**
   - Maintain a tiered test suite: unit tests for math functions, integration tests for scenario workflows, end-to-end tests for UI/Streamlit bindings, and smoke tests for quick CI runs.
   - Implement property-based testing using `hypothesis` to fuzz entity generation rules.
   - Run mutation testing via `mutmut` to detect weak assertions in the policy decision logic.
9. **Quality, Linting & CI/CD Governance:**
   - Run Vale prose linting on all markdown documents.
   - Enforce strict Ruff checks and format rules.
   - Automate package updates with Renovate.
   - Standardize logging with structured log output.
10. **Interactive & Dynamic Visualization Playbacks (SOTA Streamlit animations):**
    - **Practice ABM Playback:** Create a real-time practice status grid/network viz in Streamlit powered by `kairos` ticks showing patient flow, provider queues, and status transitions (FFor-capitation).
    - **Bass Diffusion Adopter Flow:** Render animated choropleths/line maps using `innovate` adoption trajectories to illustrate geographical/network reform rollout across a 10-15 year simulated span.
    - **Nash Equilibrium Convergence Trace:** Animate the step-by-step gradient path of clincal utility optimization showing convergence stability computed via `jaxopt` root solvers.
    - **Real-Time Monte Carlo Sweeps:** Implement a rolling histogram displaying uncertainty limits narrowing dynamically as JAX `vmap` runs batched iterations in the background.
11. **Global Parameter Sensitivity (Sobol indices):**
    - Support variance-based Sobol sensitivity analysis computed across multi-parameter ranges to assess key policy variance drivers.
12. **Client-Side Simulation Compilation (Wasm/Pyodide):**
    - Ensure Rust core modules compile to WebAssembly using `wasm-pack` to allow zero-infrastructure, browser-only simulation runs.
13. **Zero-Copy Serialization (PyArrow IPC Streaming):**
    - Stream telemetry logs from execution runtimes via PyArrow IPC record batches to dynamic frontend charts, bypassing disk operations.
14. **Differential Privacy Demographics (Differential Privacy bounds):**
    - Restrict patient demographic leak risk by enforcing Laplace or Gaussian differential privacy constraints on synthetic population generators.
15. **Model Predictive Control (JAX-Differentiable policy feedback loops):**
    - Formulate funding adjustment rules as a model predictive control feedback system, optimizing step paths using auto-differentiation gradients.
16. **Formal Logic and Queue Safety Verification:**
    - Verify that patient/provider scheduler state machine states remain deadlock-free by implementing safety invariant tests or formal TLA+ specifications.
17. **Patient Zero-Data Hard Limit:**
    - The codebase is strictly prohibited from utilizing, referencing, or storing confidential or patient-level data. All calibration components must exclusively rely on publicly available, referenced data.
18. **Enforcement of Bleeding-Edge Library Versions:**
    - The active libraries (Polars, JAX, Pydantic, etc.) must be upgraded to their latest stable or prerelease versions, leveraging modern API functions.
19. **Explainable AI (SHAP weights for agent actions):**
    - Record agent decision metrics and output Shapley Additive exPlanations (SHAP) contribution weights to detail why specific GP practices adopt capitation structures.
20. **Bayesian Optimization Policy Auto-Tuning:**
    - Enable Bayesian Optimization solver loops to auto-search parameter thresholds and maximize policy sustainability goals.
21. **CI Security Gates (SAST & Credential scans):**
    - Deploy Bandit, Semgrep, and secret scanning within CI/CD pipelines to proactively safeguard the public-data boundary and detect credential/code anomalies.
22. **GNN Patient Pathways (jraph integration):**
    - Integrate Graph Neural Network structures (using `jraph` on JAX) to represent and predict patient referral flow bottlenecks across clinics.
23. **Multi-Level Subagent Parallelisation (Swarm Dispatch):**
    - Structure track execution plan tasks in decoupled blocks to allow parallel dispatch using concurrent subagents.
24. **Simulation Data Version Control (Git LFS / DVC):**
    - Setup Git LFS or DVC rules to track simulation outcome files, keeping binary traces outside the core repository history.
25. **Cargo Build performance Caching:**
    - Configure Cargo build intermediate caches in GitHub Actions pipelines to optimize Rust-core Wasm compilation speeds.
# Model Calculations, Formulae, and Scoring Investigation

This report provides a comprehensive review of the calculations, formulae, scoring mechanisms, and validation engines used in the GTPCNZ primary care funding architecture model. It details the design, mathematical formulation, verification tests, correctness guarantees, and future enhancements of the model's core modules.

---

## 1. Core Calculations & Formulae

The model calculations are divided into two main runtime pathways:
1. **Public-Safe Bounded Indices**: Deterministic index calculations based on reference scenarios.
2. **Educational Explainer Sliders**: A simplified, interactive teaching lens designed to show the direction of health policy incentives.

### 1.1 Live Scenario Indices
In [runtime_lab.py:L102-145](file:///C:/Users/60217257/OneDrive%20-%20Flinders/Blog/Substack/rareinsights/primary-care-funding-architecture-v1.7.2/models/primarycare_model/runtime_lab.py#L102-145), the function `calculate_indices` processes a `RuntimeScenario` and calculates 9 system indices. Values are clamped via a helper function `clamp` ([runtime_lab.py:L29-30](file:///C:/Users/60217257/OneDrive%20-%20Flinders/Blog/Substack/rareinsights/primary-care-funding-architecture-v1.7.2/models/primarycare_model/runtime_lab.py#L29-30)) and values are converted to fractions using `_as_fraction` ([runtime_lab.py:L90-91](file:///C:/Users/60217257/OneDrive%20-%20Flinders/Blog/Substack/rareinsights/primary-care-funding-architecture-v1.7.2/models/primarycare_model/runtime_lab.py#L90-91)).

*   **Supply Generation Score**:
    $$Supply = \text{clamp}(100 \times (0.34 \times \text{activity} + 0.18 \times \text{capitation} + 0.24 \times \text{scope} + 0.12 \times \text{urgent} + 0.12 \times \text{place} - 0.12 \times \text{budget}))$$
*   **Access Score**:
    $$Access = \text{clamp}(100 \times (0.42 \times \frac{\text{supply}}{100} + 0.18 \times \text{urgent} + 0.15 \times \text{equity} + 0.12 \times \text{place} + 0.10 \times \text{data} - 0.16 \times \text{copay}))$$
*   **Equity & Legitimacy Score**:
    $$EquityLegitimacy = \text{clamp}(100 \times (0.34 \times \text{equity} + 0.24 \times \text{place} + 0.16 \times \text{capitation} + 0.14 \times \text{data} - 0.16 \times \text{copay}))$$
*   **Governance & Resilience Score**:
    $$GovernanceResilience = \text{clamp}(100 \times (0.44 \times \text{governance} + 0.20 \times \text{data} + 0.18 \times \text{place} + 0.10 \times \text{equity} + 0.08 \times \text{capitation}))$$
*   **Hospital Deflection Score**:
    $$Deflection = \text{clamp}(100 \times (0.32 \times \frac{\text{access}}{100} + 0.22 \times \text{urgent} + 0.16 \times \frac{\text{supply}}{100} + 0.16 \times \text{data} + 0.14 \times \text{place} - 0.10 \times \text{complexity}))$$
*   **Gaming Risk Score**:
    $$GamingRisk = \text{clamp}(100 \times (0.35 \times \text{activity} + 0.18 \times \text{scope} + 0.18 \times \text{complexity} - 0.30 \times \text{governance} - 0.18 \times \text{data} - 0.16 \times \text{place}))$$
*   **Fiscal Risk Score**:
    $$FiscalRisk = \text{clamp}(100 \times (0.22 \times \text{activity} + 0.18 \times \frac{\text{gaming\_risk}}{100} + 0.16 \times \text{complexity} + 0.14 \times (1 - \text{budget}) - 0.18 \times \text{governance} - 0.14 \times \frac{\text{deflection}}{100}))$$
*   **Hospital Pressure Score**:
    $$HospitalPressure = \text{clamp}(100 \times (0.34 \times \text{hospital\_salience} + 0.26 \times (1 - \frac{\text{deflection}}{100}) + 0.16 \times \text{complexity} + 0.14 \times \text{budget} - 0.18 \times \frac{\text{access}}{100} - 0.12 \times \text{urgent}))$$

### 1.2 Educational Explainer Levers
In [scenario_service.py:L176-231](file:///C:/Users/60217257/OneDrive%20-%20Flinders/Blog/Substack/rareinsights/primary-care-funding-architecture-v1.7.2/models/primarycare_model/scenario_service.py#L176-231), the function `score_educational_settings` calculates scores using the `EducationalSettings` sliders. The outputs map 7 UI variables to 6 educational scores:
*   **Supply**: Uses `_strategic_response` with a threshold of $0.42$ and steepness of $6.5$.
*   **Governance**: Uses `_strategic_response` with a threshold of $0.50$ and steepness of $6.0$.
*   **Equity**: Uses `_strategic_response` with a threshold of $0.48$ and steepness of $6.0$.
*   **Gaming Risk**: Uses `_strategic_response` with a threshold of $0.10$ and steepness of $7.0$.
*   **Hospital Pressure**: Evaluates the inverse of supply, governance, local support, and equity score.
*   **Viability**: Weighted sum: $0.34 \times \text{supply} + 0.22 \times \text{governance} + 0.18 \times \text{equity} + 0.16 \times (100 - \text{hospital\_pressure}) + 0.10 \times (100 - \text{gaming\_risk})$.

---

## 2. Nonlinear Behaviour

To prevent simple linear scaling and represent economic realities such as diminishing returns and tipping thresholds, two mathematical transformations are applied:

### 2.1 Diminishing Returns (Exponential Tapering)
In [runtime_lab.py:L33-35](file:///C:/Users/60217257/OneDrive%20-%20Flinders/Blog/Substack/rareinsights/primary-care-funding-architecture-v1.7.2/models/primarycare_model/runtime_lab.py#L33-35) (and duplicate `_diminishing_return` in [scenario_service.py:L60-62](file:///C:/Users/60217257/OneDrive%20-%20Flinders/Blog/Substack/rareinsights/primary-care-funding-architecture-v1.7.2/models/primarycare_model/scenario_service.py#L60-62)):
$$f(x, r) = \frac{1 - e^{-r \cdot \text{clamp}(x, 0, 1)}}{1 - e^{-r}}$$
where $r = 2.4$ is the default tapering rate. This models capacity saturation when inputs scale toward $1.0$ ($100\%$).

### 2.2 Strategic Response (Sigmoid/Logistic Tipping Points)
In [runtime_lab.py:L38-39](file:///C:/Users/60217257/OneDrive%20-%20Flinders/Blog/Substack/rareinsights/primary-care-funding-architecture-v1.7.2/models/primarycare_model/runtime_lab.py#L38-39) (and duplicate `_strategic_response` in [scenario_service.py:L56-57](file:///C:/Users/60217257/OneDrive%20-%20Flinders/Blog/Substack/rareinsights/primary-care-funding-architecture-v1.7.2/models/primarycare_model/scenario_service.py#L56-57)):
$$\sigma(x, x_0, k) = \frac{1}{1 + e^{-k(x - x_0)}}$$
where $x_0$ is the tipping threshold and $k$ represents the steepness of transition. This reflects binary outcomes or critical masses (e.g., audit effectiveness tipping at $50\%$).

A test checking the non-linear second derivative of the scheduled benefit is located at [test_scenario_service.py:L87-105](file:///C:/Users/60217257/OneDrive%20-%20Flinders/Blog/Substack/rareinsights/primary-care-funding-architecture-v1.7.2/models/tests/test_scenario_service.py#L87-105):
```python
second_diff = np.diff(values, n=2)
assert np.max(np.abs(second_diff)) > 0.5
```

---

## 3. Core Modules & Services

### 3.1 `runtime_lab`
Located at [runtime_lab.py](file:///C:/Users/60217257/OneDrive%20-%20Flinders/Blog/Substack/rareinsights/primary-care-funding-architecture-v1.7.2/models/primarycare_model/runtime_lab.py). Key features:
*   **Reference Calculation**: `run_reference_calculation` ([L148-176](file:///C:/Users/60217257/OneDrive%20-%20Flinders/Blog/Substack/rareinsights/primary-care-funding-architecture-v1.7.2/models/primarycare_model/runtime_lab.py#L148-176)) projects primary contacts, unmet needs, ED events, hospital admissions, ambulance conveyances, and costs per 100k population.
*   **Stochastic Uncertainty**: `run_stochastic_uncertainty` ([L192-232](file:///C:/Users/60217257/OneDrive%20-%20Flinders/Blog/Substack/rareinsights/primary-care-funding-architecture-v1.7.2/models/primarycare_model/runtime_lab.py#L192-232)) runs a Monte Carlo simulation (capped at 500 draws) adding Gaussian noise to scenario parameters to generate percentile bounds (p05, p50, p95).
*   **Stock-Flow Trace**: `run_stock_flow_trace` ([L235-265](file:///C:/Users/60217257/OneDrive%20-%20Flinders/Blog/Substack/rareinsights/primary-care-funding-architecture-v1.7.2/models/primarycare_model/runtime_lab.py#L235-265)) models monthly system dynamics of need generated, primary capacity, served contacts, and hospital/fiscal pressure over up to 60 months.
*   **Agent Lens (ABM)**: `run_agent_lens` ([L268-308](file:///C:/Users/60217257/OneDrive%20-%20Flinders/Blog/Substack/rareinsights/primary-care-funding-architecture-v1.7.2/models/primarycare_model/runtime_lab.py#L268-308)) runs an Agent-Based Model over $N$ patients using Beta distributions for patient needs, rurality risk modifiers, access barriers, and contact attempt success rates.

### 3.2 `scenario_service`
Located at [scenario_service.py](file:///C:/Users/60217257/OneDrive%20-%20Flinders/Blog/Substack/rareinsights/primary-care-funding-architecture-v1.7.2/models/primarycare_model/scenario_service.py). Key features:
*   **Scenario Loading**: `load_scenario_results` ([L146-158](file:///C:/Users/60217257/OneDrive%20-%20Flinders/Blog/Substack/rareinsights/primary-care-funding-architecture-v1.7.2/models/primarycare_model/scenario_service.py#L146-158)) reads, validates, and appends roles and strict `claim_boundary` disclaimers to results.
*   **Validation**: Integrates optional Pandera dataframes verification via `validate_scenario_results` ([L161-173](file:///C:/Users/60217257/OneDrive%20-%20Flinders/Blog/Substack/rareinsights/primary-care-funding-architecture-v1.7.2/models/primarycare_model/scenario_service.py#L161-173)) and `validate_reference_results_frame` ([pandera_schemas.py:L71-98](file:///C:/Users/60217257/OneDrive%20-%20Flinders/Blog/Substack/rareinsights/primary-care-funding-architecture-v1.7.2/models/primarycare_model/validation/pandera_schemas.py#L71-98)).
*   **Calibration Readiness**: `build_calibration_readiness_table` ([L252-264](file:///C:/Users/60217257/OneDrive%20-%20Flinders/Blog/Substack/rareinsights/primary-care-funding-architecture-v1.7.2/models/primarycare_model/scenario_service.py#L252-264)) maps what inputs (e.g. NPCD bookings, co-payments, ACC regulations) are needed for future calibration.

---

## 4. Correctness & Validation Guarantees

The codebase enforces calculation correctness and schema bounds at three levels:
1.  **Immutable Contracts (Pydantic)**: `ParameterDefinition` and `RuntimeScenarioDefinition` prohibit extra fields (`extra="forbid"`) and enforce strict types/bounds (e.g., Pydantic `Field(ge=0, le=100)`). See [parameters.py:L20-58](file:///C:/Users/60217257/OneDrive%20-%20Flinders/Blog/Substack/rareinsights/primary-care-funding-architecture-v1.7.2/models/primarycare_model/contracts/parameters.py#L20-58) and [scenarios.py:L14-35](file:///C:/Users/60217257/OneDrive%20-%20Flinders/Blog/Substack/rareinsights/primary-care-funding-architecture-v1.7.2/models/primarycare_model/contracts/scenarios.py#L14-35).
2.  **Optional Pandera & Fallback Validation**: `validate_reference_results_frame` ([pandera_schemas.py:L71-98](file:///C:/Users/60217257/OneDrive%20-%20Flinders/Blog/Substack/rareinsights/primary-care-funding-architecture-v1.7.2/models/primarycare_model/validation/pandera_schemas.py#L71-98)) performs schema verification on DataFrames. If `pandera` is missing, it falls back to manual numeric parsing and `between(0, 100)` bounds checks.
3.  **Algorithmic Safety Clamps**: High-frequency execution functions apply safety boundaries using `clamp()` to guarantee that intermediate calculations cannot overflow or underflow mathematical domains.

---

## 5. Verification & Testing

The tests located in `models/tests/` verify both deterministic limits and statistical distributions:
*   [test_runtime_lab.py](file:///C:/Users/60217257/OneDrive%20-%20Flinders/Blog/Substack/rareinsights/primary-care-funding-architecture-v1.7.2/models/tests/test_runtime_lab.py):
    *   `test_live_reference_calculation_has_expected_scenarios_and_bounds` ([L13-28](file:///C:/Users/60217257/OneDrive%20-%20Flinders/Blog/Substack/rareinsights/primary-care-funding-architecture-v1.7.2/models/tests/test_runtime_lab.py#L13-28)): Verifies that calculations complete and stay within the $0-100$ boundary.
    *   `test_stochastic_uncertainty_is_seeded_and_capped` ([L38-46](file:///C:/Users/60217257/OneDrive%20-%20Flinders/Blog/Substack/rareinsights/primary-care-funding-architecture-v1.7.2/models/tests/test_runtime_lab.py#L38-46)): Ensures Monte Carlo simulations are strictly reproducible via seeds and enforce population size constraints.
    *   `test_agent_lens_is_seeded_and_population_capped` ([L56-64](file:///C:/Users/60217257/OneDrive%20-%20Flinders/Blog/Substack/rareinsights/primary-care-funding-architecture-v1.7.2/models/tests/test_runtime_lab.py#L56-64)): Validates agent attributes and served contact limits.
*   [test_scenario_service.py](file:///C:/Users/60217257/OneDrive%20-%20Flinders/Blog/Substack/rareinsights/primary-care-funding-architecture-v1.7.2/models/tests/test_scenario_service.py):
    *   `test_load_scenario_results_adds_claim_boundary` ([L44-62](file:///C:/Users/60217257/OneDrive%20-%20Flinders/Blog/Substack/rareinsights/primary-care-funding-architecture-v1.7.2/models/tests/test_scenario_service.py#L44-62)): Assures that files loaded append strict caveat metadata.
    *   `test_educational_supply_response_is_not_linear_in_scheduled_benefit` ([L87-105](file:///C:/Users/60217257/OneDrive%20-%20Flinders/Blog/Substack/rareinsights/primary-care-funding-architecture-v1.7.2/models/tests/test_scenario_service.py#L87-105)): Validates the nonlinear strategic response functions using numerical differentiation.

---

## 6. Stubs and Remaining Scaffolds

The following gaps and stubs remain between the current repository implementation and a comprehensive, production-ready scenario system:
1.  **Pandera Optional Import**: Pandera checks are wrapped in a `try/except ImportError` block ([pandera_schemas.py:L14-20](file:///C:/Users/60217257/OneDrive%20-%20Flinders/Blog/Substack/rareinsights/primary-care-funding-architecture-v1.7.2/models/primarycare_model/validation/pandera_schemas.py#L14-20)). If not installed, it falls back to basic manual Pandas validation.
2.  **Static Calibration Readiness**: The calibration readiness table (`build_calibration_readiness_table`) is entirely static ([scenario_service.py:L252-264](file:///C:/Users/60217257/OneDrive%20-%20Flinders/Blog/Substack/rareinsights/primary-care-funding-architecture-v1.7.2/models/primarycare_model/scenario_service.py#L252-264)), serving as documentation rather than an active diagnostic.
3.  **Public App Gap Map**: The `model_gap_map()` output lists several items that are "Not yet complete in public app" or "Not yet implemented" ([runtime_lab.py:L311-324](file:///C:/Users/60217257/OneDrive%20-%20Flinders/Blog/Substack/rareinsights/primary-care-funding-architecture-v1.7.2/models/primarycare_model/runtime_lab.py#L311-324)).

---

## 7. Next Steps & Bleeding Edge Features

### Is the scenario calculation layer completed?
The backend calculation layer is fully functional, strictly validated, and thoroughly covered by unit tests. However, it is not "complete" from an interactive UI standpoint, as several advanced diagnostic visualizations and controls are currently documented as gaps.

### What would make it bleeding edge?
To advance the model to a state-of-the-art / bleeding-edge level, the following features should be integrated directly into the public Streamlit app:
1.  **Scenario Morphing**: Visual transition animations (e.g., interpolating weights) as users drag reform levers from `F0` (status quo) to `F4` (full hybrid).
2.  **Stochastic Replay Controls**: Allow users to run, pause, and replay seeded stochastic simulations, visualizing confidence intervals dynamically in real-time.
3.  **Agent-Flow Allocation Visuals**: Render the Agent-Based Model (`run_agent_lens`) as a live sankey diagram or queue-flow visualization, illustrating unmet attempt patterns and patient barriers.
4.  **Calculation Audit Overlay**: Add hover cards or expandable code details on every output metric to expose the exact mathematical formula sketch, inputs, and active caveats for full transparency.

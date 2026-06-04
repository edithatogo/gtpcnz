# Model card v1.7.2: public-data anchored primary care funding benchmark

## Model name
Public-data anchored benchmark for primary care funding architecture in Aotearoa New Zealand.

## Version
v1.7.2. This version incorporates red-team and devil's advocate findings into the model communication layer.

## Intended use
- Compare the relative logic of funding architectures.
- Identify which assumptions are load-bearing.
- Support public explanation, policy discussion, stakeholder validation and OIA/data planning.
- Prepare the pathway for future empirical calibration.

## Not intended for
- Claiming precise reductions in emergency department presentations, admissions or costs.
- Producing an implementation business case.
- Replacing stakeholder validation, equity review or linked-data analysis.
- Claiming that any organisation has endorsed the model.
- Arguing that fee-for-service alone is superior to capitation.

## Core policy question
Does a hybrid architecture allow lower-cost upstream care to expand safely before need becomes hospital demand? In this model, hybrid means capitation for population responsibility plus an uncapped, scheduled, rules-based fee-for-service stream for eligible primary medical activity, with place-based accountability.

## Strongest counter-hypothesis
The current reform pathway may be sufficient to improve access without a new uncapped scheduled fee-for-service stream. That pathway includes capitation reweighting, the access target, the National Primary Care Dataset, digital access, urgent-care investment, PHO accountability and separate appropriations.

## What the model must not hide
- Uncapped activity without audit, item rules and place accountability is a high-risk scenario.
- Co-payments can worsen inequity unless protected.
- Scope expansion can fragment care unless tied to shared records, governance and continuity.
- Rural access may need capital, workforce, housing, salaried and infrastructure levers as well as item payments.
- Accident Compensation Corporation is an analogy for rules-based claims, not a complete model for illness-based primary care.

## Inputs
The benchmark uses 70 parameters across demand, supply, funding, governance, ambulance, hospital, equity, risk and implementation domains. v1.7.1/v1.7.2 tiers these into core, extended and exploratory parameters.

## Outputs
- Access and supply indices.
- Hospital pressure indices.
- Fiscal/gaming risk indices.
- Hybrid viability scores.
- Scenario comparison and sensitivity outputs.

## Validation status
This is a public-data anchored benchmark and educational explainer. It is not linked-data calibrated and not a patient-level forecast. It should not be used to claim precise fiscal savings, hospital-demand reductions, workforce effects, or implementation impacts.

## Registry-backed parameters and scenarios

All tunable model parameters are maintained in versioned YAML registries (`models/primarycare_model/registries/`). No production parameter default lives outside a registry. Each parameter record includes:

- `parameter_id` — stable identifier referenced by scenarios and overrides
- `value_type` — `integer`, `number`, `boolean`, or `categorical`
- `default_value` — the production default
- `lower_bound`, `upper_bound` — validity range for runtime checks
- `evidence_tier` — `assumption`, `public_data`, `stakeholder`, `linked_data`, or `calibrated`
- `sensitivity_class` — `public`, `public_aggregate`, `template`, `sensitive`, or `confidential`

### Parameter catalogue summary

| Domain | Parameters | Evidence tiers | Claim boundary |
|---|---|---|---|
| Capitation rates | `base_capitation_rate`, age weights, deprivation uplift | `public_data` | Public documents show... |
| FFS item values | Consultations, after-hours, prolonged, vaccine admin, care coordination | `public_data` / `stakeholder` | Public documents show... / Stakeholder feedback suggests... |
| Copayment thresholds | Annual cap, income waiver, max gap | `public_data` | Public documents show... |
| Population counts | Enrolled population, catchment estimate, patient-to-GP ratio | `public_data` / `stakeholder` | Public documents show... |
| Workforce parameters | Supply elasticity, nurse substitution, participation rate | `public_data` / `calibrated` | Public documents show... / Track 043 linked-data calibration |
| Governance parameters | Audit intensity, data visibility, scope flexibility, governance index | `calibrated` | Track 043 linked-data calibration |

### Scenario catalogue summary

Scenarios are defined in `registries/scenarios.v1.yaml` and loaded via `RegistryLoader`. Each scenario references known parameter IDs and supplies override values. The `RuntimeScenarioDefinition` contract (in `models/primarycare_model/contracts/scenarios.py`) defines the fields the calculation lab consumes.

| Scenario ID | Kind | Claim boundary |
|---|---|---|
| `reference` | `reference` | "The benchmark shows the logic of..." |
| `high_capitation` | `educational` | "I think this warrants testing..." |
| `high_ffs` | `educational` | "I think this warrants testing..." |
| `balanced_hybrid` | `reference` | "The benchmark shows the logic of..." |
| (user-defined) | `stochastic_demo` | "Theory predicts..." |

## What is calculated vs. what is assumed

The distinction between calculated quantities and assumed values is critical for correct interpretation. This table identifies every output value's origin.

| Output or intermediate | Calculated by the model? | Source / formula | Claim boundary |
|---|---|---|---|
| Access index | **Yes** — deterministic formula of 9 slider inputs | `access_index = f(activity_signal, capitation, place_accountability, scope_capacity, urgent_ambulance, data_visibility, governance, equity_protection, copayment_burden)` | Benchmark shows the logic of... |
| Supply generation index | **Yes** — deterministic formula | `supply_index = f(capitation, activity_signal, scope_capacity, governance)` | Benchmark shows the logic of... |
| Hospital pressure index | **Yes** — deterministic formula | `hospital_pressure = f(access_index, urgent_ambulance, hospital_salience)` | Benchmark shows the logic of... |
| Gaming risk index | **Yes** — deterministic formula | `gaming_risk = f(activity_signal, governance, data_visibility, audit_intensity)` | Benchmark shows the logic of... |
| Hybrid viability score | **Yes** — composite of access, supply, hospital pressure, gaming risk | Weighted average with equity and governance modifiers | Benchmark shows the logic of... |
| Monte Carlo distribution (p05/p50/p95) | **Yes** — stochastic draws | `jax_mc_adapter` draws from seeded distribution; `UncertaintySummary` aggregates percentiles | Theory predicts... (demonstrative shape only) |
| ABM diffusion trace | **Yes** — agent-based simulation | `abm_adapter` runs seeded agent model over configurable population | Theory predicts... (demonstrative shape only) |
| Capitation base rate | **Assumed** — registry default | NZ Ministry of Health GP capitation funding schedule (2023/24) | Public documents show... |
| FFS item values | **Assumed** — registry default | NZ PHO Services Agreement | Public documents show... |
| GP supply elasticity | **Assumed** — registry default | Track 043 calibrated parameter (linked data) | Track 043 linked-data calibration |
| Audit intensity factor | **Assumed** — registry default | Track 043 calibrated parameter (linked data) | Track 043 linked-data calibration |
| Population counts | **Assumed** — registry default | Statistics NZ ERP / Ministry enrolment data | Public documents show... |
| Copayment thresholds | **Assumed** — registry default | NZ Community Services Card / High Use Health Card policy | Public documents show... |
| Educational lever effects | **Calculated** — simplified pedagogical formula | `educational_levers.v1.yaml` defines the lever; formula is illustrative | I think this warrants testing... |

**Rule of thumb**: If you see it in a slider in the calculation lab, it's a user-adjustable assumption with a registry default. If you see it in a score or index in the results table, it was calculated from those assumptions. The `ResultManifest` tells you which mode was used.

## Validation boundaries and result-manifest structure

Every public-facing result is packaged in a `ResultManifest` contract (defined in `models/primarycare_model/contracts/results.py`). The manifest travels with the output through the Streamlit display layer and is included in any export or download.

### ResultManifest fields

| Field | Type | Description |
|---|---|---|
| `result_id` | `str` (min_length=1) | Unique identifier for this specific run, e.g. `"sd_reference_42"` |
| `calculation_mode` | `CalculationMode` literal | One of `precomputed`, `live_deterministic`, `seeded_stochastic`, `educational` |
| `scenario_id` | `str` (min_length=1) | The scenario definition used, e.g. `"reference"`, `"high_capitation"` |
| `seed` | `int` or `None` | Seeded random seed for stochastic modes; `None` for deterministic |
| `draws` | `int` or `None` | Number of stochastic draws; `None` for deterministic |
| `claim_boundary` | `str` (min_length=1) | Wording rule from the claim ladder that applies to this result |
| `validation_status` | `str` (min_length=1) | Validation outcome: `"passed"`, `"warning"`, `"failed"` |

### ScenarioResult fields

Each scenario run produces a `ScenarioResult` (Pydantic strict contract) with scores bounded [0, 100]:

| Field | Bounds | Meaning |
|---|---|---|
| `scenario_id` | min_length=1 | Which scenario was calculated |
| `hybrid_viability_score` | 0–100 | Composite viability of the hybrid architecture under these settings |
| `access_score` | 0–100 | Estimated population access to timely primary care |
| `supply_generation_score` | 0–100 | Ability of the funding settings to generate workforce supply |
| `hospital_pressure_score` | 0–100 | Estimated avoided or deferred hospital demand (lower is better) |
| `gaming_risk_score` | 0–100 | Risk of claim inflation or gaming behaviour (lower is better) |
| `calculation_status` | min_length=1 | `"completed"`, `"partial"`, or `"error"` |

### Pandera validation (optional)

Public result frames are validated through a `ReferenceResultSchema` Pandera `DataFrameModel` when Pandera is installed. When Pandera is not available (the lean Streamlit deployment path), an equivalent `validate_reference_results_frame` function checks the same column presence, data types and 0–100 score bounds using local pandas operations. This guarantees that every value displayed in the Streamlit UI respects its declared bounds, regardless of deployment environment.

## Runtime calculation modes

The model executes in one of four calculation modes. Every public output carries a `ResultManifest` with the `calculation_mode` field set to one of these values, rendered as a coloured badge in the Streamlit UI.

| Mode | `calculation_mode` literal | When used | What guarantees are made | Claim boundary |
|---|---|---|---|---|
| **Public-data anchored** | `precomputed` | Default static benchmark tables and reference result frames | Deterministic; uses only registry defaults; no runtime slider input | "The benchmark shows the logic of..." |
| **Deterministic** | `live_deterministic` | User adjusts sliders in the calculation lab; formulas run once with the current slider state | Deterministic for the same inputs; no random variation; seed is `None` | "The benchmark shows the logic of..." |
| **Stochastic demo** | `seeded_stochastic` | User enables Monte Carlo, ABM, diffusion or MPC engines; results include a seed and draw count | Reproducible when seed is recorded; distribution shape is demonstrative, not calibrated | "Theory predicts..." / "The benchmark shows the logic of..." |
| **Educational** | `educational` | User explores educational simulation levers; formulas and effects are simplified for teaching | Results are illustrative only; formulas are pedagogical simplifications | "Stakeholder feedback suggests..." / "I think this warrants testing..." |

### What each mode means for public communication

- **`precomputed`** — Every value in the output frame was calculated from the YAML registry defaults. No runtime user input changed the numbers. This is the safest mode for public documents.
- **`live_deterministic`** — The user adjusted one or more sliders and the model ran the same deterministic formulas on the adjusted inputs. If two users set the same slider positions they get identical outputs. This is the mode used for "what if" exploration.
- **`seeded_stochastic`** — The model ran a seeded random process (Monte Carlo, agent-based model, diffusion simulation, or MPC optimisation). The result includes the seed value and draw count so it can be reproduced. The *shape* of the distribution is a public-data anchored benchmark, not a calibrated forecast. The uncertainty summary (`p05`, `p50`, `p95`) is demonstrative.
- **`educational`** — The result comes from a deliberately simplified formula designed to illustrate a policy concept (e.g. "if you raise capitation, hybrid viability goes up slightly"). Educational levers have registry-backed labels and explanations, but the formulas are not fit for policy calibration.

## Interpretation rule
Use the model to ask better questions and prioritise validation. Do not use it to claim final effect sizes.

## Public aggregate calibration programme

This model card remains bounded as public benchmark material unless generated release model cards and public aggregate validation gates pass.

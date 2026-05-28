# Enhancement Shortlist v1.8.5 — Bleeding Edge Analytical Enhancements

**Track:** 049  
**Date:** 2026-05-28  
**Status:** Approved  
**Owner:** Track-049

---

## 1. Current Capability Inventory

The table below catalogues what the repo currently exposes across inputs, subgroups, simulations, and visualisations.

### 1.1 Inputs Exposed

| Input family | What is exposed | Where |
|---|---|---|
| **Policy levers** | 7 educational sliders (scheduled benefit, capitation, place accountability, audit, equity protection, scope, local in-person) | Sidebar, `EducationalSettings` |
| **Scenario parameters** | 13 runtime parameters per scenario (activity_signal, capitation, place_accountability, scope_capacity, urgent_ambulance, data_visibility, governance, equity_protection, copayment_burden, budget_tightness, hospital_salience, complexity) | RuntimeScenario dataclass, registry-loaded |
| **Geography/access** | `rural` flag in agent lens only; `travel_barrier` slider in microeconomics lab 4 | Agent lens, access-mix lab |
| **Equity/deprivation** | `equity_protection` as policy lever; `equity_legitimacy_score` as output metric | Sidebar, scenario output |
| **Practice structure** | Not directly exposed as an input slider | — |
| **Demand mix** | `complexity` as scenario param; need bands in access-mix lab | Registry, lab 4 |
| **Payment sensitivity** | Sliders for scheduled benefit, capitation, co-payment | Sidebar |
| **Delivery mode** | `digital_access` slider in access-mix lab | Microeconomics lab 4 |

### 1.2 Subgroups Currently Exposed

| Subgroup | Exposed? | Where |
|---|---|---|
| Rural vs urban | Partial — `rural` flag in agent lens only, not on deterministic charts | run_agent_lens output |
| High vs low deprivation | Not directly exposed | — |
| Small vs large practices | Not exposed | — |
| Younger vs older panels | Not exposed | — |
| Low vs high complexity | Partial — complexity slider bands in access-mix lab | Microeconomics lab 4 |
| High vs low workforce supply | Not exposed | — |

### 1.3 Simulations Currently Exposed

| Simulation | Status | Where |
|---|---|---|
| **Deterministic reference** | ✅ Live runtime recalculation | Live model lab |
| **Seeded Monte Carlo** | ✅ run_stochastic_uncertainty (draws, seed, sd) | Live model lab |
| **Stochastic replay** | ✅ Fixed-seed vs random-seed comparison | Live model lab |
| **Stock-flow trace** | ✅ Monthly dynamics: capacity, unmet need, pressure | Live model lab |
| **Agent-based teaching lens** | ✅ Capped ABM with rural flag, access barrier | Live model lab |
| **Bass diffusion** | ✅ BassDiffusionAdapter wired, not in public UI | engines/diffusion_adapter.py |
| **Model predictive control** | ✅ MPCAdapter wired, not in public UI | engines/mpc_adapter.py |
| **Nash optimisation** | ✅ NashOptAdapter wired, not in public UI | engines/nash_opt_adapter.py |
| **Sensitivity (OAT)** | ✅ SensitivityAnalysisAdapter wired, not in public UI | engines/sensitivity_adapter.py |

### 1.4 Visualisations Currently Exposed

| Visualisation | Status | Where |
|---|---|---|
| Bar chart — reference viability | ✅ Precomputed + live | Reference scenarios tab |
| Scatter — supply vs hospital pressure | ✅ | Reference scenarios tab |
| Heatmap — scenario score matrix | ✅ px.imshow 6 metrics × 10 scenarios | Reference scenarios tab |
| Radar — scenario profile | ✅ go.Scatterpolar | Reference scenarios tab |
| Line — marginal supply response | ✅ | Microeconomics lab 1 |
| Line — claims audit game | ✅ | Game theory lab 1 |
| Line — coordination game | ✅ | Game theory lab 2 |
| Line — gaming-risk frontier | ✅ | Game theory lab 3 |
| Bar — capitation budget | ✅ | Microeconomics lab 2 |
| Bar — scheduled payment with controls | ✅ | Microeconomics lab 3 |
| Stacked bar — co-payment access mix | ✅ | Microeconomics lab 4 |
| Violin — stochastic distribution | ✅ | Live model lab |
| Line — stock-flow dynamics | ✅ Multi-trace | Live model lab |
| Scatter — agent lens | ✅ Coloured by rural, sized by contacts | Live model lab |
| Bar — calculation trace | ✅ | Live model lab |
| Bar — readiness/maturity | ✅ | Current state tab |
| Static diagram — architecture | ✅ Graphviz | Current state tab |
| Bar — educational explainer output | ✅ | Educational explainer tab |

### 1.5 What Exists Off-UI (Engines Layer)

| Engine adapter | Purpose | Wired to public UI? |
|---|---|---|
| sensitivity_adapter.py | One-at-a-time lever perturbation | ❌ No — engine exists, not rendered |
| jax_mc_adapter.py | Seeded Monte Carlo (JAX-backed) | ❌ No — runtime_lab.py has its own MC |
| abm_adapter.py | Agent-based simulation (full engine) | ❌ No — run_agent_lens is separate |
| sd_adapter.py | System dynamics (stock-flow engine) | ❌ No — run_stock_flow_trace is separate |
| diffusion_adapter.py | Bass diffusion adoption curve | ❌ No |
| mpc_adapter.py | Model predictive control | ❌ No |
---

## 2. MoSCoW Ranked Shortlist

### 2.1 Inputs

| Candidate | Rank | Rationale |
|---|---|---|
| **Equity/deprivation quintile** | **Must** | Required for subgroup equity stratification; model already computes `equity_legitimacy_score` — exposing as subgroup cut is low-cost. |
| **Rurality / remoteness** | **Must** | Already present in agent lens (`rural` flag). Needs promotion to deterministic chart stratification. |
| **Practice size / workforce mix** | **Should** | Explains provider heterogeneity but needs new registry inputs. |
| **Demand-mix bands** | **Should** | Age/LTC complexity bands enrich microeconomics lab 4. |
| **Payment sensitivity / elasticity** | **Could** | Supports threshold analysis. |
| **Delivery mode share** | **Could** | Telehealth share implicit in access-mix lab already. |

### 2.2 Subgroup Stratifications

| Candidate | Rank | Rationale |
|---|---|---|
| **Rural vs urban** | **Must** | In agent lens; promote to deterministic chart stratification. |
| **High vs low deprivation** | **Must** | Central to model thesis. Single highest-impact enhancement. |
| **Small vs large practices** | **Should** | Scale effects matter but need registry param. |
| **Younger vs older panels** | **Should** | Age-band stratification needs registry expansion. |
| **Low vs high complexity panels** | **Should** | Partial in access-mix lab; promote to full. |
| **High vs low workforce supply** | **Could** | Needs geographic workforce data. |

### 2.3 Secondary Analyses

| Candidate | Rank | Rationale |
|---|---|---|
| **Tornado sensitivity** | **Must** | Highest-impact. sensitivity_adapter.py computes OAT deltas — needs tornado chart. |
| **Counterfactual deltas** | **Must** | Live-vs-precomputed delta exists; promote to dedicated visual. |
| **Calibration-readiness check** | **Should** | Table exists; extend with per-metric flags. |
| **Variance decomposition** | **Should** | Natural progression from tornado, needs ensemble storage. |
| **Scenario matrix** | **Should** | Heatmap exists; extend with subgroup facets. |
| **Interaction scan** | **Could** | Needs multiple subgroup runs. |
| **Regime map** | **Could** | Needs parameter-space sweep infrastructure. |

### 2.4 Visualisations

| Candidate | Rank | Rationale |
|---|---|---|
| **Tornado chart** | **Must** | Direct visual for OAT sensitivity adapter. Top-3 driver ID. |
| **Waterfall / decomposition chart** | **Must** | calculation_trace has the data — needs go.Waterfall renderer. |
| **Small multiples (subgroup-stratified)** | **Must** | Core visual for equity comparison. Replicate charts with subgroup faceting. |
| **Heatmap matrix (scenario × subgroup)** | **Should** | Extends scenario heatmap with subgroup dimension. |
| **Ridge/violin (subgroup-stratified)** | **Should** | Extends violin with subgroup facets. |
| **Uncertainty ribbon (stock-flow)** | **Should** | Adds seeded stochastic spread to stock-flow lines. |
| **Payoff surface (3D)** | **Could** | 3D interactivity harder to maintain. |
| **Phase portrait / vector field** | **Could** | Needs separate equilibrium analysis. |
| **Frontier plot (multi-objective)** | **Could** | Gaming-risk frontier already exists as 2D. |

### 2.5 Simulation Modes

| Candidate | Rank | Rationale |
|---|---|---|
| **Seeded Monte Carlo ensembles** | **Must** | Exists per-scenario. Enhance to all-scenario ensemble stats. |
| **Cohort-stratified runs** | **Must** | Reuse deterministic calc with subgroup param sets. |
| **Stress-test scenarios** | **Should** | Probe extreme-but-plausible inputs. |
| **Policy shock sequences** | **Should** | Step-change events via stock-flow engine. |
| **Agent-based subgroup replay** | **Could** | Needs ABM adapter wired to UI. |
| **Regime sweep simulation** | **Could** | Computationally intensive. |

### 2.6 Solver Boundary

| Item | Decision | Rationale |
|---|---|---|
| **Stronger equilibrium solver** | **Won't (this track)** | Belongs in Track 048. Nash heuristic stays. |

### 2.7 Explicit Won't

| Candidate | Rationale |
|---|---|
| **Person-level analysis** | Violates aggregate-subgroup preference. |
| **Private / patient-level data** | Prohibited by public-data boundary. |
| **Black-box solvers** | Contradicts transparency requirement. |
| **Solver promotion without gate** | Track 048 owns that decision. |

---

## 3. First-Wave Implementation Recommendations (Top 5)

| # | Item | Category | Scope | Effort |
|---|---|---|---|---|
| 1 | **Subgroup equity/rural stratification on existing charts** | Subgroup + Visual | Add equity-deprivation and rural/urban colour splits to viability bar, scatter, and micro labs. Use small-multiples faceting. | 2-3 days |
| 2 | **Tornado sensitivity chart** | Analysis + Visual | Wire sensitivity_adapter.py OAT output into Plotly tornado chart. Show top-3 driver deltas for viability and hospital pressure. | 1-2 days |
| 3 | **Seeded Monte Carlo ensembles (all-scenario)** | Simulation | Extend run_stochastic_uncertainty across all 10 scenarios. Add ensemble-mode toggle in live model lab. | 2-3 days |
| 4 | **Waterfall / decomposition chart** | Visual | Add go.Waterfall chart showing how 7 component indices build hybrid viability. Data from calculation_trace. | 1 day |
| 5 | **Cohort-stratified runs** | Simulation | Subgroup parameter override system: run deterministic calc with rural/urban or deprivation variants. Comparison table + small-multiples. | 2-3 days |

**Wave 1 acceptance criteria:**
- At least one visual and one simulation enhancement selected ✅ (items 2+4 visual, items 3+5 simulation).
- Subgroup equity/rural stratification is highest priority ✅ (#1).
- Public claim boundary unchanged (all items use existing public-data anchored inputs).
- Clear scope and effort estimate per item.
- Tests exist for new renderers and simulation paths.

### Wave 2 — "Should" items (next batch)

| # | Item | Trigger to promote |
|---|---|---|
| 6 | Variance decomposition | After ensemble MC stores per-draw parameter-output pairs |
| 7 | Heatmap matrix (scenario × subgroup) | After subgroup stratification produces multi-dim output |
| 8 | Policy shock sequences | After stock-flow trace stable with step-change event handling |
| 9 | Uncertainty ribbon on stock-flow | After ensemble MC produces trace-level uncertainty bands |
| 10 | Ridge/violin with subgroup facets | After subgroup stratification live with stochastic runs |
| 11 | Stress-test scenarios | After parameter-boundary sweep infrastructure in place |

### Wave 3 — "Could" items (future consideration)

| # | Item | Trigger to promote |
|---|---|---|
| 12 | Phase portraits / vector fields | When Track 048 produces analytical equilibrium lane |
| 13 | Agent-based subgroup replay | When ABM adapter wired to public UI |
| 14 | Regime sweep simulation | When parameter-space sweep tooling built |
| 15 | Payoff surface (3D) | When 3D tooling justified by user research |
| 16 | Interaction scan | When multiple subgroup dimensions are live |

---

## 4. Rationale for Each Decision

### 4.1 Why equity/rural stratification is the top priority
The model already computes `equity_legitimacy_score` and flags `rural` in the agent lens. Promoting these to the deterministic chart layer lets every reader see which subgroups benefit or lose under each policy architecture. This serves the equity and Te Tiriti visibility requirement in CONTRIBUTING.md.

### 4.2 Why tornado sensitivity over variance decomposition
The OAT sensitivity adapter already exists. A tornado chart is the most intuitive way to communicate parametric influence to a policy audience. Variance decomposition requires ensemble storage across multiple seeds — infrastructure not yet built.

### 4.3 Why seeded Monte Carlo ensembles over deeper stochastic modes
Seeded MC already runs per-scenario. The enhancement is trivial: extend to all scenarios and produce ensemble-level summaries. Gives the reader uncertainty bounds across the full policy space without new engine complexity.

### 4.4 Why waterfall/decomposition in Wave 1
Hybrid viability is a weighted composite of 7 component indices. A waterfall chart directly answers *"Where does this number come from?"* The data already exists in calculation_trace — the visual is the only missing piece.

### 4.5 Why cohort-stratified runs over agent-based subgroup replay
Cohort stratification reuses the deterministic calculation engine with subgroup-specific parameter sets. Simpler, more transparent, and testable than wiring the ABM adapter to the public UI first.

### 4.6 Why solver upgrades are Won't in this track
Track 048 exists to decide whether Nash stays educational or gets promoted. Track 049 must not pre-empt that decision.

### 4.7 Why person-level and private-data items are Won't
These violate the core decision rules: prefer public-data anchored inputs, prefer aggregate subgroup analysis over person-level inference. The agent lens is the agreed limit of individual-level exposure.

---

## 5. Promotion Triggers

### 5.1 Should → Must triggers

| Item | Trigger |
|---|---|
| Variance decomposition | After ensemble MC stores per-draw perturbation data for ≥3 months |
| Heatmap matrix | After ≥2 subgroup dimensions live (e.g. rural + deprivation) |
| Policy shock sequences | After a policy stakeholder requests explicit shock-testing |
| Uncertainty ribbon | After ensemble MC produces per-timestep uncertainty |

### 5.2 Could → Should triggers

| Item | Trigger |
|---|---|
| Phase portraits | After Track 048 produces analytical equilibrium lane + user testing demand |
| Agent-based subgroup replay | After ABM adapter wired to UI + subgroup parameterisation designed |
| Regime sweep simulation | After 2D parameter-sweep built and policy question requires regime mapping |
| Payoff surface (3D) | After user research identifies need for 3D incentive visualisation |
| Interaction scan | After ≥3 subgroup dimensions live and detectable interaction effects |

---

## 6. Summary Table

| Category | Must | Should | Could | Won't |
|---|---|---|---|---|
| Inputs | Equity/deprivation, rurality | Practice size, demand-mix | Payment sensitivity, delivery mode | Private data, person-level |
| Subgroups | Rural vs urban, deprivation | Practice size, age, complexity | Workforce supply | — |
| Analyses | Tornado, counterfactual deltas | Variance decomp, scenario matrix, calibration-readiness | Interaction scan, regime map | Black-box solvers |
| Visuals | Tornado chart, waterfall, small multiples | Heatmap matrix, ridge/violin, uncertainty ribbon | Payoff surface, phase portrait, frontier | Opaque displays |
| Simulations | Seeded MC ensembles, cohort-stratified | Stress-test, policy shock sequences | ABM subgroup replay, regime sweep | Solver promotion (→ Track 048) |

---

## 7. Files Changed

- `docs/bleeding-edge-scorecard-v1.0.md` — updated to reflect new enhancement shortlist and Wave 1 commitments.
- `docs/decisions/enhancement-shortlist-v1.8.5.md` — this document (created).

*No code changes in this decision document. Implementation follows in separate PRs.*

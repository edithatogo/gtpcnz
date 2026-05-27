# Bleeding Edge Analytical Enhancements

## Problem

The repo already has a public educational explainer, several simulation engines, and a Nash-style heuristic lane. That is enough for a readable dashboard, but the broader analytical surface is still thin. The open question is which high-end additions would actually improve the product without drifting into unsupported forecasting or black-box modelling.

## Goal

Produce a ranked set of enhancements that can be added to the repo in a controlled way:

- additional public-data anchored inputs;
- subgroup and heterogeneity analyses;
- secondary analyses that improve interpretability;
- visualisations that expose structure rather than just outputs;
- simulation modes that broaden the educational and analytical range;
- optional solver upgrades only if they stay separated from the public explainer lane.

## Candidate Inputs

| Input family | Examples | Why it matters |
|---|---|---|
| Geography and access | rurality, remoteness, travel burden | exposes access gradients and service pressure |
| Equity and deprivation | deprivation quintile, equity strata, SES proxy | surfaces distributional effects and fairness tradeoffs |
| Practice structure | practice size, workforce mix, patient panel mix | explains heterogeneity across providers |
| Demand mix | age bands, complexity proxy, long-term-condition proxy | shows how funding rules behave under different case mixes |
| Payment sensitivity | co-payment sensitivity, activity sensitivity, control sensitivity | supports threshold and elasticity analysis |
| Delivery mode | in-person, telehealth, hybrid delivery share | shows how delivery mix changes modelled pressure |

## Candidate Subgroups

| Subgroup | Intended use |
|---|---|
| rural vs urban | access and workforce pressure contrasts |
| high vs low deprivation | equity and affordability contrasts |
| small vs large practices | scale effects and control sensitivity |
| younger vs older panels | demand-mix contrasts |
| low vs high complexity panels | utilisation and funding stress contrasts |
| high vs low workforce supply areas | service-capacity contrasts |

## Candidate Secondary Analyses

| Analysis | Purpose |
|---|---|
| tornado sensitivity | identify the most influential parameters |
| scenario matrix | compare policy options across assumptions |
| variance decomposition | separate parameter, subgroup, and stochastic contributions |
| regime map | show where the model changes behavior across parameter space |
| counterfactual deltas | compare policy changes against baseline assumptions |
| interaction scan | detect where subgroup effects differ materially |
| calibration-readiness check | identify which outputs are suitable for future calibration work |

## Candidate Visualisations

| Visualisation | Purpose |
|---|---|
| payoff surface | show incentive geometry clearly |
| phase portrait / vector field | show movement toward or away from equilibria |
| small multiples | compare subgroup behavior without overloading one chart |
| heatmap matrix | compare scenario and subgroup combinations |
| ridge / violin distribution | show uncertainty shape and spread |
| waterfall / decomposition chart | explain contribution of each driver |
| frontier plot | show tradeoff boundaries between options |
| uncertainty ribbon | show seeded stochastic spread over a policy path |

## Candidate Simulation Modes

| Simulation | Purpose |
|---|---|
| seeded Monte Carlo ensembles | reproducible uncertainty exploration |
| cohort-stratified runs | compare heterogeneous groups under the same policy |
| stress-test scenarios | probe extreme but plausible inputs |
| agent-based subgroup replay | show interaction effects across practice types |
| policy shock sequences | model abrupt changes rather than static scenarios |
| regime sweep simulation | map where outputs switch between stable regions |

## Solver Boundary

Any solver upgrade must remain a separate decision from the public explainer. If a stronger equilibrium method is added, it must be opt-in, benchmarked, and documented as analytical rather than forecast-grade.

## Decision Rules

- Prefer public-data anchored inputs over private or patient-level data.
- Prefer aggregate subgroup analysis over person-level inference.
- Prefer visualisations that explain structure over black-box outputs.
- Prefer seeded, reproducible simulations over opaque stochastic displays.
- Add a stronger solver only if it has a clear package boundary and test suite.

## Acceptance Criteria

- a ranked shortlist of enhancements exists;
- each shortlisted item has an owner, scope, and rationale;
- each item is classified as implement now, track later, or reject;
- the public claim boundary remains unchanged;
- at least one visual and one simulation enhancement are selected for the next implementation wave.

## Non-Goals

- no patient-level calibration claims;
- no hidden-data dependency;
- no unbounded model complexity just for novelty;
- no solver promotion without a separate decision gate.

## Verification

```powershell
rg -n "rural|depriv|equity|subgroup|tornado|variance decomposition|phase portrait|vector field|heatmap|violin|waterfall|frontier|ensemble|stochastic" models docs conductor
python -m pytest -q models/tests
```

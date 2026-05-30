# Red-team incorporation summary v1.7.2

## Purpose
This document records how the v1.7.1 red-team and devil's advocate reviews were incorporated into the actual project artefacts. It is intended to make the critique-to-edit pathway auditable.

## Bottom-line change
The project has shifted from a broad argument for an uncapped scheduled primary medical fee-for-service stream to a more risk-controlled proposition:

> Current reforms may be necessary but insufficient. The test is whether they change the marginal-supply game enough. A scheduled, rules-based, audited fee-for-service component for eligible primary medical activity should be considered only as part of a hybrid architecture that retains capitation, place-based accountability, equity protections, data observability and gaming controls.

## What changed because of the red-team review

| Critique | Change made | Where incorporated |
|---|---|---|
| "Uncapped" may be read as uncontrolled | Public wording now uses "uncapped at the global activity-envelope level, controlled at the item, scope, audit, data and accountability level" | `docs/concepts/risk-controlled-thesis-v1.7.2.md`; Post 6; decision-maker summary |
| Current reforms may already be substantial | Current reform pathway is treated as the active comparator, not a straw man | Post 5; decision-maker summary; launch gates |
| Too many model assumptions | 70-parameter scaffold remains, but model-card use is restricted; core claims rely on a smaller Tier 1 parameter set | `docs/calibration/model-card-v1.7.2.md`; parameter tiering retained |
| FFS may worsen equity | Equity protections, co-payment controls and Māori/Pacific review gates are presented as preconditions, not afterthoughts | Post 6; red-team launch gates; common-objection framing |
| PHO critique may be too broad | Wording remains limited to function-versus-intermediation, pass-through, transparency and non-capitated funding | launch gates; decision-maker summary |
| ACC analogy may overreach | ACC is framed only as a rules-based payment analogy, not a wholesale transplant | Post 6; decision-maker summary |
| Place-based commissioning may be more important than benefits | Place-based accountability is now a non-negotiable guardrail in the thesis | risk-controlled thesis; Post 6 |
| Hospital growth may have multiple drivers | Hospital deflection is described as a hypothesis to test, not a proven effect | model card; posts; decision-maker summary |
| RACMA may not be the right sponsor | RACMA remains excluded from active outreach; passive re-entry only | RACMA note retained and reinforced |

## What remains provisional
- No precise claim is made about reductions in emergency department demand, admissions, workforce shortage or public expenditure.
- The full parameterised scaffold is not empirically calibrated to linked New Zealand administrative data.
- Stakeholder validation, OIA responses and Māori/Pacific/equity review remain necessary before more prescriptive recommendations.

## Launch implication
The first public releases should educate before advocating. Posts 1-6 now contain stronger fair-counterargument framing and explicit statements of what would change the author's mind.

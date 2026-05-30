# Policy-option MCDA scoring rubric v0.9.0

## Criteria

| criterion_id   | criterion                                  |   default_weight | related_games    |
|:---------------|:-------------------------------------------|-----------------:|:-----------------|
| C1             | Access and supply generation               |               14 | G3, G4, G8       |
| C2             | Hospital deflection                        |               14 | G1, G2, G7       |
| C3             | Equity and Te Tiriti legitimacy            |               14 | G10, G12         |
| C4             | Rural and in-person resilience             |                9 | G7, G8, G9       |
| C5             | Fiscal sustainability                      |               12 | G1, G2, G6, G10  |
| C6             | Gaming and low-value activity risk         |               10 | G3, G5, G10, G13 |
| C7             | Administrative simplicity and market entry |                9 | G5, G8, G14      |
| C8             | Governance and clinical safety             |               10 | G8, G11, G14     |
| C9             | Political feasibility                      |                5 | G5, G12, G13     |
| C10            | Data and accountability readiness          |                8 | G11, G14         |

## Scoring steps

1. Agree on the policy options to score.
2. Agree on criteria and weights.
3. Score each option against each criterion using the -2 to +2 scale.
4. Record confidence for each score.
5. Apply risk penalties separately.
6. Run sensitivity analysis across stakeholder weight sets.
7. Interpret the ranking, not as a command, but as structured decision support.

## Default options

| option_id   | option                                           | description                                                                                                                                               |
|:------------|:-------------------------------------------------|:----------------------------------------------------------------------------------------------------------------------------------------------------------|
| O0          | Status quo tight control                         | Existing dominant capitation/PHO/contracting architecture with constrained upstream expansion.                                                            |
| O1          | Capitation reweighting only                      | Improve allocation of capitation without changing supply architecture.                                                                                    |
| O2          | Capitation reweighting plus access target        | Add top-level access target to reweighted capitation.                                                                                                     |
| O3          | Primary Care Benefits Schedule                   | Defined contact-type benefits, demand-driven within rules, retaining capitation for continuity.                                                           |
| O4          | Benefits schedule plus scope-enabled eligibility | Allow eligible activity by GPs, NPs, pharmacists, allied health, paramedics and other accredited providers within scope.                                  |
| O5          | Full upstream access architecture                | Benefits schedule plus scope governance, equity protections, direct/optional claiming, ambulance alternatives, PHO-function reform, data, KPIs and audit. |
| O6          | Loose demand-driven benefits with weak controls  | High activity funding with weak scope, audit, equity, data and co-payment controls.                                                                       |
| O7          | ACC/ambulance alternatives strengthened only     | Strengthen ambulance alternatives and ACC/prehospital funding, without primary care architecture reform.                                                  |
| O8          | PHO reform/direct claims only                    | Reduce PHO payment intermediation and allow direct rules-based claiming, without comprehensive benefits/scope reform.                                     |
| O9          | Hospital investment priority only                | Prioritise hospital capacity and acute rescue while leaving upstream access constrained.                                                                  |

## Important caution

The MCDA should never hide unresolved evidence questions. If participants disagree because evidence is weak, the correct output is not forced consensus. The correct output is a validation task.

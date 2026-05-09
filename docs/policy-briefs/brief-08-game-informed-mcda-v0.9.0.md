# Policy brief 08 - Game-informed MCDA decision support v0.9.0

## Policy question

How can decision-makers compare primary care funding architecture options when the problem involves multiple games, uncertain evidence, equity trade-offs, fiscal risk and professional politics?

## Proposal

Use a game-informed MCDA alongside the hybrid model.

The game map identifies strategic traps. The MCDA asks which traps matter most and which reform options move the system toward better equilibria.

## Why this matters

A single model output can be dismissed as assumption-driven. MCDA makes those assumptions visible. It allows different stakeholders to weight criteria differently and test whether the preferred policy architecture remains plausible under those values.

## Recommended MCDA criteria

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

## Example result

|   rank | option_id   | option                                           |   weighted_total_before_penalty |   risk_penalty |   risk_adjusted_score |
|-------:|:------------|:-------------------------------------------------|--------------------------------:|---------------:|----------------------:|
|      1 | O5          | Full upstream access architecture                |                           70.77 |          10.35 |                 60.42 |
|      2 | O3          | Primary Care Benefits Schedule                   |                           59.37 |          10.1  |                 49.27 |
|      3 | O4          | Benefits schedule plus scope-enabled eligibility |                           60.58 |          12.3  |                 48.28 |
|      4 | O2          | Capitation reweighting plus access target        |                           54.5  |           6.5  |                 48    |
|      5 | O1          | Capitation reweighting only                      |                           52.89 |           5.2  |                 47.69 |
|      6 | O7          | ACC/ambulance alternatives strengthened only     |                           55.78 |           8.2  |                 47.58 |

## Policy interpretation

The full upstream access architecture performs best in the example MCDA. A Primary Care Benefits Schedule performs well, but needs additional governance and equity protections. Loose demand-driven benefits perform poorly after risk adjustment.

## Recommended next step

Run a structured stakeholder workshop using the v0.9.0 scoring templates, then use the results to revise the scorecard and validation backlog.

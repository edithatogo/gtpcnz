# Game-informed MCDA framework v0.9.0

## Purpose

This framework adds a deliberative multi-criteria decision analysis layer to the New Zealand primary care funding architecture work. The earlier artefacts mapped the strategic games, created demonstrative models, stress-tested them under uncertainty, and synthesised them into a hybrid model. This MCDA layer is designed to help decision-makers ask a different question:

> Where do we think each game currently sits, how important is it, how confident are we, and which policy option best shifts the system toward a better equilibrium?

The MCDA is not intended to prove the policy case. It is intended to make judgement explicit. It separates empirical claims, model assumptions, value weights and implementation risk.

## Two-layer design

### Layer 1: diagnostic game-position mapping

Decision-makers score the 14 mapped games by harm, hospital growth contribution, equity relevance, tractability, reform risk and confidence. This identifies which strategic traps need attention before options are ranked.

### Layer 2: policy-option MCDA

Decision-makers score policy options against 10 criteria. Criteria weights can be varied by stakeholder perspective: balanced policy, equity and Te Tiriti, fiscal control, rural access, hospital pressure, and market entry.

## Default criteria

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

## Default policy options

| option_id   | option                                           | mapped_scenario   |
|:------------|:-------------------------------------------------|:------------------|
| O0          | Status quo tight control                         | S0                |
| O1          | Capitation reweighting only                      | S1                |
| O2          | Capitation reweighting plus access target        | S1+target         |
| O3          | Primary Care Benefits Schedule                   | S2                |
| O4          | Benefits schedule plus scope-enabled eligibility | S2+scope          |
| O5          | Full upstream access architecture                | S3                |
| O6          | Loose demand-driven benefits with weak controls  | S4                |
| O7          | ACC/ambulance alternatives strengthened only     | partial           |
| O8          | PHO reform/direct claims only                    | partial           |
| O9          | Hospital investment priority only                | hospital          |

## Scoring scale

| Score | Meaning |
|---:|---|
| -2 | Substantially worsens the criterion |
| -1 | Slightly worsens the criterion |
| 0 | No material change or genuinely uncertain direction |
| +1 | Slightly improves the criterion |
| +2 | Substantially improves the criterion |

Each score has a confidence rating from 0 to 1. Low-confidence scores are pulled toward neutral in the example model rather than being treated as certain.

## Risk adjustment

The example model applies option-level penalties for implementation risk, equity risk and fiscal/gaming risk. This is important because a policy option can score well on access while still being unsafe, inequitable or fiscally unstable.

## Default result

|   rank | option_id   | option                                           |   weighted_total_before_penalty |   risk_penalty |   risk_adjusted_score |
|-------:|:------------|:-------------------------------------------------|--------------------------------:|---------------:|----------------------:|
|      1 | O5          | Full upstream access architecture                |                           70.77 |          10.35 |                 60.42 |
|      2 | O3          | Primary Care Benefits Schedule                   |                           59.37 |          10.1  |                 49.27 |
|      3 | O4          | Benefits schedule plus scope-enabled eligibility |                           60.58 |          12.3  |                 48.28 |
|      4 | O2          | Capitation reweighting plus access target        |                           54.5  |           6.5  |                 48    |
|      5 | O1          | Capitation reweighting only                      |                           52.89 |           5.2  |                 47.69 |
|      6 | O7          | ACC/ambulance alternatives strengthened only     |                           55.78 |           8.2  |                 47.58 |
|      7 | O8          | PHO reform/direct claims only                    |                           53.72 |          12.25 |                 41.47 |
|      8 | O9          | Hospital investment priority only                |                           48.04 |           8    |                 40.04 |
|      9 | O0          | Status quo tight control                         |                           40.9  |           7.5  |                 33.4  |
|     10 | O6          | Loose demand-driven benefits with weak controls  |                           47.33 |          22.75 |                 24.58 |

The default demonstrative MCDA ranks the full upstream access architecture first, followed by the Primary Care Benefits Schedule and the benefits schedule plus scope-enabled eligibility. Loose benefits with weak controls rank last after risk adjustment.

## Interpretation

The MCDA supports the same core conclusion as the hybrid model, but through a decision-maker lens:

> Demand-driven within rules; not demand-driven without rules.

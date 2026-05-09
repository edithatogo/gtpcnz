---
title: "New Zealand primary care, ambulance and hospital funding: game-theoretic map"
version: "0.4.0"
status: "working technical map"
last_updated: "2026-05-07"
owner: "Dylan A Mordaunt"
---

# New Zealand primary care, ambulance and hospital funding: game-theoretic map

## Status

This is the first full game-theoretic map of the New Zealand problem as currently framed. Earlier project versions contained a general payoff-model scaffold. This version maps the broader NZ policy problem explicitly: primary care, ambulance/prehospital care, Health NZ budget competition, PHO intermediation, capitation, professional scope constraints, consumer co-payment behaviour, health targets and hospital pressure.

It is a policy-modelling framework, not proof. Its purpose is to make the hypothesised mechanisms explicit enough to test with simulation modelling, qualitative evidence and administrative data.

## One-sentence thesis

New Zealand may be tightly managing activity and expenditure in lower-cost upstream sectors - primary care, urgent care and ambulance/prehospital care - in ways that unintentionally channel unmet demand into the higher-cost, more visible hospital system.

## Central game-theoretic claim

The problem is not one simple game. It is a nested repeated game with multiple principals, multiple agents, incomplete information, asymmetric political salience, weakly observed upstream failure, and strong hospital rescue incentives.

The key equilibrium risk is:

> Tight upstream control + weak marginal supply incentives + provider/professional entry barriers + high co-payment/waiting costs -> delayed or displaced care -> visible hospital and ambulance pressure -> hospital rescue funding -> continued upstream constraint.

This can be described as **hospital-rescue dominance**.

## Public-policy anchors

1. The current NZ capitation reweighting work is a technical allocation exercise, not a fundamental redesign of the primary care funding model. The released Sapere briefing states that the work has not considered fundamental changes to the overall funding model for primary care.
2. The Health and Disability System Review recommended more flexible Tier 1 arrangements, including moving away from mandatory PHO contracting and increasingly paying providers directly through new commissioning arrangements.
3. Recent Cabinet material states that over the previous five years hospital funding increased by nearly 53%, while primary and community care rose by 41%, and that this means opportunities to intervene earlier are being missed.
4. A new primary care access target and National Primary Care Dataset are being introduced, but targets alone do not generate supply unless the funding and workforce architecture make additional contacts viable.
5. Ambulance services are commissioned by Health NZ and ACC. Ambulance performance is measured, but the strategic accountability for ambulance as hospital-avoidance infrastructure is not yet equivalent to hospital targets.

## Map of actors

| Actor | Formal role in the model | Main incentives | Information problem |
|---|---|---|---|
| Ministers / Cabinet | Political principal | visible access, fiscal discipline, hospital stability, election risk | upstream failure is less visible than hospital failure |
| Treasury | fiscal/value principal | whole-of-Crown exposure, value for money, macro-fiscal control | siloed health cost shifts may be hard to see |
| Ministry of Health | steward, policy adviser, monitor | system settings, equity, performance, advice quality | limited operational visibility unless datasets mature |
| Health NZ | commissioner and hospital operator | meeting targets, controlling deficits, delivering hospitals, commissioning services | dual role creates asymmetric salience: hospitals are direct and visible |
| ACC | injury funder and purchaser | claims cost, injury rehabilitation, scheme sustainability | constrained ACC FFS may affect general primary care supply |
| PHOs/locality intermediaries | contract/payment/data/support intermediaries | organisational survival, coordination, programme delivery | transaction costs and margins may be opaque |
| Primary care providers | supply agents | viability, workload, professional autonomy, patient care, risk | demand/unmet need is observed locally but not always nationally |
| Pharmacists/NPs/allied health/Maori/Pacific providers | potential supply entrants | scope utilisation, viability, patient access | funding may not follow scope capability |
| Ambulance/paramedic providers | prehospital access agents | response, conveyance, safety, workforce capacity | alternative pathways may be underfunded or unavailable |
| Hospitals/ED | visible pressure domain | throughput, safety, target performance, deficit control | demand appears unavoidable once it arrives |
| Patients/whanau | consumers and voters | access, price, continuity, cultural safety, travel, trust | may lack clear signals about appropriate pathway |

## Core repeated game

### Sequence

1. Government and Health NZ set budget architecture and targets.
2. Health NZ allocates attention and resources across hospitals, primary/community care, ambulance and other priorities.
3. Primary/urgent/ambulance providers decide whether to expand, maintain or ration supply.
4. Consumers decide whether to seek early care, delay, use telehealth, call ambulance or attend ED.
5. Unmet need either resolves, worsens, or appears as ambulance/ED/hospital demand.
6. Hospital pressure becomes politically visible.
7. Government responds with hospital rescue, upstream reform, or both.
8. The next period begins with changed baselines, expectations and provider viability.

### Simplified dynamic

```text
H_t = baseline_hospital_demand_t
      + alpha * unmet_primary_need_t
      + beta * ambulance_conveyance_t
      - gamma * upstream_resolution_t

unmet_primary_need_t = need_t - accessible_upstream_contacts_t

accessible_upstream_contacts_t = f(provider_FTE, scope_eligible_providers,
                                   marginal_payment, co-payment, wait,
                                   rurality, transaction_cost, governance)
```

### Equilibrium risk

If hospital pressure has a high immediate political penalty and upstream access failure has a low immediate political penalty, the rational repeated-game response is to protect hospital delivery first. This can persist even if upstream investment would be more efficient over the long run.

## Game 1: Health NZ budget and salience game

### Players

- Government/Minister
- Treasury
- Ministry of Health
- Health NZ
- Hospitals
- Primary/community/ambulance sectors

### Strategies

| Player | Strategy set |
|---|---|
| Government | hospital rescue; upstream reform; target-only reform; demand-driven benefits |
| Health NZ | allocate to visible hospital pressure; maintain tight upstream control; expand upstream payment architecture |
| Treasury | constrain fiscal exposure; require modelling of whole-system costs; permit demand-driven benefit stream with controls |
| Upstream sectors | maintain, ration, expand if funded |

### Payoff logic

```text
Government payoff = - public_expenditure
                    - political_penalty(hospital_pressure)
                    - political_penalty(access_failure)
                    - equity_penalty
                    + system_performance
```

The hypothesis is that the political penalty for hospital pressure is larger, faster and more concentrated than the penalty for primary care access failure. Health NZ also operates hospitals directly, while much general practice is privately provided and mediated through contracts. That asymmetry changes the game.

### Predicted equilibrium under current architecture

- Health NZ prioritises hospital stability when under pressure.
- Primary/community initiatives are considered from within baselines or tightly managed programme funding.
- Hospital rescue becomes recurrent.
- Upstream failure is recognised rhetorically but remains structurally constrained.

### Policy lever

Do not simply ring-fence a fixed upstream pool. Instead, create a rules-based demand-driven benefits stream for specified upstream contacts, with transaction-level controls and system-level fiscal monitoring.

## Game 2: Capitation marginal-supply game

### Players

- Funder/Health NZ/PHO
- General practice or primary care provider
- Patient

### Strategies

| Player | Strategy set |
|---|---|
| Funder | fixed capitation; reweighted capitation; blended capitation + contact benefits |
| Provider | expand contacts; maintain contacts; ration by closed books/wait/co-payments/short visits |
| Patient | seek early care; delay; use ED/ambulance; use telehealth |

### Payoff logic

```text
Provider payoff = capitation
                  + contact_benefit * eligible_contacts
                  + co_payments
                  + ACC_revenue
                  + programme_funding
                  - marginal_cost(contacts)
                  - admin_cost
                  - governance_risk
                  - burnout_cost
```

Under dominant capitation, the marginal payment for additional clinically necessary work may be weak or zero. If marginal cost exceeds marginal revenue, the provider response is rationing, higher co-payments, shorter visits or exit. Reweighting can improve distribution, but if it is funded from an existing baseline and does not add a meaningful marginal contact payment, it may not materially expand supply.

### Predicted equilibrium under reweighting-only

- Better allocation between enrolled populations.
- Possible redistribution between practices.
- Limited expansion of total contacts unless workforce and marginal payment improve.
- Ongoing pressure on co-payments and waiting time.

### Policy lever

Define eligible primary care contact types and pay a public benefit when an accredited provider supplies them within scope. Keep capitation for continuity, baseline viability and population accountability, but do not make it the sole or dominant access mechanism.

## Game 3: Consumer co-payment and pathway game

### Players

- Patient/whanau
- Primary/urgent care provider
- Ambulance/ED/hospital system
- Funder

### Strategies

| Patient strategy | Conditions that make it more likely |
|---|---|
| Early primary care | low/moderate co-payment, short wait, trusted provider, local access |
| Delay/forgo care | high co-payment, long wait, transport/digital barriers, distrust |
| ED/ambulance | urgent symptoms, no appointment, after-hours gap, zero/low direct ED price |
| Telehealth | convenience, digital access, low complexity, acceptable continuity trade-off |

### Payoff logic

```text
Patient payoff = health_benefit
                 - co_payment
                 - waiting_cost
                 - travel_cost
                 - uncertainty
                 - fragmentation_cost
                 + continuity/trust/cultural_safety
```

Co-payment can be a demand signal, but it can also become an equity failure mechanism. The model should treat co-payment settings as a policy instrument that calibrates demand, not as an unqualified virtue.

### Predicted equilibrium if co-payment + wait too high

- Lower-value demand may fall, but high-need patients may also delay.
- Delayed care can return as ED, ambulance or hospital demand.
- Equity gaps widen unless protections are built into the benefit schedule.

### Policy lever

Use co-payments as a calibrated signal, with exemptions, caps or higher public benefit for children, community services card holders, high-deprivation populations, rurality, multimorbidity and priority contact types.

## Game 4: Professional-scope and supply-entry game

### Players

- Professional groups and regulators
- Funder/payment system
- Providers
- Patients

### Strategies

| Architecture | Consequence |
|---|---|
| Doctor/practice-enrolment constrained | low supply elasticity; entry barriers; GP bottleneck |
| Scope-based provider eligibility | higher supply elasticity; need stronger governance and data |
| Unrestricted provider activity without governance | safety/fragmentation risk |

### Payoff logic

Traditional funding architecture can unintentionally enforce professional constraints beyond clinical law. If public benefits are only available through a GP-centred enrolment model, supply expansion by pharmacists, nurse practitioners, physiotherapists, paramedics, psychologists, Maori/Pacific providers or community providers is artificially limited even where scope and governance permit care.

### Predicted equilibrium under professional constraint

- GP time remains the scarce bottleneck.
- Other workforce capacity is underused.
- Hospitals and ED become the pathway of last resort.

### Policy lever

Define payment eligibility by contact type + scope + credentialing + clinical governance + data reporting, not by professional guild or traditional practice structure alone.

## Game 5: PHO intermediation and transaction-cost game

### Players

- Health NZ
- PHOs/locality intermediaries
- Practices and new entrants
- Patients/communities

### Strategies

| PHO/locality role | Potential value | Potential cost |
|---|---|---|
| Population health | equity, outreach, data, local intelligence | unclear accountability if not measured |
| Quality improvement | practice support, programme delivery | administrative burden |
| Payment gateway | contract management, pass-through | transaction cost, opacity, entry barrier |
| Locality coordination | integration and planning | incumbency protection |

### Game-theoretic interpretation

PHOs may reduce coordination costs, but they may also create transaction costs, principal-agent distance and barriers to entry. The game is not "PHO good" versus "PHO bad". It is whether specific PHO functions lower or raise the cost of generating timely, safe, equitable upstream contacts.

### Predicted equilibrium under mandatory intermediation

- Incumbents have stronger bargaining position.
- New entrants must navigate contract and enrolment pathways before generating publicly subsidised activity.
- Payment architecture becomes less portable and less contestable.

### Policy lever

Separate PHO/locality functions from payment intermediation. Allow direct benefits claims for eligible contact types while separately commissioning population health, equity, outreach and locality coordination functions.

## Game 6: Ambulance conveyance and alternative-pathway game

### Players

- Ambulance providers/paramedics
- Health NZ
- ACC
- ED/hospitals
- Primary/urgent care providers
- Patients/whanau

### Strategies

| Strategy | Consequence |
|---|---|
| Convey to ED | clinically safe default, but increases ED/hospital pressure |
| Hear-and-treat | avoids conveyance for suitable calls, requires governance and follow-up |
| Treat-and-refer | resolves or diverts care, requires accessible downstream provider |
| Alternative destination | urgent care or primary pathway, requires funded capacity |

### Payoff logic

```text
Ambulance payoff = safety + response_performance + workforce_sustainability
                   - clinical_risk
                   - offload_delay
                   - lack_of_downstream_options
```

If alternative pathways are not funded, governed and available, conveyance becomes the dominant safe strategy. This can be rational for ambulance providers even if it is not optimal for the whole system.

### Predicted equilibrium under constrained upstream care

- More calls become ED conveyance problems.
- Offload delay/ramping risk increases.
- Ambulance is treated as transport rather than access infrastructure.

### Policy lever

Add ambulance and urgent primary care contact types to the benefits schedule: hear-and-treat, treat-and-refer, paramedic-initiated follow-up, rural extended-care paramedic contacts, and safe alternative-destination pathways.

## Game 7: Targets, KPIs and salience game

### Players

- Government/Minister
- Health NZ executives and regions
- Hospitals
- Primary/ambulance providers
- Public/media

### Strategies

| Target design | Behavioural implication |
|---|---|
| Hospital-heavy top-tier targets | hospital optimisation dominates |
| Primary care target without supply payment | pressure without capacity |
| Primary + ambulance + hospital top-tier targets | upstream access becomes politically salient |
| Dataset without payment reform | better measurement of a constrained system |

### Game-theoretic interpretation

What is measured at the top tier becomes salient. If hospital metrics dominate executive attention and political accountability, managers will rationally optimise hospital metrics, even if upstream access would reduce avoidable demand over time.

### Policy lever

Place primary care and ambulance KPIs at hospital-equivalent accountability level. Candidate top-tier domains:

- timely primary care access;
- urgent/same-day primary care access;
- open-books/enrolment access;
- co-payment burden;
- continuity;
- rural in-person access;
- ambulance response;
- ambulance non-conveyance with safe follow-up;
- ambulance offload delay;
- potentially preventable hospitalisations;
- lower-urgency ED attendances, interpreted cautiously.

## Game 8: Political economy game

### Players

- Political parties
- Ministers
- Health NZ
- Treasury
- PHOs and provider organisations
- Professional colleges
- Patient groups
- Media/public

### Strategies

| Actor | Likely move |
|---|---|
| Incumbent intermediaries | defend existing role; emphasise coordination and equity |
| Professional groups | defend quality and scope; seek funding for own members |
| Government | seek visible access improvement within fiscal control |
| Treasury | avoid uncapped fiscal risk without evidence |
| Patients | value actual access more than architecture |

### Equilibrium risk

The policy debate collapses into "more money for GPs" versus "protect capitation/equity", missing the larger design problem: whether lower-cost sectors are structurally prevented from expanding supply.

### Policy lever

Frame the proposal as a whole-system, non-partisan, rules-based access architecture: public benefits for defined contact types; scope-based provider eligibility; governance and audit; calibrated co-payments; and top-tier accountability for primary care and ambulance outcomes.

## Summary of hypothesised equilibria

| Game | Current equilibrium risk | Reform equilibrium sought |
|---|---|---|
| Budget/salience | hospital rescue dominance | upstream access treated as a top-tier performance and fiscal domain |
| Capitation | distribution improved but supply constrained | capitation + demand-driven contact benefits |
| Consumer pathway | delay/ED when price or wait high | early care when benefit/co-pay/wait are calibrated |
| Professional scope | GP bottleneck | scope-based supply generation |
| PHO intermediation | incumbent friction | direct payment plus separately funded coordination functions |
| Ambulance | conveyance default | safe alternative pathways and treat-and-refer |
| Targets | hospital metrics dominate | primary/ambulance/hospital metrics at equivalent level |
| Political economy | sector funding debate | system-design debate |

## Testable hypotheses

H1. Capitation reweighting improves distribution but does not materially increase total accessible primary care contacts unless accompanied by activity-sensitive benefits or workforce expansion.

H2. A demand-driven primary care benefits schedule increases supply where provider capacity exists or can enter, especially if eligibility is based on contact type and scope rather than GP-only models.

H3. PHO intermediation increases transaction cost and entry friction for some providers, but PHO/locality functions may still add value for equity, outreach and coordination.

H4. ACC fee-for-service and injury-related activity subsidise general practice viability and may partly mitigate capitation-related supply constraints.

H5. Constraining ambulance and urgent primary care pathways increases ED/hospital pressure unless alternative contact types are funded and governed.

H6. Top-tier primary care and ambulance KPIs increase executive and political salience and alter allocation behaviour.

H7. Co-payment calibration determines whether a demand-driven model improves access or worsens inequity.

## What would falsify the theory?

The theory should be weakened if:

- reweighting capitation from baseline funding produces substantial improvements in waits, open books, rural in-person access and co-payment burden;
- broader scope-based provider eligibility does not increase supply;
- direct benefits payment does not reduce transaction costs or improve entry;
- PHO intermediation demonstrably improves access and equity at lower total transaction cost than direct payment alternatives;
- ambulance alternative pathways do not reduce avoidable ED conveyance or hospital pressure;
- top-tier primary/ambulance KPIs do not change resource allocation or operational focus;
- co-payment settings cannot be made compatible with equity.

## Modelling implication

A realistic simulation should not model capitation, fee-for-service and hospital demand as isolated financing instruments. It should model:

- provider supply response;
- patient pathway choice;
- co-payment sensitivity;
- PHO transaction costs;
- professional scope constraints;
- ambulance conveyance and alternative pathways;
- Health NZ budget salience;
- hospital rescue response;
- equity, rurality and unmet need.

The next modelling step is to translate this map into a system dynamics model and an agent-based model with explicit scenario testing.

## Sources to verify and maintain

- Ministry of Health. The Sapere report and re-weighting primary care capitation funding. Briefing H2024057558.
- Ministry of Health. Reweighting capitation funding in primary care. Briefing H2025066443.
- Ministry of Health. Primary health care priorities: next steps to improve capitation funding. Briefing H2025067084.
- Health and Disability System Review. Final Report. 2020.
- Ministry of Health. Cabinet paper: Health NZ's progress towards financial stability and improving delivery. 2026.
- Ministry of Health. Primary care health target.
- Health New Zealand. National Primary Care Dataset and new primary care health target.
- Health New Zealand. The Ambulance Team.

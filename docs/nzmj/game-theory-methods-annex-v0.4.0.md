---
title: "NZMJ methods annex: game-theoretic mapping"
version: "0.4.0"
status: "draft annex"
last_updated: "2026-05-07"
owner: "Dylan A Mordaunt"
track: "008-nz-game-theory-map"
---

# NZMJ methods annex: game-theoretic mapping

## Purpose

This annex supports a potential NZMJ Viewpoint or Article by specifying how the game-theory component could be presented in a publishable way.

## Proposed article placement

In a Viewpoint, the game-theory map can appear as:

- one short conceptual section;
- one table of players, strategies and failure modes;
- one figure showing the repeated hospital-rescue loop.

In an Original Article, it can be placed in the Methods section as a formal policy-game mapping exercise, combined with system dynamics and agent-based modelling.

## Suggested methods wording

We conceptualised New Zealand primary care, ambulance and hospital funding architecture as a repeated, partially observed policy game. Actors included Ministers and central agencies, Health New Zealand, hospital services, primary care providers, PHOs/locality intermediaries, ambulance providers, ACC, regulators and consumers. Strategies were mapped from publicly described funding and accountability mechanisms, including capitation, PHO-mediated commissioning, ambulance commissioning, proposed primary care access targets and hospital performance accountability.

We then identified mechanisms by which local rationality could produce system-level inefficiency. These mechanisms included asymmetric observability of hospital versus primary care access failure, weak marginal revenue under capitation, transaction costs and information asymmetry associated with intermediation, cross-funder externalities between ACC and Health NZ, and safety/liability incentives influencing ambulance conveyance decisions. Each mechanism was translated into a testable simulation hypothesis.

## Proposed Table 1: policy-game map

| Game | Players | Mechanism | Hypothesised equilibrium | Testable prediction |
|---|---|---|---|---|
| Hospital-salience budget game | Ministers, Treasury, Health NZ, hospitals | Visible hospital pressure dominates dispersed upstream access failure | recurrent hospital rescue | hospital expenditure and management attention grow faster than upstream access capacity |
| Capitation supply game | practices, patients, Health NZ/PHOs | marginal contacts have positive cost but weak marginal public payment | supply rationing | reweighting alone improves distribution but not total contact availability |
| PHO intermediation game | PHOs, practices, Health NZ, entrants | intermediation can coordinate or create friction | mixed value; possible entry barriers | direct/optional claiming reduces administrative delay if population-health functions are preserved |
| ACC spillover game | ACC, Health NZ, practices | injury FFS may stabilise practice viability | siloed optimisation | constraining ACC FFS may reduce overall practice viability and shift demand |
| Ambulance conveyance game | ambulance, ED, funders, patients | conveyance may be safer organisationally than alternatives | ED as default destination | funded treat-and-refer and safe follow-up reduce ED conveyance |
| Scope-of-practice game | providers, regulators, funders | funding eligibility narrower than clinical scope constrains supply | professional bottleneck | broader eligibility increases supply elasticity without quality loss if governed |
| Data salience game | Health NZ, Ministry, practices | unmeasured upstream failure remains residual | hospital target dominance | top-tier primary and ambulance KPIs shift attention and resource allocation |

## Proposed Figure 1: repeated hospital-rescue loop

```text
Tight upstream funding and payment/professional constraints
-> constrained primary, urgent and ambulance supply
-> unmet or delayed need
-> ED, ambulance and hospital pressure
-> visible target, media and deficit pressure
-> hospital rescue funding
-> renewed upstream constraint
```

## Simulation hypotheses

1. Reweighted capitation improves allocation but not necessarily marginal supply.
2. Provider supply expansion occurs when benefit plus co-payment exceeds marginal, administration and governance costs.
3. Broader provider eligibility increases supply elasticity.
4. Co-payment safety nets are necessary to prevent equity failure.
5. Ambulance alternatives reduce ED pressure only when payment, clinical governance and liability rules are aligned.
6. Top-tier primary and ambulance KPIs alter funder behaviour by increasing the salience of upstream failure.

## Reporting standards

The empirical version should use simulation reporting guidance, an explicit agent-based model description protocol, and health economic reporting guidance if a formal economic evaluation component is included.

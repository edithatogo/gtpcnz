---
title: "Formal game-theory model for the NZ primary care, ambulance and hospital funding problem"
version: "0.4.0"
status: "mathematical scaffold"
last_updated: "2026-05-07"
owner: "Dylan A Mordaunt"
track: "008-nz-game-theory-map"
---

# Formal game-theory model for the NZ primary care, ambulance and hospital funding problem

This document provides a mathematical scaffold for the NZ policy-game atlas. It is not a calibrated empirical model.

## Nested game

Represent the New Zealand policy problem as:

```text
G_NZ = {G_B, G_H, G_C, G_P, G_A, G_S, G_T, G_K, G_E, G_D}
```

where:

- G_B = budget allocation and hospital-rescue game;
- G_H = Health NZ internal allocation game;
- G_C = capitation and marginal supply game;
- G_P = PHO/intermediation and transaction-cost game;
- G_A = ambulance conveyance and alternative-pathway game;
- G_S = professional-scope and provider-entry game;
- G_T = telehealth/local supply game;
- G_K = KPI and target-gaming game;
- G_E = equity and co-payment mechanism-design game;
- G_D = data observability game.

## State variables

```text
D_t = population demand for lower-cost first-contact, urgent and prehospital care
Q_t = accessible primary/urgent/ambulance-resolved contacts
U_t = max(0, D_t - Q_t) = unmet or delayed need
H_t = hospital pressure
A_t = ambulance conveyance pressure
R_t = reported target performance
X_t = true patient access
E_t = equity gap
S_t = safety or gaming failure penalty
V_t = effective upstream hospital avoidance
```

Hospital pressure evolves as:

```text
H_(t+1) = rho * H_t + alpha * U_t + beta * A_t - gamma * V_t + epsilon_t
```

## Provider supply decision

For provider i and contact type j, supply occurs if:

```text
MR_ij + p_j + v_ij - MC_ij - Admin_i - Risk_i > 0
```

Under dominant capitation for an enrolled patient:

```text
MR_ij ~= 0
```

for additional contacts, unless the work is covered by another programme, ACC or patient co-payment.

Under a contact-benefit schedule:

```text
MR_ij = B_j * W_ij
```

where B_j is the public benefit for contact type j and W_ij is an eligibility/weighting term reflecting complexity, rurality, deprivation, scope and clinical governance.

## Patient pathway choice

Patient n chooses option k from primary care, telehealth, pharmacy, ambulance, ED or delay:

```text
utility_nk = health_gain_nk
             - copay_nk
             - wait_nk
             - travel_nk
             - trust_penalty_nk
             - fragmentation_nk
```

Co-payment is therefore both a demand signal and an equity risk.

## Funder payoff

```text
F_t = - C_primary_t
      - C_ambulance_t
      - C_hospital_t
      - hospital_pressure_penalty_t
      - equity_penalty_t
      - safety_or_gaming_penalty_t
      + avoided_escalation_value_t
```

The policy question is whether increasing primary and ambulance expenditure through controlled contact benefits reduces hospital expenditure and pressure enough to improve patient welfare and whole-system fiscal value.

## KPI gaming

Let R_t be reported access performance and X_t true access. In a weak audit environment:

```text
R_t = X_t + metric_management_t
```

A single target can therefore produce apparent improvement without equivalent access gains.

## Equilibria

### E0: hospital-rescue equilibrium

Conditions:

- hospital salience is high;
- upstream benefit marginal signal is weak;
- hospitals are directly managed;
- primary and ambulance access indicators have lower salience;
- the budget cycle is short relative to prevention lags.

Provider best response: ration or maintain supply.
Funder best response: protect hospital delivery first.

### E1: capitation-rationing equilibrium

Conditions:

- additional contacts weakly funded;
- provider marginal cost positive;
- workforce scarce;
- co-payment constrained by affordability or politics.

Provider best response: ration supply rather than expand.

### E2: regulated contact-benefit expansion equilibrium

Conditions:

- benefits exceed marginal cost for desired contacts;
- provider scope is broad enough;
- co-payment protects equity;
- audit reduces gaming;
- performance measures include quality and hospital avoidance.

Provider best response: expand eligible supply.

### E3: uncontrolled activity equilibrium

Conditions:

- benefits are too high for low-value contacts;
- eligibility is too broad;
- audit is weak;
- continuity and safety are not measured.

Provider best response: volume expansion. Funder response: reversal or renewed constraint.

## Scenario set

| Scenario | Description |
|---|---|
| S0 | Status quo / tight upstream control |
| S1 | Capitation reweighting only |
| S2 | Reweighting plus access target but no supply architecture change |
| S3 | Benefits schedule for GP-only contacts |
| S4 | Benefits schedule with broad provider eligibility |
| S5 | Benefits schedule plus co-payment safety nets |
| S6 | Benefits schedule plus ambulance alternatives |
| S7 | PHO optional/direct claiming |
| S8 | ACC activity payment constrained in isolation |
| S9 | Telehealth-only expansion |
| S10 | Top-tier primary care and ambulance KPIs |

## Falsification criteria

The model should be revised if empirical data show:

1. reweighted capitation alone materially expands access and reduces hospital pressure;
2. contact benefits produce mainly low-value volume without access or hospital-avoidance gains;
3. PHO intermediation has no material effect on transaction cost or market entry;
4. scope-based claims produce unacceptable safety failures;
5. ambulance non-conveyance alternatives do not safely reduce ED demand;
6. ACC activity is unrelated to primary care practice viability or broader supply;
7. primary care and ambulance top-tier KPIs do not change organisational behaviour.

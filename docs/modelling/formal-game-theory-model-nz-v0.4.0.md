---
title: "Formal game-theory model for the NZ primary care architecture problem"
version: "0.4.0"
status: "mathematical scaffold"
---

# Formal game-theory model for the NZ primary care architecture problem

This is a modelling scaffold, not a calibrated empirical model.

## Nested game

Represent the New Zealand policy problem as:

```text
G_NZ = {G_B, G_C, G_I, G_S, G_A, G_K, G_E}
```

where:

- G_B = budget allocation and hospital-rescue game;
- G_C = capitation and marginal supply game;
- G_I = intermediation and PHO transaction-cost game;
- G_S = professional-scope and provider-entry game;
- G_A = ambulance conveyance and alternative-pathway game;
- G_K = KPI and target-gaming game;
- G_E = equity and co-payment mechanism-design game.

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
S_t = safety/gaming failure penalty
```

Hospital pressure evolves as:

```text
H_(t+1) = rho * H_t + alpha * U_t + beta * A_t - gamma * V_t + error_t
```

where V_t is effective upstream hospital avoidance.

## Provider supply under capitation

For provider i and contact type j, supply occurs if:

```text
MR_ij + p_j + v_ij - MC_ij - Admin_i - Risk_i > 0
```

Under dominant capitation for an enrolled patient:

```text
MR_ij is approximately 0
```

for additional contacts, unless the work is covered by another programme, ACC or patient co-payment.

Under a contact-benefit schedule:

```text
MR_ij = B_j * W_ij
```

where B_j is the public benefit for contact type j and W_ij is an eligibility/weighting term reflecting complexity, rurality, deprivation, scope and clinical governance.

## Patient choice

Patient n chooses option k from primary care, telehealth, pharmacy, ambulance, ED or delay:

```text
utility_nk = health_gain_nk
             - copay_nk
             - wait_nk
             - travel_nk
             - trust_penalty_nk
             - fragmentation_nk
```

A patient chooses the option with the highest utility. Co-payment is therefore both a demand signal and an equity risk.

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

### Hospital-rescue equilibrium

Conditions:

- hospital salience high;
- upstream benefit marginal signal weak;
- hospital pressure directly managed;
- primary/ambulance access indicators lower salience;
- budget cycle short relative to prevention lag.

### Capitation-rationing equilibrium

Conditions:

- additional contacts weakly funded;
- provider marginal cost positive;
- workforce scarce;
- patient co-payment constrained by affordability or politics.

Provider best response: ration supply rather than expand.

### Regulated contact-benefit expansion equilibrium

Conditions:

- benefits exceed marginal cost for desired contacts;
- provider scope is broad enough;
- co-payment protects equity;
- audit reduces gaming;
- performance measures include quality and hospital avoidance.

Provider best response: expand eligible supply.

## Falsification criteria

The model should be revised if empirical data show:

1. Reweighted capitation alone materially expands access and reduces hospital pressure.
2. Contact benefits produce mainly low-value volume without access or hospital-avoidance gains.
3. PHO intermediation has no material effect on transaction cost or market entry.
4. Scope-based claims produce unacceptable safety failures.
5. Ambulance non-conveyance alternatives do not safely reduce ED demand.
6. ACC activity is unrelated to primary care practice viability or broader supply.

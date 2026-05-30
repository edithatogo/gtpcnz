# NZMJ methods section draft: game-theoretic mapping

**Version:** v0.4.0  
**Use:** Insert into NZMJ Viewpoint, Article protocol or technical appendix.

## Game-theoretic mapping method

We conceptualised New Zealand primary care funding architecture as a nested set of policy games rather than a single dyadic interaction. The mapping was developed to identify incentive-compatible and incentive-incompatible features of current and proposed funding arrangements, with particular attention to the relationship between primary care, ambulance/prehospital care and hospital demand.

The mapping proceeded in five steps.

First, we defined the system boundary as publicly funded or publicly subsidised first-contact, urgent, community and prehospital care in Aotearoa New Zealand. This included general practice, PHO-mediated funding, ACC-related injury contacts, ambulance/prehospital care and Health New Zealand hospital-pressure effects. Pharmaceutical and medical device funding were excluded from the first model.

Second, we identified actor classes and payoff domains. Actor classes included Cabinet and Ministers, Treasury, the Ministry of Health, Health New Zealand, PHOs/locality intermediaries, primary care providers, ambulance providers, ACC, patients/whanau and professional groups. Payoff domains included fiscal exposure, hospital pressure, political salience, provider viability, patient access, equity, safety, data transparency and administrative burden.

Third, we classified each interaction using standard game-theoretic or adjacent economic frames: repeated game, principal-agent problem, common-pool budget game, transaction-cost game, mechanism-design problem, congestion game, adverse-selection game, audit/target-gaming game, coalition/guild game and bargaining game.

Fourth, we specified likely status-quo equilibria and candidate policy levers. These included a hospital-rescue equilibrium, capitation-rationing equilibrium, PHO-intermediary persistence equilibrium, scope-bottleneck equilibrium, conveyance-default equilibrium, metric-management equilibrium and telehealth low-complexity capture equilibrium.

Fifth, we translated the map into testable modelling hypotheses for future system dynamics and agent-based modelling. Variables include appointment availability, enrolment status, provider marginal revenue and cost, co-payment burden, ambulance conveyance, non-conveyance outcomes, ED use, ambulatory-sensitive hospitalisation, patient-reported unmet need, provider type and rurality.

## Formal model summary

Let D_t represent underlying primary, urgent and prehospital demand in period t, Q_t lower-cost accessible contacts supplied, and U_t = max(0, D_t - Q_t) unmet or delayed need. Let H_t represent hospital pressure and A_t ambulance conveyance pressure. Under dominant capitation, the marginal public benefit for additional contacts after enrolment is approximated as weak or zero. Under a Primary Care Benefits Schedule, a contact-specific public benefit B_j is paid for eligible contact type j, subject to provider scope and clinical governance eligibility.

Provider i supplies contact type j where:

```text
B_j + p_j + v_ij - c_ij - r_i > 0 and g_ij = 1
```

Hospital pressure evolves as:

```text
H_(t+1) = rho * H_t + alpha * U_t + beta * A_t - gamma * V_t
```

where V_t represents effective upstream hospital avoidance.

## Interpretation

The mapping does not assume that capitation is intrinsically inferior to fee-for-service. Rather, it identifies a failure mode of dominant capitation in a constrained supply environment: the marginal clinically necessary contact may be weakly funded even where patient need is high. Reweighted capitation may improve distribution across enrolled populations but may not change the provider best response unless paired with a marginal access signal, scope-based provider eligibility and balanced accountability.

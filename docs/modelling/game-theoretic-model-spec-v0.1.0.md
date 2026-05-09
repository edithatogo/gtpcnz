---
title: "Game-theoretic model specification"
version: "0.1.0"
status: "draft"
last_updated: "2026-05-07"
owner: "Dylan A Mordaunt"
next_review: "2026-05-21"
---


# Game-theoretic model specification

## Purpose

Formalise the strategic interactions that may lead to hospital growth under constrained upstream funding.

## Minimal repeated game

### Players

1. Funder/government.
2. Upstream providers.
3. Hospital system.
4. Consumers.

### Period sequence

1. Funder chooses upstream architecture: constrained capitation/contracting or demand-driven contact benefits.
2. Providers choose supply level: expand, maintain or ration.
3. Consumers choose early care, delayed care or ED/ambulance.
4. Hospital demand materialises.
5. Funder responds to hospital pressure.
6. Next period begins with changed budgets and provider viability.

## Payoffs

Funder payoff:

`U_F = - public_cost - political_penalty_hospital - political_penalty_copayment - equity_penalty + hospital_avoidance_benefit`

Provider payoff:

`U_P = revenue - marginal_cost - admin_cost - burnout_cost + professional_utility`

Consumer payoff:

`U_C = health_benefit - copayment - waiting_cost - travel_cost - fragmentation_cost`

Hospital payoff/system pressure:

`H = baseline_demand + avoidable_flow_from_unmet_need + ambulance_conveyance - avoided_by_upstream_resolution`

## Equilibrium hypothesis

Under high hospital political penalty and weak upstream marginal revenue, the repeated-game equilibrium favours hospital rescue and provider rationing.

Under contact-type benefits, broader provider eligibility and co-payment/equity controls, a different equilibrium may emerge in which upstream supply expands and hospital avoidable flow is reduced.

## Parameters to estimate or vary

- political salience of hospital pressure;
- elasticity of patient demand to co-payment;
- elasticity of provider supply to marginal payment;
- transaction cost of PHO intermediation;
- substitution rate across provider types;
- probability that unmet primary need becomes ED/hospital demand;
- fiscal penalty for excess low-value activity;
- quality/safety penalty for inappropriate substitution.

## Model outputs

- equilibrium strategy profile;
- conditions for provider supply expansion;
- conditions for hospital rescue dominance;
- sensitivity to co-payment protections;
- sensitivity to PHO transaction costs;
- sensitivity to ACC activity funding.

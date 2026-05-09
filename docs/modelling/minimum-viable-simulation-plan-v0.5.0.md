# Minimum viable simulation plan v0.5.0

## Purpose

Build the smallest defensible simulation that can test the core policy question:

> Does a reweighted-capitation-only pathway improve distribution while leaving marginal supply constrained, compared with a demand-driven, rules-based contact benefits schedule?

## Phase 1: Structural model with synthetic parameters

Use synthetic parameters to test model logic only. No policy claims should be made from Phase 1 results.

### Scenarios

1. **Status quo tight control**: capitation plus programme funding, PHO-mediated access, constrained marginal public payment.
2. **Reweighted capitation only**: better distribution by need, no activity-sensitive contact benefit.
3. **Benefits schedule low**: modest public benefits for defined contact types, co-payment remains meaningful.
4. **Benefits schedule high**: higher public benefits, stronger supply response and fiscal risk.
5. **Benefits schedule + scope expansion**: eligible activity by GPs, NPs, pharmacists, nurses, allied health and paramedics within scope.
6. **Benefits schedule + equity protections**: lower co-payments for priority groups and higher public benefit for deprivation/rurality/complexity.
7. **ACC constraint shock**: reduced ACC activity payments, testing practice viability and non-injury capacity spillover.
8. **Ambulance alternatives**: funded hear-and-treat/treat-and-refer and safe alternative destination pathways.

## Phase 2: Calibration-ready model

Replace synthetic values with:

- population distribution;
- encounter rates;
- appointment wait measures;
- co-payment distributions;
- provider cost estimates;
- ED/ASH/ambulance metrics;
- ACC claim and revenue data;
- PHO cost/pass-through estimates.

## Phase 3: Decision model

Only proceed once the model can reproduce baseline patterns in:

- primary care access;
- ED presentations;
- ambulance conveyance;
- ambulatory-sensitive hospitalisations;
- practice viability proxy;
- equity gradients.

## Minimum outputs

For each scenario, report:

- total primary care contacts;
- contacts by provider type;
- unmet need;
- wait time proxy;
- co-payment burden;
- fiscal cost;
- low-value activity proxy;
- hospital pressure;
- ambulance conveyance;
- equity gap;
- provider viability.

## Decision rule

A contact benefits schedule should not be favoured unless it improves access and reduces unmet need without unacceptable equity harm, safety risk, low-value activity or fiscal exposure.

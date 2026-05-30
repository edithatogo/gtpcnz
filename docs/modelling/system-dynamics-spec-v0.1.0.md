---
title: "System dynamics specification"
version: "0.1.0"
status: "draft"
last_updated: "2026-05-07"
owner: "Dylan A Mordaunt"
next_review: "2026-05-21"
---


# System dynamics specification

## Purpose

Model the feedback loops by which primary care and ambulance constraints may increase hospital demand.

## Stocks

- enrolled population;
- unmet primary care need;
- appointment capacity;
- provider workforce FTE;
- provider burnout/exit risk;
- rural in-person capacity;
- telehealth capacity;
- ACC-funded episode volume;
- ambulance call volume;
- ambulance non-conveyance capacity;
- ED demand;
- hospital admissions;
- hospital budget pressure;
- primary care budget pressure.

## Flows

- new need generation;
- successful primary care contact;
- delayed primary care contact;
- unmet need to ED;
- ED to admission;
- hospital discharge to primary care follow-up;
- workforce entry;
- workforce exit;
- practice market entry;
- practice closure;
- ambulance conveyance;
- ambulance treat-and-refer;
- ACC-funded primary care contact.

## Feedback loops

### R1: Hospital rescue loop

Unmet primary care need -> ED demand -> hospital pressure -> hospital funding priority -> upstream funding remains constrained -> unmet need continues.

### B1: Primary care benefits loop

Primary care benefits -> marginal provider revenue -> supply expansion -> reduced unmet need -> lower ED demand.

### R2: Co-payment barrier loop

Higher co-payments -> reduced early access among price-sensitive patients -> delayed care -> ED/hospital demand -> system cost.

### B2: Multidisciplinary supply loop

Scope-based benefits -> broader provider participation -> more contacts -> reduced GP bottleneck -> better access.

### R3: ACC stabiliser loop

ACC FFS revenue -> practice viability -> non-injury primary care capacity -> reduced unmet need. If ACC FFS constrained, this loop reverses.

## Core equations: early sketch

- `PrimaryCareSupply(t) = f(workforce, marginal_payment, provider_mix, admin_burden, co_payment_revenue)`
- `UnmetNeed(t+1) = UnmetNeed(t) + NeedGenerated - SuccessfulPrimaryCareContacts - AmbulanceResolvedContacts`
- `EDDeman(t) = baseline_ED + alpha * UnmetNeed + beta * AmbulanceConveyance`
- `ProviderEntry = sigmoid(expected_margin - entry_threshold - admin_burden)`
- `ProviderExit = sigmoid(burnout + financial_stress - resilience)`

## Validation

- reproduce known utilisation patterns;
- test extreme assumptions;
- calibrate to available primary care access, ambulance and hospital demand data;
- stakeholder face validity.

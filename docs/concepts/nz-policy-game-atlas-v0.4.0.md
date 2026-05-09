---
title: "New Zealand primary care, ambulance and hospital funding: policy game atlas"
version: "0.4.0"
status: "technical map for policy modelling"
last_updated: "2026-05-07"
owner: "Dylan A Mordaunt"
track: "008-nz-game-theory-map"
---

# New Zealand primary care, ambulance and hospital funding: policy game atlas

## Purpose

This atlas maps the broader New Zealand policy problem as a set of interacting games. Earlier project versions contained a general repeated-game scaffold. This version explicitly maps the larger architecture problem: primary care funding, capitation, PHO intermediation, ambulance/prehospital care, ACC spillovers, Health NZ hospital pressure, professional scope constraints, co-payments, telehealth, equity, data and political economy.

This is a policy-modelling framework, not empirical proof. The aim is to make the hypothesised mechanisms explicit enough to test through simulation modelling, qualitative research and linked administrative data.

## One-sentence thesis

New Zealand may be tightly managing activity and expenditure in lower-cost upstream sectors - primary care, urgent care and ambulance/prehospital care - in ways that unintentionally channel unmet demand into the higher-cost, more visible hospital system.

## Core repeated-game claim

The problem is not one simple game. It is a nested repeated game with multiple principals, multiple agents, incomplete information, asymmetric political salience, weakly observed upstream failure and strong hospital-rescue incentives.

The key equilibrium risk is:

```text
Tight upstream control
+ weak marginal supply incentives
+ professional/provider entry barriers
+ high co-payment, waiting and travel costs
-> delayed or displaced care
-> visible ambulance, ED and hospital pressure
-> hospital rescue funding
-> continued upstream constraint
```

This can be described as **hospital-rescue dominance**.

## Public-policy anchors

The current capitation reweighting work is useful but narrow. The released Sapere briefing describes the work as a technical analysis to improve the capitation formula and says it has not considered fundamental changes to the overall funding model for primary care. The same briefing says the current capitation model was put in place in the early 2000s, was developed from use patterns at the time, and has been limited by relying mainly on age and sex variables.

The Health and Disability System Review recommended more flexible Tier 1 funding and contracting arrangements, including moving away from mandatory PHO contracting. More recent Ministry material on PHO finances records limited direct visibility over PHO financial activity, ownership structures and business models.

The National Primary Care Dataset and the new primary care access target create a better observability layer. That is valuable, but measurement does not by itself create supply unless the payment, workforce and scope architecture makes additional contacts viable.

Ambulance should be modelled as access infrastructure, not only transport. Ambulance commissioning and performance reporting sit at the interface of Health NZ, ACC, EDs and community alternatives.

## Actors

| Actor | Role in the game | Main incentive | Information problem |
|---|---|---|---|
| Ministers / Cabinet | Political principal | visible access, fiscal control, hospital stability | upstream failure is less visible than hospital failure |
| Treasury | fiscal/value principal | whole-of-Crown exposure and value for money | siloed cost shifts may be difficult to observe |
| Ministry of Health | steward, policy adviser, monitor | system settings, equity, performance | limited operational visibility without stronger datasets |
| Health NZ | commissioner and hospital operator | targets, deficits, hospital delivery, service commissioning | hospitals are direct and visible; upstream access failure is dispersed |
| ACC | injury funder and purchaser | injury cost, rehabilitation, scheme sustainability | ACC savings may affect broader primary care supply |
| PHOs/locality entities | intermediary and support layer | organisational survival, coordination, programmes | transaction costs and margins can be opaque |
| Primary/urgent care providers | supply agents | viability, workload, autonomy, clinical care | unmet need is visible locally but not always nationally |
| Pharmacists, NPs, allied health, Maori/Pacific providers | potential supply entrants | scope utilisation and access | funding may not follow legal or clinical scope |
| Ambulance/paramedics | prehospital access agents | response, safety, conveyance, workforce | alternatives may be underfunded or under-governed |
| Hospitals/ED | visible pressure domain | throughput, safety, targets, deficit control | demand appears unavoidable once it arrives |
| Patients/whanau | consumers and voters | access, price, continuity, trust, distance | uncertainty about best pathway |

## Core sequence

1. Government and Health NZ set budget architecture, funding rules and targets.
2. Health NZ allocates attention across hospitals, primary/community care, ambulance and other priorities.
3. Primary, urgent and ambulance providers decide whether to expand, maintain or ration supply.
4. Consumers decide whether to seek early care, delay, use telehealth, call ambulance or attend ED.
5. Unmet need resolves, worsens or appears as ambulance, ED or hospital demand.
6. Hospital pressure becomes visible and politically salient.
7. Government and Health NZ respond through hospital rescue, upstream reform or both.
8. The next period begins with changed baselines, provider viability and expectations.

## Component games

### G1. Hospital-salience budget game

Hospital pressure is more visible, more politically costly and more operationally direct than upstream access failure. The status quo equilibrium is recurrent hospital rescue. The policy lever is hospital-equivalent accountability for primary care and ambulance plus a mechanism that allows upstream supply to expand.

### G2. Health NZ internal allocation game

Health NZ both operates hospitals and commissions primary/community care. When hospitals are under visible pressure, operational risk may dominate upstream investment. The policy lever is to alter salience, accountability and funding rules so primary care and ambulance outcomes cannot remain residual.

### G3. Capitation marginal-supply game

Capitation supports continuity and population responsibility, but under dominant capitation an additional clinically necessary contact may have positive marginal cost and weak marginal public revenue. Reweighting improves distribution but may not create supply. The policy lever is a blended model with contact-type benefits.

### G4. Consumer access pathway game

Patients choose between early primary care, delay, telehealth, ambulance and ED based on co-payment, waiting time, distance, trust, continuity and perceived urgency. The policy lever is co-payment calibration plus supply expansion and patient pathway design.

### G5. PHO intermediation game

PHOs may provide useful equity, data, quality and locality functions, but mandatory payment intermediation may add friction, opacity and entry barriers. The policy lever is to separate PHO functions from payment-gateway functions.

### G6. ACC/Health NZ cross-funder game

ACC activity funding may stabilise general practice capacity. A saving inside ACC could increase Health NZ or hospital pressure if it reduces general primary care supply. The policy lever is whole-of-Crown modelling of ACC, primary care, ambulance and hospital effects.

### G7. Ambulance conveyance game

If ED conveyance is the safest funded and legally defensible pathway, conveyance becomes the default even where alternatives may be safe and lower cost. The policy lever is funded hear-and-treat, treat-and-refer, alternative destination and community follow-up pathways.

### G8. Scope-of-practice supply game

Funding eligibility can be narrower than legal or clinical scope, creating professional bottlenecks. The policy lever is claimability by contact type, scope, credentialing and clinical governance rather than professional category alone.

### G9. Telehealth/local-supply game

Telehealth can extend access, but if it captures low-complexity work while local providers retain complex in-person work, local viability can erode. The policy lever is integration, continuity requirements and rural/in-person loadings.

### G10. Co-payment calibration game

Co-payments can signal demand, but can also deter necessary care and worsen equity. The policy lever is a calibrated co-payment regime with concessions, caps, essential-service protections and monitoring of unmet need.

### G11. KPI salience game

What is measured at the top tier gets managed. A narrow access target can create metric management without true capacity improvement. The policy lever is a balanced scorecard: access, continuity, fees, equity, ambulance disposition, avoidable hospitalisations and patient-reported unmet need.

### G12. Equity and trust game

Direct contact benefits can expand average access but may reward easy volume unless equity and trust are built into the design. The policy lever is equity-weighted benefits plus explicit funding for kaupapa Maori, Pacific, rural and outreach functions.

### G13. Political economy game

The same reform can be framed as pro-market, pro-patient, anti-PHO, anti-GP or anti-equity. The policy lever is a non-partisan system-design narrative focused on access, safety, equity, supply and hospital avoidance.

### G14. Data observability game

Unmeasured upstream failure remains less fundable than measured hospital pressure. The policy lever is linked data across primary care, ambulance, ED, admissions, co-payments, enrolment, patient-reported access and equity groups.

## Normal-form simplification

| Funder architecture | Provider rations | Provider maintains | Provider expands |
|---|---|---|---|
| Tight capitation / contract control | Short-term fiscal control; long-term hospital pressure | Provider absorbs cost; burnout risk | Provider loses unless cross-subsidised |
| Reweighted capitation only | Distribution improves but marginal supply remains weak | Better allocation, access may remain constrained | Expansion depends on workforce and co-payments |
| Contact benefits plus capitation | Rationing less attractive if benefits exceed marginal cost | Stable access more likely | Expansion rational where benefit plus co-payment exceeds cost and risk |

## Formal skeleton

Let:

```text
D_t = underlying primary, urgent and prehospital demand in period t
Q_t = accessible lower-cost contacts supplied
U_t = max(0, D_t - Q_t) = unmet or delayed need
H_t = hospital pressure
A_t = ambulance conveyance pressure
B_j = public benefit for eligible contact type j
p_j = patient co-payment for contact type j
c_ij = marginal cost to provider i of delivering contact j
g_ij = governance and scope eligibility indicator
r_i = risk, liability and administration cost for provider i
```

Provider i supplies contact type j where:

```text
B_j + p_j + v_ij - c_ij - r_i > 0 and g_ij = 1
```

Hospital pressure evolves as:

```text
H_(t+1) = rho * H_t + alpha * U_t + beta * A_t - gamma * V_t
```

where V_t is effective upstream hospital avoidance.

## What would falsify the hypothesis?

The central hypothesis should be weakened if:

1. reweighted capitation alone materially improves waits, open books, rural in-person access and co-payment burden;
2. contact benefits do not generate supply where provider capacity exists;
3. broader provider eligibility does not increase supply or creates unacceptable safety problems;
4. PHO intermediation demonstrably reduces transaction costs and improves market entry compared with direct/optional claiming;
5. ambulance alternative pathways do not safely reduce ED conveyance;
6. top-tier primary and ambulance KPIs do not change organisational focus or resource allocation;
7. co-payment settings cannot be made compatible with equity.

## Policy interpretation

Capitation reweighting may improve who gets the existing primary care funding, but it does not necessarily change the game that determines whether lower-cost primary, urgent and ambulance care can expand fast enough to prevent hospital growth.

The policy intervention is a change in the rules of the game: define eligible lower-cost contacts; allow accredited providers within scope to deliver them; fund them through a transparent patient-linked claims platform; calibrate co-payments with equity safeguards; and hold primary care and ambulance to hospital-equivalent accountability.

---
title: "Agent-based model specification"
version: "0.1.0"
status: "draft"
last_updated: "2026-05-07"
owner: "Dylan A Mordaunt"
next_review: "2026-05-21"
---


# Agent-based model specification

## Purpose

Model heterogeneous patients, providers and local markets under alternative funding architectures.

## Patient agents

Attributes:

- age;
- sex;
- ethnicity;
- deprivation;
- rurality;
- disability;
- multimorbidity;
- enrolment status;
- income/price sensitivity;
- transport access;
- digital access;
- probability of urgent/routine/preventive/chronic care need;
- probability of injury/ACC-related need.

Decisions:

- seek primary care;
- delay;
- use telehealth;
- use pharmacy/NP/physio/paramedic;
- call ambulance;
- attend ED;
- abandon care.

## Provider agents

Types:

- GP practice;
- nurse practitioner provider;
- pharmacy;
- physiotherapy/allied health;
- kaupapa Māori provider;
- Pacific provider;
- telehealth provider;
- ambulance provider;
- urgent care clinic.

Attributes:

- workforce FTE;
- scope/activity eligibility;
- location/rurality;
- capitation revenue;
- benefit revenue;
- ACC revenue;
- co-payment policy;
- admin burden;
- clinical governance maturity;
- market entry/exit thresholds;
- appointment capacity;
- willingness to enrol new patients.

Decisions:

- enter market;
- expand services;
- reduce services;
- open/close books;
- alter co-payments;
- hire provider types;
- provide in-person or telehealth contacts;
- invest in after-hours care.

## Funder agents

- Health NZ;
- Ministry/Treasury payment architecture;
- ACC;
- PHO/locality intermediary;
- Australian Commonwealth/state extension.

Decisions:

- set capitation weight;
- set benefit values;
- set co-payment protections;
- allow provider type eligibility;
- require PHO mediation;
- fund ambulance alternative pathways;
- prioritise hospital rescue.

## Scenarios

Use `scenario-library-v0.1.0.md`.

## Outputs

- contacts by provider type;
- unmet need;
- co-payment burden;
- ED/ambulance use;
- market entry and exit;
- equity outcomes;
- fiscal cost.

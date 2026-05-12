# Streamlit dashboard content and presentation contract v1.8.1

## Purpose

The Streamlit dashboard must be readable by a general audience while remaining safe for policy, research and public communication. It is an explainer for a source-informed model scaffold, not a calibrated simulator.

## Audience

The primary audience is an interested public reader, journalist, policy stakeholder, clinician, public servant or reviewer who has not read the full project.

The dashboard should not assume that the reader already understands capitation, fee-for-service, PHOs, NPCD, OIA, calibration or model indices.

## Required first-screen content

The first screen must contain:

- A plain-English title identifying the dashboard as a funding architecture explainer.
- The full model caveat:

> This is a source-informed parameterised scaffold and educational explainer. It is not a real-data calibrated forecast and should not be used to claim precise fiscal savings, hospital-demand reductions, workforce effects, or implementation impacts.

- A short reader guide explaining the difference between reference scenarios and toy slider settings.
- Clear direction on how to read the dashboard.

## Required sections

The dashboard must include these sections or tabs:

- Start here: thesis, claim boundary, model status and interpretation rules.
- Current state: current New Zealand reform pathway, public project status, static table and static diagram.
- Reference scenarios: precomputed model-generated indices and dynamic charts.
- Toy explainer: educational sliders and dynamic toy-output chart.
- Evidence and OIA: public evidence tracker table.
- Calibration readiness: table of data required before real calibration.
- Glossary: plain-English definitions of core terms.

## Required current-state information

The current-state section must explain that the current reform pathway is the comparator, not a straw man. It must cover:

- capitation reweighting;
- primary care access target;
- National Primary Care Dataset;
- digital access and telehealth;
- urgent and after-hours care;
- PHO accountability and commissioning.

## Required visual and tabular material

The dashboard must include both static and dynamic explanatory material:

- Static tables:
  - current reform pathway table;
  - public project status table;
  - evidence/OIA tracker table;
  - calibration-readiness table.
- Static diagram:
  - public explainer architecture diagram showing current reform pathway, tested gap, scaffold, toy explainer, evidence tracker and calibration readiness.
- Dynamic figures:
  - reference scenario viability chart;
  - reference scenario supply-generation versus hospital-pressure scatter plot;
  - scenario score heatmap;
  - selected scenario radar/profile chart;
  - toy explainer output chart;
  - project readiness chart.

## Wording constraints

The dashboard must:

- use "explainer", "source-informed scaffold", "reference scenario", "toy explainer" and "model-generated index";
- describe outputs as model-generated indices, not observed New Zealand outcomes;
- state that F0/current reform is the comparator;
- state that toy sliders do not rerun the full parameterised model;
- state that index differences must not be converted into dollars saved, beds avoided, workforce numbers, ED reductions or implementation impacts.

The dashboard must not:

- describe itself as a calibrated simulator;
- describe slider output as a forecast;
- imply precise fiscal savings, hospital-demand reductions, workforce effects or implementation impacts;
- imply government endorsement.

## Deployment contract

The dashboard must be deployable from Streamlit Community Cloud using:

- repository: `edithatogo/gtpcnz`;
- branch: `main`;
- entrypoint: `streamlit_app.py`.

The public URL is:

<https://gtpcnz.streamlit.app/>

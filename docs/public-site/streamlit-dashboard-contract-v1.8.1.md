# Streamlit dashboard content and presentation contract v1.8.1

## Purpose

The Streamlit dashboard must be readable by a general audience and safe for policy, research and public communication. It is an explainer for a source-informed model scaffold, not a calibrated simulator.

## Audience

The primary audience is an interested public reader, journalist, policy stakeholder, clinician, public servant or reviewer who has not read the full project.

The dashboard should not assume that the reader already understands capitation, fee-for-service, PHOs, NPCD, OIA, calibration or model indices.

## Required first-screen content

The first screen needs:

- A plain-English title identifying the dashboard as a funding architecture explainer.
- The full model caveat:

> This is a source-informed parameterised scaffold and educational explainer. It is not a real-data calibrated forecast and should not be used to claim precise fiscal savings, hospital-demand reductions, workforce effects, or implementation impacts.

- A short reader guide explaining the difference between reference scenarios and toy slider settings.
- A short guide to reading the dashboard.

## Required sections

The dashboard needs these sections or tabs:

- Start here: thesis, claim boundary, model status and interpretation rules.
- Post guide / reading map: each public post mapped to the corresponding Quarto section, Streamlit module, GitHub Pages card, static visual and dynamic visual.
- Current state: current New Zealand reform pathway, public project status, static table and static diagram.
- Reference scenarios: precomputed model-generated indices and dynamic charts.
- Microeconomics lab: marginal supply, capitation budget constraint, scheduled activity payment and co-payment barrier modules.
- Game theory lab: formulas-do-not-solve-games module, payoff/best-response explanation, controls/gaming-risk module and guided toy incentive simulation.
- Toy explainer: educational sliders and dynamic toy-output chart.
- Toy parameter dictionary: plain-English definitions for every slider, including what 0, 100 and a high value mean.
- Evidence and OIA: public evidence tracker table.
- Calibration readiness: table of data required before real calibration.
- Glossary: plain-English definitions of core terms.

## Required current-state information

The current-state section must explain that the current reform pathway is the comparator, not a straw man. It should cover:

- capitation reweighting;
- primary care access target;
- National Primary Care Dataset;
- digital access and telehealth;
- urgent and after-hours care;
- PHO accountability and commissioning.

## Required visual and tabular material

The dashboard must mix static and dynamic material:

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
  - marginal supply simulation;
  - co-payment/access barrier simulation;
  - game-theory payoff or best-response simulation;
  - gaming-risk frontier or controls-stack simulation.

## Post-to-dashboard crosswalk

The dashboard must implement the public reading map defined in:

- `docs/public-site/post-surface-crosswalk-contract-v1.8.2.md`

Minimum mappings:

| Post | Streamlit destination | Required dynamic component |
|---|---|---|
| 01 upstream rationing and hospital growth | Start here; Current state; Reference scenarios | Supply versus hospital-pressure plot |
| 02 FFS/capitation/blended funding | Funding models or Toy explainer | Funding comparison toy module |
| 03 marginal supply | Microeconomics lab | Marginal supply simulation |
| 04 formulas do not solve games | Game theory lab | Toy incentive game or best-response simulation |
| 05 current reform pathway | Current state; Reference scenarios | F0/current reform comparator selector |
| 06 uncapping primary care funding | Toy explainer; Microeconomics lab | Activity/payment/control simulation |

Later game-theory posts and appendices that are referenced by the public surfaces must have a corresponding dashboard module or guided explainer. They must not remain only as off-dashboard background.

## Wording constraints

The dashboard must:

- use "explainer", "source-informed scaffold", "reference scenario", "toy explainer" and "model-generated index";
- describe outputs as model-generated indices, not observed New Zealand outcomes;
- state that F0/current reform is the comparator;
- state that toy sliders do not rerun the full parameterised model;
- state that toy sliders are qualitative teaching levers, not estimated structural parameters;
- define the toy scale as 0 = absent/weak and 100 = strong/reliably implemented;
- use public slider labels that explain the policy lever rather than exposing only internal implementation names;
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

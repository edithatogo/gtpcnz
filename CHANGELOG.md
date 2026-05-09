# Changelog

## v1.2.1

- Added systematic contract-compliance audit and acceptance-criteria matrix.
- Updated README and Conductor tracks to current package state.
- Repaired local Markdown figure links and confirmed zero local-link errors.
- Added Substack v1.2.1 QA checklist.
- Initialised git history in packaged release.


## v1.0.0 — parameterised model run

- Added source-informed parameter input register.
- Added parameterised scenario set P0-P8.
- Reran deterministic game and hybrid models.
- Added uncertainty stress test and hybrid-informed MCDA.
- Added workbook, report, plots and tables.
- Added conductor track 015.

# Changelog

## v0.5.0 — Empirical validation readiness

- Added Track 010: Empirical validation readiness.
- Added research audit dossier and audit index v0.5.0.
- Added claim-to-source ledger and source registry.
- Added research quality gates and artefact lineage graph.
- Added model parameter inventory and minimum viable simulation plan.
- Added STRESS, ODD and PRISMA-ScR crosswalks.
- Added stakeholder validation pack and sampling frame.
- Added OIA/data request dashboard.
- Added audit integrity tests.
- Updated repo index, source notes and version metadata.


## v0.4.1 — Research audit and traceability pack

- Added Track 009: Research audit and traceability.
- Added audit index and artefact manifest.
- Added game-map traceability matrix linking each mapped game to evidence status, assumptions, artefacts and falsification risks.
- Added claim-evidence-assumption register.
- Added decision log, source-quality/search log, reproducibility checklist, falsification register and stakeholder validation plan.
- Updated repo index and source notes.

## v0.4.0 - 2026-05-07

### Added

- Explicit New Zealand policy-game atlas mapping 14 component games across primary care, ambulance, Health NZ, PHOs, ACC, professional scope, co-payments, KPIs, telehealth, equity and data observability.
- Formal game-theory model specification with players, strategies, payoff variables, equilibria, scenarios and falsification tests.
- Policy brief 06: The New Zealand primary care and ambulance funding game.
- NZMJ methods annex for presenting the game-theory mapping in Viewpoint or Original Article form.
- Substack post 09 translating the NZ policy game for a public audience.
- Python `nz_game_map.py` representation and tests.
- Standalone DOCX and PDF outputs for the NZ policy game map.
- Conductor Track 008 for game-theory mapping.

### Changed

- Clarified that v0.3.0 contained a core payoff scaffold, while v0.4.0 maps the broader NZ policy game explicitly.
- Clarified that the proposal is demand-driven within rules, not a fixed primary care ring-fence.
- Clarified the distinction between capitation reweighting as allocation reform and contact benefits as supply architecture.
- Strengthened the distinction between clinical safety constraints and funding-model professional constraints.

### Verified

- Python tests pass: 18 passed.
- Policy brief 06 DOCX rendered to page images and visually checked.
- Policy brief 06 PDF rendered to page images and visually checked.

## v0.3.0 - 2026-05-07

### Added

- Near-submission NZMJ Viewpoint draft with structured abstract.
- Expanded RACMA-ready policy brief on the National Primary Care Benefits Schedule.
- v0.2.0 drafts of briefs on PHO intermediation, ambulance/prehospital care, Australia and KPIs.
- Public-facing Substack plan and draft set through provider-scope, co-payment and ambulance themes.
- Formal repeated-game payoff model and causal logic model.
- OIA addendum targeting operational capitation formula, PHO advice and ambulance substitution advice.
- Evidence review protocol with mechanism and parameter extraction fields.
- Word and PDF versions of the main policy brief under `outputs/`.

### Changed

- Reframed the architecture from a fixed ring-fenced pool to a demand-driven benefits schedule constrained at transaction level.
- Updated Conductor tracks to include v0.3.0 release and public-facing translation workflow.
- Expanded Python model scaffold and tests.

### Verified

- Python tests pass.
- Main policy brief DOCX rendered and visually checked through generated page images.

## v0.1.0 - 2026-05-07

Initial scaffold and first working drafts.

## v0.6.0 - Demonstrative modelling layer

- Added executable demonstrative models for all 14 mapped New Zealand policy games.
- Added five scenario archetypes: status quo tight control, capitation reweighting only, Primary Care Benefits Schedule, full upstream access architecture, and loose benefits with weak controls.
- Added per-game equilibrium labels, welfare scores, hospital pressure scores, gaming risk scores and sensitivity outputs.
- Added charts: `demonstrative-game-summary-v0.6.0.png` and `demonstrative-hospital-pressure-by-game-v0.6.0.png`.
- Added `demonstrative-model-audit-matrix-v0.6.0.csv` linking each game to its model function, key lever, outputs and validation steps.
- Added tests for model coverage, bounded outputs and scenario directionality.

Important caveat: these are demonstrative models only. They are not empirical estimates and are not calibrated to administrative datasets.

## v0.7.0 — Empirical calibration readiness

- Added uncertainty and sensitivity module.
- Added parameter prior/evidence register.
- Added Monte Carlo stress-test outputs.
- Added calibration protocol and uncertainty report.
- Added validation backlog and evidence-priority register.
- Added policy brief on empirical tests needed before policy reliance.
- Added Conductor track 012.

## v0.8.0 - Final hybrid synthesis

- Added final hybrid model integrating the 14 mapped NZ policy games.
- Added hybrid deterministic and uncertainty outputs.
- Added final comprehensive report, executive brief and artefact index.
- Added Conductor track 013.
- Status remains demonstrative/non-calibrated.

## v0.9.0 - Game-informed MCDA decision support

- Added a game-informed MCDA layer with diagnostic game-position scoring, policy-option scoring, stakeholder weight sensitivity and risk-adjusted rankings.
- Added MCDA report, brief, rubrics, workshop guide, templates and workbook.
- Added executable `mcda.py` model and tests.
- Status remains demonstrative/non-calibrated.

## v1.1.0 - Pragmatic validation without full calibration (2026-05-08)

- Added validation and translation report artefacts.
- Added stakeholder game-validation and MCDA workshop pack.
- Added evidence threshold matrix and priority empirical checks.
- Added OIA/data request pack.
- Added rapid scoping review protocol and screening templates.
- Added prospective pilot/evaluation plan.
- Added validation workbook and figures.
- Did not attempt a fully empirically calibrated predictive model.


## v1.2.0 - Substack-ready publication pack
- Expanded Substack posts into humanised, hyperlinked, plain-English drafts.
- Added dedicated Substack conceptual diagrams, figure placement guide and alt text.
- Added source bank, glossary, voice guide and publication QA checklist.
- Preserved caveat that the model is source-informed and demonstrative, not fully calibrated.


## v1.3.1 — Uncapped FFS entitlement clarification

- Clarified that the proposal removes global caps on eligible primary medical activity.
- Added ACC-style FFS medical stream language and controls.
- Added G19, brief 13, post 15, MCDA update, OIA addendum and revised model outputs.

## v1.4.0 — Source-read catalogue, email-trail incorporation and expanded Substack series

- Added a source-read catalogue separating public/read documents, withheld advice, internal/private documents and unverified email intelligence.
- Incorporated RACMA email-trail insights into the background, analysis and discussion.
- Revised the central thesis to distinguish separate appropriations/current reform from the continuing strategic allocation game.
- Added current-reform comparator material covering capitation reweighting, access target, National Primary Care Dataset, digital access, urgent/after-hours care and PHO accountability.
- Added revised game-map material, including place-based accountability/cherry-picking, current reform sufficiency, formula-fixation, urgent-care policy and uncapped entitlement/fiscal-governance games.
- Expanded the Substack publication layer into an 18-post series covering individual games, the hybrid game, composite modelling, MCDA and recommendations.
- Added explanatory microeconomic and conceptual diagrams for marginal supply, fixed-envelope rationing, co-payment/equity, place accountability, model stack and hybrid architecture.
- Preserved the caveat that the model remains demonstrative/source-informed rather than fully empirically calibrated or predictive.



## v1.5.1 - Short-form Substack public series

- Split the v1.5.0 long Substack drafts into shorter public posts and optional deep-dive appendices.
- Preserved all long drafts as backup material.
- Added a short-form publication strategy for twice-weekly rollout.
- Added QA checklist and local link audit for the short posts and appendices.

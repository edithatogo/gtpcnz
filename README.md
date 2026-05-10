# Primary care funding architecture project

**Current release: v1.7.0 — full parameterised model scaffold.**

This repository contains a policy-research package on New Zealand and Australia primary care funding architecture. The current release continues the calibrated-model pathway. It adds a full parameterisation scaffold with explicit parameters, bounds, scenario values, data-input contracts, monthly dynamics, sensitivity analysis and plots. The model is still not empirically calibrated or predictive until real data replace the priors and validation is completed.


## v1.7.0 modelling front-door files

- `docs/calibration/full-parameterised-model-build-report-v1.7.0.md`
- `docs/calibration/parameterisation-data-contract-v1.7.0.md`
- `docs/calibration/real-data-update-pathway-v1.7.0.md`
- `outputs/full-parameterised-dashboard-table-v1.7.0.csv`
- `outputs/full-parameter-register-v1.7.0.csv`
- `outputs/full-parameterised-summary-results-v1.7.0.csv`
- `outputs/figures/full-parameterised-scenario-viability-pressure-v1.7.0.png`

## Current front-door files

- `docs/substack-ready/post-00-series-landing-page-v1.6.0.md`
- `docs/substack-ready/complete-substack-series-v1.6.0.md`
- `docs/substack-ready/common-objections-and-responses-v1.6.0.md`
- `docs/substack-ready/equity-review-brief-v1.6.0.md`
- `docs/substack-ready/publication-calendar-twice-weekly-with-pause-v1.6.0.md`
- `docs/substack-ready/one-page-visual-summary-v1.6.0.md`
- `docs/substack-ready/oia-launch-pack-v1.6.0.md`


---

# Primary Care Funding Architecture: Australia and Aotearoa New Zealand

Version: **v1.5.0**

This repository contains a research-to-policy programme on primary care funding architecture, with a focus on Aotearoa New Zealand and Australia.

## Core hypothesis

Current reform in New Zealand is focused on improving allocation within capitation. That is necessary but may be insufficient. The larger system question is whether tightly controlled lower-cost primary, urgent and ambulance/prehospital activity channels demand growth into higher-cost hospital care.

The repository develops this as a structured, falsifiable policy hypothesis. It is **not** a fully empirically calibrated predictive model.

## Proposed policy architecture

The repo develops the case for a **National Primary Care Benefits Schedule**:

- public benefits for defined primary, urgent and ambulance/prehospital contact types;
- provider eligibility based on accreditation, scope of practice and clinical governance;
- co-payment settings used as a calibrated demand signal, with equity protections;
- capitation retained for continuity, baseline viability, enrolment and population accountability;
- Primary Health Organisation/locality functions separated from mandatory payment-gateway functions;
- primary care and ambulance outcomes lifted to hospital-equivalent top-tier accountability.

The short version is:

> Demand-driven within rules; not demand-driven without rules.

## What the package contains

```text
conductor/              Conductor-style project context, tracks, specs and plans
docs/concepts/          Core thesis, causal logic and architecture options
docs/modelling/         Game maps, demonstrative models, uncertainty analysis and source-informed parameterised model outputs
docs/mcda/              Game-informed Multi-Criteria Decision Analysis framework and workshop tools
docs/policy-briefs/     Policy briefs and index
docs/substack-ready/    Expanded Substack-ready posts, figures, source bank, glossary and publication QA
docs/nzmj/              New Zealand Medical Journal Viewpoint and article/protocol material
docs/review/            Rapid scoping review protocol and extraction/screening material
docs/oia/               Official Information Act request drafts and trackers
docs/audit/             Claim-source ledger, traceability, research audit and v1.2.1 contract-compliance audit
models/                 Lightweight Python model scaffold and tests
outputs/                Generated public-facing reports, workbooks, plots and standalone artefacts
```

## Current release

This is **v1.4.0**, the source-read catalogue, email-trail incorporation and expanded Substack/modelling explanation release.

It incorporates the document classes and policy insights raised in the RACMA email trail, including separate Vote Health appropriations, the current primary care reform pathway, Primary Health Organisation transparency and pass-through issues, urgent and after-hours care, Accident Compensation Corporation payment architecture, Population-Based Funding Formula transparency debates, and the distinction between an uncapped eligible medical fee-for-service stream and an uncontrolled market model.

The release adds a source-read catalogue, an incorporation report, a revised hybrid thesis, a current-reform comparator, a game-map update, new explanatory microeconomic diagrams, and an expanded 18-post Substack series covering the individual games, hybrid game, composite modelling, Multi-Criteria Decision Analysis and recommendations.

Earlier v1.2.1 contract-compliance checks remain in the package and verify that:

- background and theory are laid out;
- the broader New Zealand policy game is mapped;
- each game has demonstrative modelling;
- uncertainty, hybrid synthesis, source-informed parameterised modelling and MCDA layers are present;
- policy briefs, reports, New Zealand Medical Journal material and validation plans are present;
- the Substack series has expanded human-readable, hyperlinked posts with figures, glossary and source bank;
- local Markdown links and figure references pass automated checks;
- README, Conductor track index and versioning metadata are updated;
- the package now includes git history in the v1.2.1 zip.


Key v1.4.0 outputs:

- `docs/source-notes/source-read-catalogue-v1.4.0.csv`
- `docs/source-notes/source-read-catalogue-v1.4.0.md`
- `docs/analysis/document-incorporation-report-v1.4.0.md`
- `docs/concepts/revised-hybrid-thesis-v1.4.0.md`
- `docs/concepts/current-reform-comparator-v1.4.0.md`
- `docs/modelling/game-map-update-v1.4.0.md`
- `docs/substack-ready/complete-substack-series-v1.4.0.md`
- `docs/substack-ready/posts-v1.4.0/`
- `docs/substack-ready/figures/fig-08-*` through `fig-14-*`

Key v1.2.1 audit outputs:

- `docs/audit/contract-compliance-audit-v1.2.1.md`
- `docs/audit/acceptance-criteria-matrix-v1.2.1.csv`
- `docs/audit/substack-post-qa-checklist-v1.2.1.csv`
- `docs/audit/local-link-audit-v1.2.1.csv`
- `docs/audit/remediation-log-v1.2.1.md`

## Substack-ready publication layer

The expanded v1.4.0 publication-ready draft series is in:

```text
docs/substack-ready/posts-v1.4.0/
docs/substack-ready/figures/
docs/substack-ready/complete-substack-series-v1.4.0.md
docs/substack-ready/figure-placement-and-alt-text-v1.4.0.md
docs/substack-ready/substack-post-qa-checklist-v1.4.0.csv
```

Earlier v1.2.x drafts and source-bank/glossary material remain available for comparison.

The posts are **Substack-ready drafts**, not final Dylan-signed-off copy. They still need final judgement on political sharpness, voice, Te Tiriti/Māori and Pacific nuance, and stakeholder risk.

## Testing

```bash
pytest -q
```

The v1.4.0 release passes the model test suite; earlier v1.2.1 local-link audit remains in the package, with v1.4.0 source and Substack files added subsequently.

## Status and caveat

This repo is a working policy and research package, not a final endorsed RACMA/RACGP/RNZCGP/ACRRM/GPNZ position.

The modelling is demonstrative and source-informed. It can support stakeholder discussion, Substack publication, RACMA scoping, policy brief development and a New Zealand Medical Journal Viewpoint/protocol pathway. It should not be used to claim precise forecast effects without future empirical calibration and validation.


## Current release: v1.3.1

This release clarifies that the preferred architecture is **capitation + uncapped primary medical fee-for-service + place-based population accountability**. The cap is removed at the global eligible-activity level, while item prices, service definitions, clinical eligibility, provider scope, audit, co-payment protections and place-based obligations remain as safeguards.


## Current release: v1.5.0

This release adds three major items:

1. **Comprehensive Substack hyperlinking and expansion.** The Substack series now has 18 expanded posts in `docs/substack-ready/posts-v1.5.0/`, each with figure placement and a larger public source list. The QA checklist shows all posts exceed 1,200 words and include at least 10 external links.
2. **Twice-weekly publication plan.** The publication calendar starts Tuesday 12 May 2026 and runs on Tuesdays and Fridays for nine weeks.
3. **Calibrated-model starter.** The repo now contains a working calibration starter in `models/primarycare_model/calibration_v150.py`. It uses synthetic data to exercise the pipeline and produces observed-versus-predicted plots, parameter recovery outputs and a calibration build plan. This is not an empirically calibrated predictive model yet.

Key v1.5.0 artefacts:

- `docs/substack-ready/posts-v1.5.0/`
- `docs/substack-ready/complete-substack-series-v1.5.0.md`
- `docs/substack-ready/publication-calendar-twice-weekly-v1.5.0.md`
- `docs/substack-ready/substack-post-qa-checklist-v1.5.0.csv`
- `docs/substack-ready/figures/fig-15-*` through `fig-25-*`
- `models/primarycare_model/calibration_v150.py`
- `docs/calibration/calibration-starter-report-v1.5.0.md`
- `outputs/calibration-parameter-estimates-v1.5.0.csv`
- `outputs/calibration-observed-vs-predicted-primary-v1.5.0.png`
- `outputs/calibration-observed-vs-predicted-ed-v1.5.0.png`
- `outputs/calibration-observed-vs-predicted-cost-v1.5.0.png`

### Voice note

A public web search did not confidently identify Dylan's Substack publication URL. The v1.5.0 posts are therefore drafted against the voice evident in the email trail and project instructions, and still need final author sign-off.


## v1.5.1 short-form Substack update

The Substack series now has a short-form public version plus optional appendices. Public posts are generally 850-1,050 words, retain figures and key source links, and preserve the longer v1.5.0 material as deep-dive appendices and backup drafts.

Key files:

- `docs/substack-ready/posts-v1.5.1-public/`
- `docs/substack-ready/appendices-v1.5.1/`
- `docs/substack-ready/complete-substack-series-v1.5.1.md`
- `docs/substack-ready/complete-substack-appendices-v1.5.1.md`
- `docs/substack-ready/short-form-publication-strategy-v1.5.1.md`


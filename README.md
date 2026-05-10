# Primary care funding architecture project

**Current release: v1.7.1 — model hardening and launch simplification.**

This repository contains a policy-research and public-translation package on primary care funding architecture in Aotearoa New Zealand and Australia.

The current release hardens the v1.7.0 full parameterised scaffold and simplifies the publication pathway. It adds parameter tiering, an identifiability map, model card, figure-caption audit, source-confidence labels, red-team and devil's advocate reviews, a stakeholder validation survey, first-six-post launch copies, and a RACMA-excluded engagement pathway.

## Current policy thesis

Capitation should be retained for continuity, enrolment, baseline viability and population responsibility. Eligible primary medical activity should also have an uncapped, scheduled, rules-based fee-for-service stream, controlled through item rules, provider scope, clinical governance, documentation, audit, co-payment protections and place-based accountability.

Short version:

> Uncapped does not mean uncontrolled.

## Current publication pathway

Use only the front-door materials first:

1. `docs/substack-ready/post-00-series-landing-page-v1.6.0.md`
2. `docs/substack-ready/posts-v1.7.1-launch/`
3. `docs/launch/decision-maker-summary-v1.7.1.md`
4. `docs/substack-ready/common-objections-and-responses-v1.6.0.md`
5. `docs/calibration/model-card-v1.7.1.md`

The first six posts are the only public posts prepared for immediate launch-level review. The back half of the series should be revised after feedback.

## Current model status

The model is a **full parameterised scaffold**, not an empirically calibrated predictive model. It should not be used to claim precise fiscal savings, hospital-demand reductions or workforce effects.

Key model-hardening files:

- `docs/calibration/parameter-tiering-v1.7.1.csv`
- `docs/calibration/parameter-identifiability-map-v1.7.1.csv`
- `docs/calibration/model-card-v1.7.1.md`
- `docs/audit/red-team-review-v1.7.1.md`
- `docs/audit/devils-advocate-review-v1.7.1.md`
- `docs/audit/what-would-change-my-mind-v1.7.1.md`

## RACMA status

RACMA is excluded from proactive outreach in this release. If RACMA comes back interested, provide the decision-maker summary and model card, not the full repository.

## Testing

```bash
pytest -q
```

## Caveat

This is a structured, source-informed, falsifiable policy hypothesis and launch package. It is not an endorsed policy position and not a real-data calibrated forecasting model.

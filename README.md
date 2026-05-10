# Primary care funding architecture project

**Current release: v1.7.2 — model hardening and launch simplification.**

This repository contains a policy-research and public-translation package on primary care funding architecture in Aotearoa New Zealand and Australia.

The current release incorporates the red-team and devil's advocate critiques into the live launch materials. It updates the public thesis, model card, decision-maker summary, first-six Substack posts, claim-boundary rules, common objections, Conductor guidance and action register.

## Current policy thesis

Capitation should be retained for continuity, enrolment, baseline viability and population responsibility. Eligible primary medical activity should also have an uncapped, scheduled, rules-based fee-for-service stream, controlled through item rules, provider scope, clinical governance, documentation, audit, co-payment protections and place-based accountability.

Short version:

> Uncapped does not mean uncontrolled.

## Current publication pathway

Use v1.7.2 launch files. The red-team checks are now embedded in each first-six post.

Use only the front-door materials first:

1. `docs/substack-ready/post-00-series-landing-page-v1.6.0.md`
2. `docs/substack-ready/posts-v1.7.2-launch/`
3. `docs/launch/decision-maker-summary-v1.7.2.md`
4. `docs/substack-ready/common-objections-and-responses-v1.6.0.md`
5. `docs/calibration/model-card-v1.7.2.md`

The first six posts are the only public posts prepared for immediate launch-level review. The back half of the series should be revised after feedback.

## Current model status

The model is a **full parameterised scaffold**, not an empirically calibrated predictive model. It should not be used to claim precise fiscal savings, hospital-demand reductions or workforce effects.

Key model-hardening files:

- `docs/calibration/parameter-tiering-v1.7.2.csv`
- `docs/calibration/parameter-identifiability-map-v1.7.2.csv`
- `docs/calibration/model-card-v1.7.2.md`
- `docs/audit/red-team-review-v1.7.2.md`
- `docs/audit/devils-advocate-review-v1.7.2.md`
- `docs/audit/what-would-change-my-mind-v1.7.2.md`

## RACMA status

RACMA is excluded from proactive outreach in this release. If RACMA comes back interested, provide the decision-maker summary and model card, not the full repository.

## Testing

```bash
pytest -q
```

## Caveat

This is a structured, source-informed, falsifiable policy hypothesis and launch package. It is not an endorsed policy position and not a real-data calibrated forecasting model.


## Red-team incorporation release — v1.7.2
This release incorporates the v1.7.1 red-team and devil's advocate reviews into the actual launch artefacts: the risk-controlled thesis, model card, decision-maker summary, first-six Substack posts, launch gates and action register. RACMA remains excluded from active outreach.

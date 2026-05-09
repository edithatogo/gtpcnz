# Primary Care Funding Architecture: Australia and Aotearoa New Zealand

Version: **v1.2.1**

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
docs/substack-ready/    12 Substack-ready posts, figures, source bank, glossary and publication QA
docs/nzmj/              New Zealand Medical Journal Viewpoint and article/protocol material
docs/review/            Rapid scoping review protocol and extraction/screening material
docs/oia/               Official Information Act request drafts and trackers
docs/audit/             Claim-source ledger, traceability, research audit and v1.2.1 contract-compliance audit
models/                 Lightweight Python model scaffold and tests
outputs/                Generated public-facing reports, workbooks, plots and standalone artefacts
```

## Current release

This is **v1.2.1**, the contract-compliance audit and housekeeping release.

It verifies and patches the v1.2.0 package against the accumulated requirements:

- background and theory are laid out;
- the broader New Zealand policy game is mapped;
- each game has demonstrative modelling;
- uncertainty, hybrid synthesis, source-informed parameterised modelling and MCDA layers are present;
- policy briefs, reports, New Zealand Medical Journal material and validation plans are present;
- the Substack series has 12 human-readable, hyperlinked posts with figures, glossary and source bank;
- local Markdown links and figure references pass automated checks;
- README, Conductor track index and versioning metadata are updated;
- the package now includes git history in the v1.2.1 zip.

Key v1.2.1 audit outputs:

- `docs/audit/contract-compliance-audit-v1.2.1.md`
- `docs/audit/acceptance-criteria-matrix-v1.2.1.csv`
- `docs/audit/substack-post-qa-checklist-v1.2.1.csv`
- `docs/audit/local-link-audit-v1.2.1.csv`
- `docs/audit/remediation-log-v1.2.1.md`

## Substack-ready publication layer

The publication-ready draft series is in:

```text
docs/substack-ready/posts/
docs/substack-ready/figures/
docs/substack-ready/complete-substack-series-v1.2.0.md
docs/substack-ready/figure-placement-and-alt-text-v1.2.0.md
docs/substack-ready/plain-english-glossary-v1.2.0.md
docs/substack-ready/source-bank-v1.2.0.md
```

The posts are **Substack-ready drafts**, not final Dylan-signed-off copy. They still need final judgement on political sharpness, voice, Te Tiriti/Māori and Pacific nuance, and stakeholder risk.

## Testing

```bash
pytest -q
```

The v1.2.1 audit run passes the model test suite and local-link audit.

## Status and caveat

This repo is a working policy and research package, not a final endorsed RACMA/RACGP/RNZCGP/ACRRM/GPNZ position.

The modelling is demonstrative and source-informed. It can support stakeholder discussion, Substack publication, RACMA scoping, policy brief development and a New Zealand Medical Journal Viewpoint/protocol pathway. It should not be used to claim precise forecast effects without future empirical calibration and validation.


## Current release: v1.3.1

This release clarifies that the preferred architecture is **capitation + uncapped primary medical fee-for-service + place-based population accountability**. The cap is removed at the global eligible-activity level, while item prices, service definitions, clinical eligibility, provider scope, audit, co-payment protections and place-based obligations remain as safeguards.

# Inputs, Calibration, and Provenance

**Status:** Complete

## Problem

The repo is honest about being a public-data anchored benchmark, but the inputs layer is still mostly documentary. The user needs a stronger provenance and calibration-readiness story so that each public source, assumption, and missing dataset can be traced cleanly.

## Goal

Create a durable input/provenance layer that:

- records the source and purpose of each public input;
- separates public-source assumptions from empirical calibration inputs;
- keeps the OIA/data-gap tracker aligned with the current model story;
- carries claim-boundary metadata through public outputs;
- makes calibration readiness machine-readable, not just prose.

## Current State

| Concern | Current locations | Gap |
|---|---|---|
| Public claim boundary | `models/primarycare_model/scenario_service.py`, `docs/STREAMLIT-DEPLOYMENT.md`, `docs/REPORTS-AND-DASHBOARD.md` | Boundary language is consistent, but not yet machine-readable across every input surface. |
| Calibration readiness table | `models/primarycare_model/scenario_service.py` | Static documentation exists, but it is not yet a typed manifest or freshness-checked registry. |
| OIA/data gaps | `docs/audit/oia-request-tracker.csv`, `data/evidence/oia_request_tracker.csv` | Good inventory, but it is not yet linked to runtime or release gates. |
| Scenario loading | `models/primarycare_model/scenario_service.py` | Validation exists, but provenance is still shallow. |
| Public docs | `docs/calibration/model-card-v1.7.2.md`, `docs/launch/claim-boundaries-v1.7.2.md` | Strong caveat language, but no unified input manifest. |

## Target State

- every public input has source, date, transform, and status;
- calibration readiness can be inspected as data;
- OIA gaps are linked to the model components they would unlock;
- public claims stay anchored to the correct boundary label;
- provenance is visible in both the docs and the runtime-adjacent code.

## Acceptance Criteria

- a typed provenance or registry layer exists for the main public inputs;
- calibration readiness can be queried consistently from code and docs;
- OIA/data gaps are not just a CSV and prose note;
- claim-boundary metadata appears in the public output chain;
- the repo keeps its public-data-only boundary intact until linked data is actually available.

## Non-Goals

- Do not introduce linked-data claims.
- Do not require access to private or patient-level datasets.
- Do not block public explanation work while calibration remains pending.

## Verification

```powershell
python -m pytest -q models/tests/test_scenario_service.py models/tests/test_public_site_visual_contract.py
rg -n \"claim_boundary|calibration readiness|OIA|public-data anchored|not linked-data calibrated|not a patient-level forecast\" docs models data
```
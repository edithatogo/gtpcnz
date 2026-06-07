# Public Source Readiness Closeout v1

## 1. Current Status

| Property | Value |
|---|---|
| Calibration state | `calibration_readiness_only` |
| Claim level | `public_benchmark` |
| Claim-boundary status | `not_valid_for: [precise fiscal savings, ED reductions, hospital-demand reductions, workforce effects, implementation impacts, causal effects]` |
| Source checksums | 6 of 6 sources have `checksum: pending-download` |
| Calibration targets with `source_ready=false` | 3 of 3 targets |
| Track 053 gates | Both pass (calibration stays readiness-only because sources not ready) |
| Track 052 gates | All pass (snapshot infrastructure, retrieval-plan registry, and strict source-readiness flags exist, but no actual source files downloaded) |

All 6 registered public sources in `models/primarycare_model/registries/public/sources.public.v1.yaml` have `checksum: pending-download`. The calibration engine (`models/primarycare_model/calibration/public_aggregate_calibration.py`) gates all targets on `source.checksum != "pending-download"`, so every target currently reports `source_ready=false`.

The `data/public_raw/` and `data/public_processed/` directories exist but are empty (contain only `README.md` placeholders).

---

## 2. Public Source Retrieval Tasks

Each of the 6 registered sources has a machine-readable retrieval plan in `models/primarycare_model/registries/public/source_retrieval.public.v1.yaml`. The plan is checked by:

```
python scripts/check_public_source_retrieval_plan.py
```

The current retrieval status for every source is `reference_pinned_pending_download`: public reference pages are pinned, fetch entrypoints are source-pinned, but raw files and processed outputs have not been created. A single cross-stage readiness matrix is checked by:

```sh
python scripts/check_public_source_readiness_matrix.py
```

The strict matrix gate intentionally fails until raw files, verified checksums, and processed artifacts exist:

```sh
python scripts/check_public_source_readiness_matrix.py --strict
```

### 2.1 `src_hnz_capitation_schedule` — Health NZ Capitation and PHO Services Schedules

| Property | Value |
|---|---|
| URL | `https://www.tewhatuora.govt.nz/for-health-providers/primary-care-sector/capitation-rates` |
| Expected content | Published capitation funding rates by age/sex/ethnicity group; PHO services schedule values |
| Proposed raw file | `data/public_raw/src_hnz_capitation_schedule/capitation-rates.html` |
| Retrieval script | `scripts/fetch_hnz_capitation_schedule.py` |
| Task | Identify the exact schedule publication page, download the published PDF or CSV, place in `data/public_raw/` |

### 2.2 `src_pho_services_agreement` — PHO Services Agreement Public Schedule

| Property | Value |
|---|---|
| URL | `https://www.tewhatuora.govt.nz/for-health-providers/primary-care-sector/primary-health-organisation-services-agreement` |
| Expected content | Public schedule of consultation values, service fees, and funding formulae |
| Proposed raw file | `data/public_raw/src_pho_services_agreement/master-pho-services-agreement.pdf` |
| Retrieval script | `scripts/fetch_pho_services_agreement.py` |
| Task | Locate the PHO Services Agreement schedule, download published document(s), place in `data/public_raw/` |

### 2.3 `src_hnz_enrolment` — Primary Care Enrolment Public Data

| Property | Value |
|---|---|
| URL | `https://www.tewhatuora.govt.nz/for-health-professionals/data-and-statistics/primary-care` |
| Expected content | Aggregate enrolled population counts by DHB/region, age, sex |
| Proposed raw file | `data/public_raw/src_hnz_enrolment/primary-care-enrolment-public-data.html` |
| Retrieval script | `scripts/fetch_hnz_enrolment.py` |
| Task | Access the public enrolment dashboard or published tables, download aggregate counts, place in `data/public_raw/` |

### 2.4 `src_mcnz_workforce` — Medical Council Workforce Survey

| Property | Value |
|---|---|
| URL | `https://www.mcnz.org.nz/about-us/publications/workforce-survey/` |
| Expected content | Published aggregate workforce participation rates, FTE counts, demographics |
| Proposed raw file | `data/public_raw/src_mcnz_workforce/workforce-survey-report-2025.pdf` |
| Retrieval script | `scripts/fetch_mcnz_workforce.py` |
| Task | Access the Medical Council publications page, download the most recent workforce survey report, place in `data/public_raw/` |

### 2.5 `src_nz_health_survey` — New Zealand Health Survey Public Data Explorer

| Property | Value |
|---|---|
| URL | `https://minhealthnz.shinyapps.io/nz-health-survey-2023-24-annual-data-explorer/` |
| Expected content | Published aggregate survey output: cost barrier to GP access by demographic group |
| Proposed raw file | `data/public_raw/src_nz_health_survey/nz-health-survey-2023-24-cost-barrier-export.csv` |
| Retrieval script | `scripts/fetch_nz_health_survey.py` |
| Task | Use the public data explorer to export or extract the cost-barrier indicator table, place in `data/public_raw/` |

### 2.6 `src_statsnz_population` — Stats NZ Population Estimates

| Property | Value |
|---|---|
| URL | `https://www.stats.govt.nz/indicators/population-of-nz/` |
| Expected content | Estimated resident population (ERP) by DHB/region, age, sex — public tables |
| Proposed raw file | `data/public_raw/src_statsnz_population/population-of-nz-indicator.html` |
| Retrieval script | `scripts/fetch_statsnz_population.py` |
| Task | Download the most recent estimated resident population tables from Stats NZ public database, place in `data/public_raw/` |

### 2.7 Fetch script contract gate

Every `fetch_script` named in `models/primarycare_model/registries/public/source_retrieval.public.v1.yaml` must exist and be pinned to its source ID. The readiness-compatible gate is:

```
python scripts/check_public_source_fetch_scripts.py
```

The strict calibration-upgrade gate is:

```
python scripts/check_public_source_fetch_scripts.py --require-raw
```

Strict mode currently fails for all six public sources because no raw public source files have been retrieved into `data/public_raw/{source_id}/`. Individual source entrypoints can also be checked without network access or writes, for example:

```
python scripts/fetch_statsnz_population.py --check-only
```

Actual download is explicit and non-default:

```
python scripts/fetch_statsnz_population.py --download
```

---

## 3. Licence/Access Metadata Requirements

Each source currently has `licence_status: public_reference` and `public_access_status: public`. After retrieval, these must be verified and recorded more precisely.

### 3.1 Required metadata fields per source (in `sources.public.v1.yaml`)

| Field | Current value | Required post-retrieval |
|---|---|---|
| `url_or_reference` | Concrete public reference page | Must resolve to the exact page/document URL used in retrieval |
| `retrieval_date` | `2026-06-03` (placeholder) | Must be the actual date the file was downloaded |
| `licence_status` | `public_reference` | Must be confirmed as one of: `open_government`, `cc_by`, `public_domain`, `public_reference`, or equivalent known licence |
| `public_access_status` | `public` | Must be `public` — reject any source that requires authenticated access or has use restrictions |
| `licence_url` | (not present) | **Should be added** to record the URL of the licence terms |
| `attribution_required` | (not present) | **Should be added** to flag any attribution requirement |
| `checksum` | `pending-download` | Must be replaced with the computed SHA-256 hex digest of the downloaded file |
| `transform_description` | Brief sentence | Should be updated with exact steps run and output schema |

### 3.2 Verification gates

After retrieval, each source must pass:
1. **`licence_status`** is a known non-restrictive public licence (one of: `open_government`, `cc_by`, `cc0`, `public_domain`, `public_reference`).
2. **`public_access_status`** is `public` — no login wall, no data use agreement required beyond standard attribution.
3. **`url_or_reference`** resolves to the exact download URL, not a search portal.
4. No patient-level, practitioner-level, or confidential fields are present.

---

## 4. Checksum Verification Tasks

### 4.1 Current state

All 6 sources: `checksum: pending-download`.

### 4.2 Required tasks

| # | Task | Script/File | Gate |
|---|---|---|---|
| 1 | Download each source file to `data/public_raw/{source_id}/` | `scripts/fetch_*.py` (6 source-pinned scripts) and `python scripts/check_public_source_fetch_scripts.py --require-raw` | File exists in expected path |
| 2 | Compute SHA-256 checksum of each downloaded raw file | `python -c "import hashlib; print(hashlib.sha256(open(f,'rb').read()).hexdigest())"` | Checksum is a 64-char hex string |
| 3 | Update `checksum` field in `sources.public.v1.yaml` | Manual edit or update script | Value matches computed hash |
| 4 | Rebuild snapshot manifest | `python scripts/build_public_source_snapshot.py` | Snapshot JSON reflects the new checksums |
| 5 | Run snapshot checker | `python scripts/check_public_source_snapshot.py` | Returns exit code 0 |
| 6 | Run snapshot test | `python -m pytest -q models/tests/test_public_source_snapshot.py` | Test passes |

### 4.3 Future drift detection

Strict checksum drift detection is implemented as an opt-in readiness gate:

```
python scripts/check_public_source_snapshot.py --verify-checksums
```

This script recomputes checksums of files in `data/public_raw/` and compares against `sources.public.v1.yaml`. With the current pending-download registry, it intentionally fails and keeps calibration at `calibration_readiness_only`.

---

## 5. Transformation Pipeline Requirements

### 5.1 Current state

`data/public_processed/` is empty. Source-specific transform entrypoints now exist and are registry-gated. They remain readiness-compatible until raw public artifacts exist; source-specific parsing still cannot produce processed outputs until public raw files are retrieved.

### 5.2 Required pipeline stages

```
data/public_raw/          data/public_processed/       models/primarycare_model/registries/public/
   │                            │                                │
   ▼                            ▼                                ▼
[raw download] ──> [extract/parse] ──> [validate schema] ──> [inputs/v1, calibration_targets/v1, parameters/v1]
```

### 5.3 Transform entrypoint scripts

| Script | Purpose | Input | Output |
|---|---|---|---|
| `scripts/transform_hnz_capitation.py` | Parse capitation schedule into structured parameter values | `data/public_raw/src_hnz_capitation_schedule/*` | Validated schema -> registry updates |
| `scripts/transform_pho_agreement.py` | Extract consultation fee schedule values | `data/public_raw/src_pho_services_agreement/*` | Validated schema -> registry updates |
| `scripts/transform_hnz_enrolment.py` | Extract aggregate enrolment counts | `data/public_raw/src_hnz_enrolment/*` | Validated schema -> registry updates |
| `scripts/transform_mcnz_workforce.py` | Extract workforce participation rates | `data/public_raw/src_mcnz_workforce/*` | Validated schema -> registry updates |
| `scripts/transform_nz_health_survey.py` | Extract cost-barrier access indicators | `data/public_raw/src_nz_health_survey/*` | Validated schema -> registry updates |
| `scripts/transform_statsnz_population.py` | Extract population estimates for calibration | `data/public_raw/src_statsnz_population/*` | Validated schema -> registry updates |

### 5.4 Transform script contract gate

Every `transform_script` named in `models/primarycare_model/registries/public/source_retrieval.public.v1.yaml` must exist and be pinned to its source ID. The readiness-compatible gate is:

```
python scripts/check_public_source_transform_scripts.py
```

The strict calibration-upgrade gate is:

```
python scripts/check_public_source_transform_scripts.py --require-raw
```

Strict mode currently fails for all six public sources because no raw public source files have been retrieved into `data/public_raw/{source_id}/`. Individual source entrypoints can also be checked without writing outputs, for example:

```
python scripts/transform_statsnz_population.py --check-only
```

### 5.5 Schema validation requirements

Each transformed dataset must be validated against schemas defined in:
- `models/primarycare_model/contracts/inputs.py`
- `models/primarycare_model/registries/public/inputs.public.v1.yaml`

Validation checks:
- All `required: true` fields present with correct data types
- No NULL/NaN values in required fields
- Values within expected ranges (e.g., population counts positive, rates in [0,1])
- No patient-level identifiers present

### 5.6 Processed file format

Transformed files land in `data/public_processed/` with:
- Standard format: Parquet or CSV with schema header
- A companion `.hash` file (SHA-256 of the processed file)
- A `_metadata.yaml` file recording:
  - Source ID
  - Transformation script used and its version
  - Date of transformation
  - Row count, column list, null counts
  - Schema version

### 5.7 Processed schema validation gate

The processed-input schema validator is implemented as:

```
python scripts/check_transformed_schemas.py
```

The default mode is readiness-compatible and passes while processed artifacts are absent. The calibration-upgrade gate is strict and must fail until the expected transformed CSV and `_metadata.yaml` files exist for registry-backed public input datasets:

```
python scripts/check_transformed_schemas.py --require-processed
```

The strict gate currently reports the missing Stats NZ population and NZ Health Survey processed artifacts and does not alter claim status.

---

## 6. Validation Gate Requirements

### 6.1 Source-level gates (must all pass for a single source to be `source_ready=true`)

| Gate | Check | Script |
|---|---|---|
| G1 | Raw file exists at expected `data/public_raw/{source_id}/` path | `scripts/check_public_source_snapshot.py --verify-files`, `python scripts/check_public_source_fetch_scripts.py --require-raw`, and `python scripts/check_public_source_transform_scripts.py --require-raw` |
| G2 | SHA-256 checksum matches `sources.public.v1.yaml` entry | `scripts/check_public_source_snapshot.py --verify-checksums` |
| G3 | Licence status is one of the allowed public licences | `scripts/check_public_source_snapshot.py --verify-licences` |
| G4 | Public access status is `public` | `scripts/check_public_source_snapshot.py` (existing check) |
| G5 | No patient-level or practitioner-level fields | `scripts/check_no_patient_data.py` (extended for raw data) |
| G6 | Transformed file exists at `data/public_processed/{source_id}/` | `scripts/check_public_source_snapshot.py --verify-processed` |
| G7 | Transformed file passes schema validation | `python scripts/check_transformed_schemas.py --require-processed` and `python -m pytest -q models/tests/test_transformed_schemas.py` |
| G8 | Processed checksum matches companion `.hash` file | `scripts/check_public_source_snapshot.py --verify-processed` |
| G9 | Cross-stage source readiness matrix shows the same raw, checksum, processed, and claim status | `python scripts/check_public_source_readiness_matrix.py --strict` |

### 6.2 Calibration-level gates (must pass for calibration to upgrade from `calibration_readiness_only`)

| Gate | Check | Script |
|---|---|---|
| C1 | All 6 sources pass G1–G8 | See above |
| C2 | All 3 calibration targets have `source_ready=true` and target-level blocker matrix is clear | `python scripts/check_calibration_target_readiness.py --strict` and `python scripts/run_public_aggregate_calibration.py --check-only` |
| C3 | Calibration validation gates report baseline, holdout, PPC, and claim-downgrade status | `python scripts/check_calibration_validation_gates.py --strict` and `python scripts/run_public_aggregate_calibration.py` (full run) |
| C4 | Precision claims still prohibited | Assert `not_valid_for` list preserved |
| C5 | Public mirror drift check | `python scripts/sync_public_mirror.py --check` |

### 6.3 Post-gate claim upgrade

Only when **all** gates G1–G8 **and** C1–C5 pass:

| Field | Current value | Post-gate value |
|---|---|---|
| `calibration_status` | `calibration_readiness_only` | `public_aggregate_validated` |
| `claim_level` | `public_benchmark` | `empirically_supported_if_gated` |
| `source_ready` (per target) | `false` | `true` |

**Precise fiscal savings, ED reductions, hospital-demand reductions, workforce effects, implementation impacts, and causal effects remain `not_valid_for`** unless separate, specific public-data gates for those claim types independently pass.

---

## 7. Explicit Exclusion List

The following inputs are **not proposed** and must never be used in the public-source readiness pipeline:

| Category | Examples | Reason for exclusion |
|---|---|---|
| Private administrative data | PHO claims data, NHI-linked primary care records, Schedule of Personal Medical Services payments | Not public; contains patient-level or practitioner-level data |
| Patient-level data | Individual enrolment records, individual consultation records, patient identifiers | Not aggregate; cannot be used without ethics/privacy review |
| Confidential OIA responses | OIA requests with redacted commercial information, unredacted contracts | Not published; may contain confidential business information |
| Stakeholder analysis | DHB submissions, sector-group advocacy documents, unpublished consultation responses | Not independently verifiable; not published aggregate data |
| Unpublished expert elicitation | Internal SME estimates, workshop outputs, Delphi panels with unpublished protocols | Not published; not reproducible from public sources |
| Commercial-in-confidence data | PHO-level reconciliation reports, DHB-specific funding flows, pharmacy/community provider contracts | Not public; restricted by commercial sensitivity |
| Person-level survey microdata | Individual NZ Health Survey responses, Census individual records | Requires data use agreement; not public aggregate |

All public-source readiness gates must reject any file that falls into the above categories.

---

## 8. Calibration Readiness Lock

> **Calibration remains at `calibration_readiness_only` until all of the following conditions are met:**
>
> 1. All 6 public source files are downloaded to `data/public_raw/` with verified SHA-256 checksums that replace `pending-download` in `sources.public.v1.yaml`.
> 2. Every source has its licence status confirmed as a known public licence and its public access status confirmed as `public`.
> 3. All sources pass `scripts/check_public_source_snapshot.py` with exit code 0 and no warnings.
> 4. Transformation scripts exist and produce validated output in `data/public_processed/`.
> 5. Processed files pass schema validation against the contracts in `inputs.public.v1.yaml`.
> 6. All 3 calibration targets have `source_ready=true` when `python scripts/check_calibration_target_readiness.py --strict` and `python scripts/run_public_aggregate_calibration.py --check-only` run.
> 7. `python scripts/check_calibration_validation_gates.py --strict` and `python scripts/check_posterior_predictive_checks.py --strict` pass for baseline, public holdout, posterior predictive, and claim-downgrade gates.
> 8. The `not_valid_for` precision-claim list remains intact and cannot be bypassed.
> 9. The public mirror (`public/gtpcnz`) drift check passes.
>
> Until every gate in Sections 4–6 passes, the claim boundary remains:
>
> ```
> calibration_status: calibration_readiness_only
> claim_level: public_benchmark
> not_valid_for:
>   - precise fiscal savings
>   - ED reductions
>   - hospital-demand reductions
>   - workforce effects
>   - implementation impacts
>   - causal effects
> ```

---

## 9. Summary of Required Work

| Layer | Current state | Target state | Owner |
|---|---|---|---|
| Source retrieval | 0/6 files downloaded; 6/6 retrieval plans and fetch scripts pinned | 6/6 files in `data/public_raw/` with verified checksums | Post-063 work packages |
| Licence/access metadata | Placeholder values | Verified per-source with `licence_url` | Post-063 work packages |
| Checksums | `pending-download` on all 6 | SHA-256 hash on all 6 | Post-063 work packages |
| Transformation | Source-specific transform entrypoints and transform-script gate exist; source-specific parsers await raw files | 6 transformation scripts plus validated processed CSV/metadata outputs | Post-063 work packages |
| Validation gates | Default snapshot, retrieval, fetch, transform, readiness-matrix, and transformed-schema checkers pass; strict `--verify-files`, `--verify-checksums`, `--verify-processed`, `--verify-licences`, `check_public_source_fetch_scripts.py --require-raw`, `check_public_source_transform_scripts.py --require-raw`, `check_public_source_readiness_matrix.py --strict`, and `check_transformed_schemas.py --require-processed` gates exist and currently expose missing source files/processed artifacts | Strict gates pass after public downloads and transforms | Post-063 work packages |
| Calibration upgrade | `calibration_readiness_only` | `public_aggregate_validated` only after all gates pass | Post-063 work packages |

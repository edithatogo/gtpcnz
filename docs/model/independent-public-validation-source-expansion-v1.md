# Independent Public Validation Source Expansion v1

Track 073 adds a candidate layer for public validation sources that are not yet part of the runtime public source snapshot.

## Current Candidate Decisions

| Candidate | Status | Validation family | Decision |
|---|---|---|---|
| Ministry of Health planning and performance historical measures | Registered retrieval-plan candidate | Hospital pressure, avoidable admissions, district holdout | Public page identifies district planning/performance measures including acute hospital bed days, readmissions, ambulatory sensitive hospital admissions, inpatient length of stay, and youth alcohol-related ED presentations. It is independent of the current population, NZHS cost-barrier, workforce, PHO access, and capitation runtime sources, but it is not loaded by runtime until raw download, checksum, transform, schema, and comparison gates pass. |
| HQSC Atlas of Healthcare Variation PHO analyses | Candidate pending locator | PHO variation and equity | Public Atlas navigation identifies PHO-analysis domains, but domain-specific machine-readable export locators and licence/grain review are still required before registration as a retrieval-ready source. |
| New Zealand Health Survey regional release | Rejected for independent-validation counting | Regional unmet need and equity | Public and useful for descriptive checks, but not independent of the current `src_nz_health_survey` calibration target source. It must not satisfy independent validation for that target family. |

## Boundary

These records are not runtime model inputs. They do not alter public parameters, calibration targets, validation gates, outputs, or claims. They are not valid for precise fiscal savings, ED reductions, hospital-demand reductions, workforce effects, implementation impacts, or causal effects.

The registered Ministry planning/performance candidate can move into the runtime source registry only after a later track checks in the raw public source file, verifies checksums and licence/access metadata, produces schema-valid processed artifacts with hash sidecars, and adds defensible model-vs-public comparison rules.

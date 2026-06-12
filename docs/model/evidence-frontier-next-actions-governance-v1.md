# Evidence frontier next actions governance v1

This note records follow-up governance for the remaining evidence frontier after Tracks 072 and 073. It is documentation only. It does not change runtime registries, source snapshots, calibration targets, validation gates, outputs, or claims.

## Current frontier

| Frontier item | Current role | Runtime status | Follow-up action |
|---|---|---|---|
| PHO Services Agreement public schedule | Reference-only policy-shock plausibility source | Not a numeric comparison input | Find an official public URL that returns valid PHO Services Agreement PDF bytes, or an official public machine-readable schedule table, before any bounded table-cell extraction is attempted. |
| Ministry planning and performance historical measures | Registered retrieval-plan candidate | Not loaded by runtime | Acquire the raw public artifact, verify checksum and licence/access metadata, transform to schema-valid processed outputs with hash sidecars, then add defensible model-vs-public comparison rules before runtime use. |
| HQSC Atlas of Healthcare Variation PHO analyses | Candidate pending locator | Not loaded by runtime | Identify domain-specific machine-readable export locators, confirm licence/access terms, verify PHO-level grain, and document independence from current calibration targets before retrieval-plan registration. |

## PHO Services Agreement blocker

The Track 072 blocker is source-resolution, not model evidence. The registry-pinned public URL currently returns HTML under the expected PDF filename, so the bounded transform records `extraction_blocked` rather than table values.

Until a verified public replacement resolves to valid PHO Services Agreement PDF bytes or an official machine-readable schedule table, this source remains reference-only. It must not be used to pass a numeric pre/post comparison lane, alter CAL-G-005, or support claims about pass-through, transaction costs, fiscal effects, hospital demand, workforce effects, implementation impacts, or causal effects.

## Track 073 candidate sources

The Ministry and HQSC records are validation-source governance records only. They identify possible independent public validation families, but they are not source-ready runtime inputs.

The Ministry planning/performance candidate has a retrieval plan, but runtime use still requires checked-in raw evidence, checksum verification, licence/access confirmation, processed artifacts, schema validation, and comparison-gate logic. The HQSC Atlas PHO candidate is earlier-stage: it still needs a domain-specific export locator, grain review, licence/access review, and independence review before it can become retrieval-ready.

## Runtime-use gate

No frontier source can be promoted into runtime use until a later track documents all of the following:

- official public source locator and access/licence status;
- raw artifact checked into the public evidence custody path with SHA-256 metadata;
- deterministic fetch and transform scripts;
- schema-valid processed artifact with hash sidecar;
- explicit comparison contract naming the affected CAL-G lane or validation family;
- passing validation gate output;
- updated claim-boundary review confirming no precision, fiscal, ED, hospital-demand, workforce, implementation-impact, or causal claim expansion without claim-specific evidence.

Until those conditions are met, the current public aggregate validation posture remains unchanged.

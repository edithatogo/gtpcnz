# Implementation Log

2026-06-03: Initial public-only SOTA calibration scaffold added with strict claim-boundary posture.

2026-06-03: Cline/deepseek parallel execution controls added: dependency wave, file ownership, work packages, subagent prompts, collision rules, and exact gates.


2026-06-03: Wave 1 completion (Cline DeepSeek v4 Flash coordinator run).
  Work packages: WP-052-A (source-contracts), WP-052-B (snapshot-builder), WP-052-C (checksum-readiness), WP-052-D (processed-schema).
  Files changed: Verified models/primarycare_model/contracts/public_sources.py, models/primarycare_model/data/public_source_snapshot.py, models/primarycare_model/registries/public/sources.public.v1.yaml, data/public_raw/**, data/public_processed/**, data/snapshots/**, scripts/build_public_source_snapshot.py, scripts/check_public_source_snapshot.py, models/tests/test_public_source_snapshot.py.
  Gates run:
    - python scripts/build_public_source_snapshot.py -> PASSED
    - python scripts/check_public_source_snapshot.py -> PASSED
    - python -m pytest -q models/tests/test_public_source_snapshot.py -> PASSED (1 passed)
  Result: All 3 gates pass. Public source snapshots built and validated.
  Claim-boundary status: public_benchmark (snapshot readiness; no source_ready flag promoted).
  Residual blockers: None. All sources have URL/reference, retrieval date, licence status, checksum entries.
  Follow-on owner: coordinator (052 complete; 053, 057, 059 unblocked).

2026-06-05: Strict public-source readiness flags implemented.
  Work packages: WP-052-C (checksum-readiness), WP-052-D (processed-schema).
  Files changed: models/primarycare_model/data/public_source_snapshot.py, scripts/check_public_source_snapshot.py, models/tests/test_public_source_snapshot.py, docs/model/public-source-readiness-closeout-v1.md, conductor/tracks/052-public-source-ingestion-and-snapshots/implementation-log.md.
  Gates run:
    - python -m pytest -q models/tests/test_public_source_snapshot.py -> PASSED (4 passed)
    - python scripts/check_public_source_snapshot.py -> PASSED
    - python scripts/check_public_source_snapshot.py --verify-licences -> PASSED
    - python scripts/check_public_source_snapshot.py --verify-files --verify-checksums --verify-processed -> FAILED AS EXPECTED because all six registered public sources still have no raw files, checksum: pending-download, and no processed outputs.
  Result: Default readiness-only snapshot gate remains CI-compatible. Strict opt-in gates now make public-source retrieval, checksum replacement, and processed-output creation machine-checkable.
  Claim-boundary status: public_benchmark / calibration_readiness_only preserved. No source was promoted to source_ready=true.
  Residual blockers: All six public sources still require reproducible download, checksum replacement, transformation, and processed-output hash manifests.
  Follow-on owner: coordinator (next public-source retrieval work).

2026-06-05: Public source registry references narrowed from home pages to concrete public source pages.
  Work package: WP-052-A (source-contracts), WP-052-B (snapshot-builder).
  Files changed: models/primarycare_model/registries/public/sources.public.v1.yaml, data/snapshots/public-source-snapshot-v1.json, conductor/tracks/052-public-source-ingestion-and-snapshots/implementation-log.md, public/gtpcnz mirror files.
  Evidence used: official public pages for Health NZ capitation rates, PHO Services Agreement, Health NZ primary-care data/statistics, MCNZ workforce survey, NZ Health Survey explorer, and Stats NZ estimated population indicator.
  Gates run:
    - python scripts/build_public_source_snapshot.py -> PASSED
    - python scripts/check_public_source_snapshot.py -> PASSED
  Result: Public source records now use concrete public reference pages rather than generic organisation home pages. Checksums remain pending-download.
  Claim-boundary status: public_benchmark / calibration_readiness_only preserved. No source was promoted to source_ready=true.

2026-06-05: Public source retrieval-plan registry and checker added.
  Work package: WP-052-A (source-contracts), WP-052-C (checksum-readiness).
  Files changed: models/primarycare_model/contracts/public_sources.py, models/primarycare_model/data/public_source_retrieval.py, models/primarycare_model/registries/public/source_retrieval.public.v1.yaml, scripts/check_public_source_retrieval_plan.py, models/tests/test_public_source_retrieval_plan.py, docs/model/public-source-readiness-closeout-v1.md, conductor/tracks/052-public-source-ingestion-and-snapshots/implementation-log.md.
  Gates run:
    - python scripts/check_public_source_retrieval_plan.py -> PASSED
    - python -m pytest -q models/tests/test_public_source_retrieval_plan.py -> PASSED
  Result: Every public source now has a typed retrieval plan with source_id, public reference URL, expected raw path, retrieval method, transform script, expected processed output, and pending-download status.
  Claim-boundary status: public_benchmark / calibration_readiness_only preserved. Retrieval plans are references only and do not promote source_ready=true.

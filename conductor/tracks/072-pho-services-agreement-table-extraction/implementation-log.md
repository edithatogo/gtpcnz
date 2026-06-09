# Implementation Log

- Track opened because the PHO Services Agreement PDF is currently public custody evidence only.
- Current CAL-G-005 pass depends on the capitation schedule bounded policy-condition comparison, not PHO Services Agreement numeric extraction.
- `python scripts/fetch_pho_services_agreement.py --download` was run against the registry-pinned public URL.
- The fetched artifact was written to `data/public_raw/src_pho_services_agreement/master-pho-services-agreement.pdf` with fetch metadata sidecar.
- The fetched artifact is not valid PDF bytes: it starts with `<!doctype html>` and `pypdf` reports an invalid PDF header / missing EOF marker.
- The bounded transform now detects the media type and writes `data/public_processed/src_pho_services_agreement/pho_services_schedule.csv` as a deterministic `extraction_blocked` artifact with raw hash, byte size, media type, blocker reason, provenance placeholders, and claim boundary.
- The PHO Services Agreement row remains `reference_only` for CAL-G-005 and does not block or inflate the capitation schedule numeric comparison lane.
- Documentation is recorded in `docs/model/pho-services-agreement-bounded-extraction-v1.md`.

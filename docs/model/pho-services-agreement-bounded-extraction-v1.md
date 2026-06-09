# PHO Services Agreement bounded extraction v1

Track 072 attempted bounded table extraction from the public PHO Services Agreement source registered as `src_pho_services_agreement`.

## Source status

The registry-pinned public URL is:

`https://www.tewhatuora.govt.nz/assets/For-health-providers/Primary-care-sector/Master-PHO-Services-Agreement-.pdf`

The repository fetch script was run against that URL and wrote:

`data/public_raw/src_pho_services_agreement/master-pho-services-agreement.pdf`

The fetched artifact is not valid PDF bytes. It begins with `<!doctype html>` and `pypdf` raises an invalid-header / missing-EOF error. The fetched page title is for oral health service specifications, not the PHO Services Agreement.

## Processed artifact

The transform now writes a deterministic blocker artifact:

`data/public_processed/src_pho_services_agreement/pho_services_schedule.csv`

The artifact records:

- source identifier;
- raw artifact SHA-256;
- raw artifact filename and byte size;
- detected media type;
- extraction status;
- blocker reason;
- empty page/table/row/column provenance fields;
- claim boundary.

Current status is `extraction_blocked` because the current public download returns HTML where the bounded extractor expected PDF bytes.

## Claim boundary

This source remains reference-only for CAL-G-005. It does not support a numeric pre/post comparison lane and does not authorize claims about:

- pass-through;
- transaction costs;
- fiscal effects;
- hospital demand;
- workforce effects;
- implementation impacts;
- causal effects.

The current CAL-G-005 pass continues to depend on the capitation schedule numeric comparison lane, not on PHO Services Agreement extraction.

## Next source action

To move beyond this blocker, the source registry needs a public URL that resolves to valid PHO Services Agreement PDF bytes or an official public machine-readable schedule table. Only then should the transform be upgraded from blocker provenance to table-cell extraction.

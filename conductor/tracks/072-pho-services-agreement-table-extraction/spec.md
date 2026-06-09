# Track 072 - PHO Services Agreement bounded table extraction

Move the PHO Services Agreement public PDF from custody-manifest-only evidence toward bounded, schema-valid public table extraction where the PDF permits deterministic extraction.

This track covers:

- extracting clearly bounded public schedule tables from the checked-in PHO Services Agreement PDF;
- recording table, page, row, column, source hash, and transform provenance;
- deciding whether any extracted table supports a future CAL-G-005 `numeric_comparison` lane;
- keeping the current PHO Services Agreement policy-shock row as `reference_only` unless the extracted data satisfies the strengthened comparison contract.

This track does not infer missing values, use private PHO data, or claim pass-through, transaction-cost, fiscal, workforce, hospital, implementation, or causal effects.

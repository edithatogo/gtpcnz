# Plan

1. Inspect the checked-in PHO Services Agreement PDF and identify extractable public schedule tables.
2. Implement a deterministic bounded transform that writes table cells with page/table/row/column provenance.
3. Add schema validation and hash sidecars for the processed artefact.
4. Update source retrieval/transform docs only if the processed artefact becomes more than a PDF manifest.
5. Assess whether any extracted row can support a future CAL-G-005 numeric comparison; keep `reference_only` if not.

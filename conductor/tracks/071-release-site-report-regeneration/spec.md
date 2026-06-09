# Track 071 - Release site and report regeneration after aggregate validation

Regenerate and verify public release artefacts after CAL-G-001 through CAL-G-007 pass and the aggregate calibration lane reports `public_aggregate_validated` / `empirically_supported_if_gated`.

This track covers:

- regenerating release model cards, manifests, Quarto outputs, and public-site artefacts from checked-in public snapshots;
- ensuring generated artefacts carry the new aggregate-validation status;
- preserving not-valid-for warnings around precise fiscal, ED, hospital-demand, workforce, implementation, and causal claims;
- checking that GitHub Pages and report outputs are reproducible from the same source snapshot and manifest hashes.

This track does not add new evidence, alter model parameters, or broaden claim boundaries beyond aggregate validation.

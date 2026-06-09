# Plan

1. Run the release manifest and model-card generators from a clean checkout.
2. Render the Quarto report/site and capture generated artefact paths.
3. Verify the generated site/report surfaces show `public_aggregate_validated` only for aggregate validation.
4. Verify every release-facing artefact preserves not-valid-for warnings for precision and causal claims.
5. Update docs/release evidence with command outputs, generated hashes, and any remaining publication blockers.

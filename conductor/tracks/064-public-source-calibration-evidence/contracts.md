# Contracts

Primary contracts:

- `CON-PUBLIC-001`: public source admissibility.
- `CON-CAL-001`: public aggregate calibration.
- `CON-VIS-001`: public-facing claim grammar where evidence is visualised.

Required claim posture:

- Public source evidence may be marked `public_aggregate_source_ready` only after raw artefacts, checksums, licence/access checks, processed artefacts, and schema validation pass.
- Calibration output remains `calibration_readiness_only` while any validation family is `public_data_unavailable`.
- Precision or causal claims remain explicitly prohibited.

Required gates:

```powershell
uv run --frozen --all-groups python scripts/check_public_source_snapshot.py --verify-files --verify-checksums --verify-licences --verify-processed
uv run --frozen --all-groups python scripts/check_public_source_readiness_matrix.py --strict
uv run --frozen --all-groups python scripts/check_transformed_schemas.py --require-processed
uv run --frozen --all-groups python scripts/run_public_aggregate_calibration.py --check-only
uv run --frozen --all-groups python -m pytest -q models/tests/test_public_source_calibration_evidence.py
```

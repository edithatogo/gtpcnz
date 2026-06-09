# Contracts

- Candidate sources must be public or published and must pass public-only boundary checks before runtime use.
- New validation rows must include source ID, period/geography/subgroup grain, metric definition, tolerance rule, and not-valid-for warnings.
- Validation expansions must not reuse the same aggregate source as both calibration target and independent validation target without explicitly documenting dependence.
- Claim-specific upgrades require claim-specific validation gates; aggregate validation alone is insufficient for precision or causal claims.

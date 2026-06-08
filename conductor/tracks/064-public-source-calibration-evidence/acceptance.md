# Acceptance

- All six public sources have non-placeholder SHA-256 checksums.
- Strict source readiness gates pass.
- Processed public input schemas pass in `--require-processed` mode.
- Public aggregate calibration target readiness passes.
- Calibration validation gate output records baseline and PPC pass while holdout/subgroup/policy-shock validation remains unavailable.
- Calibration output remains `calibration_readiness_only` and `claim_level: public_benchmark`.
- Documentation no longer says source retrieval is `0/6` or that all checksums are `pending-download`.

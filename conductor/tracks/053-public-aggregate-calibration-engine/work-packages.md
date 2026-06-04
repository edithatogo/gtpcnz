# Work Packages

Recommended Cline model: DeepSeek v4 Flash.

Parallelism policy:

- Run these packages in parallel only if their files do not overlap.
- Keep each package to one subagent and one level of delegation.
- Escalate to the coordinator for any cross-track edit.

| Work package | Subagent role | Task | Allowed files | Stop condition |
|---|---|---|---|---|
| WP-053-A | `target-registry` | Define public aggregate targets and validation gates by family. | models/primarycare_model/calibration/**, models/primarycare_model/contracts/calibration_targets.py, models/primarycare_model/registries/public/calibration_targets.public.v1.yaml, scripts/run_public_aggregate_calibration.py, docs/calibration/public-aggregate-calibration-methods-v1.md, models/tests/test_public_aggregate_calibration.py | Gates pass or blocker logged. |
| WP-053-B | `calibration-runner` | Implement transparent public-only calibration that downgrades when public source readiness fails. | models/primarycare_model/calibration/**, models/primarycare_model/contracts/calibration_targets.py, models/primarycare_model/registries/public/calibration_targets.public.v1.yaml, scripts/run_public_aggregate_calibration.py, docs/calibration/public-aggregate-calibration-methods-v1.md, models/tests/test_public_aggregate_calibration.py | Gates pass or blocker logged. |
| WP-053-C | `ppc-and-holdouts` | Add baseline, temporal, subgroup/geographic, and PPC hooks where public data permit. | models/primarycare_model/calibration/**, models/primarycare_model/contracts/calibration_targets.py, models/primarycare_model/registries/public/calibration_targets.public.v1.yaml, scripts/run_public_aggregate_calibration.py, docs/calibration/public-aggregate-calibration-methods-v1.md, models/tests/test_public_aggregate_calibration.py | Gates pass or blocker logged. |
| WP-053-D | `claim-downgrade` | Prove failed or missing gates force `public_benchmark` status and not-valid-for warnings. | models/primarycare_model/calibration/**, models/primarycare_model/contracts/calibration_targets.py, models/primarycare_model/registries/public/calibration_targets.public.v1.yaml, scripts/run_public_aggregate_calibration.py, docs/calibration/public-aggregate-calibration-methods-v1.md, models/tests/test_public_aggregate_calibration.py | Gates pass or blocker logged. |

Handoff format:

```text
Work package:
Files changed:
Gates run:
Result:
Claim-boundary status:
Residual blockers:
Follow-on owner:
```

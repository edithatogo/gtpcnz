# Work Packages

Recommended Cline model: DeepSeek v4 Flash.

Parallelism policy:

- Run these packages in parallel only if their files do not overlap.
- Keep each package to one subagent and one level of delegation.
- Escalate to the coordinator for any cross-track edit.

| Work package | Subagent role | Task | Allowed files | Stop condition |
|---|---|---|---|---|
| WP-052-A | `source-contracts` | Require URL/reference, retrieval date, licence/access status, checksum, transform and claim boundary. | models/primarycare_model/contracts/public_sources.py, models/primarycare_model/data/public_source_snapshot.py, models/primarycare_model/registries/public/sources.public.v1.yaml, data/public_raw/**, data/public_processed/**, data/snapshots/**, scripts/build_public_source_snapshot.py, scripts/check_public_source_snapshot.py, models/tests/test_public_source_snapshot.py | Gates pass or blocker logged. |
| WP-052-B | `snapshot-builder` | Build deterministic snapshot manifests from public registry files only. | models/primarycare_model/contracts/public_sources.py, models/primarycare_model/data/public_source_snapshot.py, models/primarycare_model/registries/public/sources.public.v1.yaml, data/public_raw/**, data/public_processed/**, data/snapshots/**, scripts/build_public_source_snapshot.py, scripts/check_public_source_snapshot.py, models/tests/test_public_source_snapshot.py | Gates pass or blocker logged. |
| WP-052-C | `checksum-readiness` | Keep pending checksums as readiness blockers, not calibration success. | models/primarycare_model/contracts/public_sources.py, models/primarycare_model/data/public_source_snapshot.py, models/primarycare_model/registries/public/sources.public.v1.yaml, data/public_raw/**, data/public_processed/**, data/snapshots/**, scripts/build_public_source_snapshot.py, scripts/check_public_source_snapshot.py, models/tests/test_public_source_snapshot.py | Gates pass or blocker logged. |
| WP-052-D | `processed-schema` | Document schemas and hash manifests for processed public datasets. | models/primarycare_model/contracts/public_sources.py, models/primarycare_model/data/public_source_snapshot.py, models/primarycare_model/registries/public/sources.public.v1.yaml, data/public_raw/**, data/public_processed/**, data/snapshots/**, scripts/build_public_source_snapshot.py, scripts/check_public_source_snapshot.py, models/tests/test_public_source_snapshot.py | Gates pass or blocker logged. |

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

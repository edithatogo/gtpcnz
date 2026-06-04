# Work Packages

Recommended Cline model: DeepSeek v4 Flash.

Parallelism policy:

- Run these packages in parallel only if their files do not overlap.
- Keep each package to one subagent and one level of delegation.
- Escalate to the coordinator for any cross-track edit.

| Work package | Subagent role | Task | Allowed files | Stop condition |
|---|---|---|---|---|
| WP-057-A | `report-structure` | Cover methods, sources, parameters, calibration, uncertainty, VOI, limitations and claim boundaries. | reports/public_aggregate_model_report.qmd, docs/release/model-card-template.qmd, scripts/render_public_model_report.py, models/tests/test_report_artifacts.py | Gates pass or blocker logged. |
| WP-057-B | `generated-figures` | Read figures/tables from reproducible outputs, not manual copies. | reports/public_aggregate_model_report.qmd, docs/release/model-card-template.qmd, scripts/render_public_model_report.py, models/tests/test_report_artifacts.py | Gates pass or blocker logged. |
| WP-057-C | `model-card-template` | Keep model-card template aligned with release manifest fields. | reports/public_aggregate_model_report.qmd, docs/release/model-card-template.qmd, scripts/render_public_model_report.py, models/tests/test_report_artifacts.py | Gates pass or blocker logged. |
| WP-057-D | `report-tests` | Assert expected report artefacts exist and are render-addressable. | reports/public_aggregate_model_report.qmd, docs/release/model-card-template.qmd, scripts/render_public_model_report.py, models/tests/test_report_artifacts.py | Gates pass or blocker logged. |

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

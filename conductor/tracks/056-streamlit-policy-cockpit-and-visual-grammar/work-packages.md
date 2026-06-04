# Work Packages

Recommended Cline model: DeepSeek v4 Flash.

Parallelism policy:

- Run these packages in parallel only if their files do not overlap.
- Keep each package to one subagent and one level of delegation.
- Escalate to the coordinator for any cross-track edit.

| Work package | Subagent role | Task | Allowed files | Stop condition |
|---|---|---|---|---|
| WP-056-A | `chart-contract` | Every chart exposes title, unit, claim, calibration, uncertainty, source, interpretation, warning, download and table fallback. | models/primarycare_model/ui/**, models/primarycare_model/app.py, docs/visualisation/visual-grammar-contract-v1.md, models/tests/test_streamlit_cockpit_contracts.py, models/tests/test_app.py | Gates pass or blocker logged. |
| WP-056-B | `cockpit-payload` | Build modular cockpit payloads from calibration, structural and VOI engines. | models/primarycare_model/ui/**, models/primarycare_model/app.py, docs/visualisation/visual-grammar-contract-v1.md, models/tests/test_streamlit_cockpit_contracts.py, models/tests/test_app.py | Gates pass or blocker logged. |
| WP-056-C | `app-integration` | Integrate cockpit surfaces without hiding existing public caveats. | models/primarycare_model/ui/**, models/primarycare_model/app.py, docs/visualisation/visual-grammar-contract-v1.md, models/tests/test_streamlit_cockpit_contracts.py, models/tests/test_app.py | Gates pass or blocker logged. |
| WP-056-D | `accessibility` | Validate table fallbacks, labels, contrast warnings and non-colour-only encodings. | models/primarycare_model/ui/**, models/primarycare_model/app.py, docs/visualisation/visual-grammar-contract-v1.md, models/tests/test_streamlit_cockpit_contracts.py, models/tests/test_app.py | Gates pass or blocker logged. |

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

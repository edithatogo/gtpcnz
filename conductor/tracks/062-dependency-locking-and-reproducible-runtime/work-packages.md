# Work Packages

Recommended Cline model: DeepSeek v4 Flash.

Parallelism policy:

- Run these packages in parallel only if their files do not overlap.
- Keep each package to one subagent and one level of delegation.
- Escalate to the coordinator for any cross-track edit.

| Work package | Subagent role | Task | Allowed files | Stop condition |
|---|---|---|---|---|
| WP-062-A | `lock-surface` | Keep pyproject, uv lock, Dockerfile and devcontainer present and consistent. | pyproject.toml, uv.lock, Dockerfile, .devcontainer/devcontainer.json, scripts/check_dependency_lock.py, models/tests/test_dependency_files.py, .github/workflows/dependency-edge.yml | Gates pass or blocker logged. |
| WP-062-B | `dependency-gate` | Fail when legacy requirements files return or dependency files referenced by workflows are absent. | pyproject.toml, uv.lock, Dockerfile, .devcontainer/devcontainer.json, scripts/check_dependency_lock.py, models/tests/test_dependency_files.py, .github/workflows/dependency-edge.yml | Gates pass or blocker logged. |
| WP-062-C | `edge-workflow` | Keep edge workflow non-blocking unless explicitly promoted and resolve it through uv prerelease mode. | pyproject.toml, uv.lock, Dockerfile, .devcontainer/devcontainer.json, scripts/check_dependency_lock.py, models/tests/test_dependency_files.py, .github/workflows/dependency-edge.yml | Gates pass or blocker logged. |
| WP-062-D | `runtime-docs` | Document reproducible local, CI and deployment runtime expectations. | pyproject.toml, uv.lock, Dockerfile, .devcontainer/devcontainer.json, scripts/check_dependency_lock.py, models/tests/test_dependency_files.py, .github/workflows/dependency-edge.yml | Gates pass or blocker logged. |

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

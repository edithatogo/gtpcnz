# Dependency-security maintenance — 13 November 2026

## Problem and scope

The existing Python 3.11 quality workflow failed its dependency audit with 106 reported vulnerabilities across 16 installed packages. Updating one dependency in each open PR did not repair that shared baseline.

This maintenance update refreshes the affected locked dependencies and their necessary resolution changes. It adds no audit ignores and leaves the quality thresholds and model behaviour intact. The Streamlit upgrade removes the vulnerable GitPython dependency; its AppTest API also requires test entrypoints to be resolved from the repository root instead of relying on the caller's working directory.

## Acceptance and evidence

- The frozen environment targets Python 3.11.18, matching CI's Python 3.11 lane.
- `uv sync --frozen --all-groups --python 3.11`: passed.
- `pip-audit`: passed with **no known vulnerabilities found** after the update.
- Ruff, basedpyright, strict mypy across 23 files, concern-boundary and patient-data checks: passed.
- Parameter-contract coverage gate: 3 tests passed, 98.61% coverage, above the existing 90% threshold.
- The initial full test run after the dependency upgrade: 340 passed and 6 failed. All six failures were AppTest paths resolving relative to the test module. Both test modules now use explicit repository-root paths.
- The complete test suite after that compatibility fix: **346 passed** in 129.46 seconds. The 265 warnings are existing Dash DataTable deprecation warnings; no test was skipped to make the suite pass.
- Conductor parallel-track contracts passed after the maintenance records were updated.
- Required hosted checks, merge and feature-branch pruning have **not** yet been verified.

## Boundaries and rollback

The change does not alter model inputs, calculations, public claims, calibration status, security exemptions or workflow permissions. Do not treat this dependency audit result as a source-code security audit or a guarantee against undisclosed vulnerabilities. Reverting this maintenance commit restores the previous lockfile and test paths, but also restores the dependency-audit failures.

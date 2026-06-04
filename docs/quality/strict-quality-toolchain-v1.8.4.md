# Strict Quality Toolchain

This repo now has a dedicated quality lane for strict typing, dependency maintenance, coverage, property tests, mutation testing, security scanning and profiling.

## Type Checking

The target posture is:

- `basedpyright` as the blocking strict type gate;
- `mypy --strict` as a blocking CI compatibility gate across contract, validation, and engine layers;
- `ty check` as a non-blocking canary until it is mature enough to promote.

## Dependency Automation

Dependabot remains configured. Renovate is configured through `renovate.json` and `.github/workflows/renovate.yml`. The workflow can run with `GITHUB_TOKEN`, but a `RENOVATE_TOKEN` repository secret is still preferred if Renovate needs to trigger follow-up workflows from its pull requests.

Renovate is pinned to the current v43 action line, while `actions/checkout@v6`, `actions/setup-python@v6`, and `github/codeql-action@v5` keep the GitHub Actions runtime on the Node 24 / current CodeQL surface.

## Test Quality

The CI quality lane targets:

- `pytest --cov-fail-under=90`;
- Hypothesis property tests for clamp, scoring, seeded stochastic replay and bounded outputs;
- `mutmut` mutation testing for pure runtime and scenario-service modules;
- `pip-audit` dependency vulnerability checks.

The coverage gate excludes Streamlit UI code, optional exploratory engine adapters, and optional Arrow/runtime-check modules until those surfaces are promoted into the blocking test boundary. The measured threshold is for the core model contracts, registries, runtime calculations and scenario service.

Local verification on 2026-05-28:

- `python scripts/dev_check.py` passed.
- Repo health score: 11/11.
- Bleeding-edge scorecard: 17/17.
- Full test suite: 134 passed.
- Coverage: 91.68% against `models.primarycare_model`.
- `ty check models/primarycare_model` remains a non-blocking canary and currently reports 17 diagnostics, mostly around Pandas row typing and optional adapter typing.

## Profiling

Scalene is configured through `requirements-dev.txt`, `.github/workflows/profiling.yml`, and `scripts/run_scalene_profile.py`.

Manual command:

```powershell
python -m scalene --cli --reduced-profile --profile-all scripts/run_scalene_profile.py
```

The target intentionally avoids Streamlit UI code and profiles pure runtime calculation paths.

On Windows, Scalene 2.3 may require Microsoft C++ Build Tools if no compatible wheel is available. The dev requirement is therefore Linux-only while the scheduled GitHub Actions profiling lane remains enabled.

## GitHub Security Settings

Repository-side settings checked on 2026-05-28:

- Dependabot alerts / vulnerability alerts: enabled.
- Dependabot security updates: enabled.
- Secret scanning: enabled.
- Secret scanning push protection: enabled.
- Secret scanning non-provider patterns and validity checks: unavailable or still disabled on the current public-repo plan/API response.
- Code scanning: configured by `.github/workflows/codeql.yml`; it will become active after the workflow lands on `main` and runs.
- Branch rulesets / required checks: active baseline repository ruleset `main baseline protection` is enabled for the default branch. It blocks branch deletion and force pushes, requires linear history, requires pull-request flow with resolved review threads, and requires both the existing `test-and-render` CI status check and the new `Quality / python-quality` status check with strict up-to-date checks.

CodeQL, mutation testing, profiling and Renovate are configured as scheduled/manual control lanes rather than every-PR blocking checks.

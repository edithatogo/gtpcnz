from __future__ import annotations

import json
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))


def read(path: str) -> str:
    return (ROOT / path).read_text(encoding="utf-8")


def exists(path: str) -> bool:
    return (ROOT / path).exists()


def run(command: list[str]) -> tuple[bool, str]:
    completed = subprocess.run(command, cwd=ROOT, text=True, capture_output=True)
    output = "\n".join(part for part in [completed.stdout, completed.stderr] if part).strip()
    if completed.returncode == 0:
        return True, output.splitlines()[-1] if output else "passed"
    return False, "\n".join(output.splitlines()[-20:])


def check_identity() -> tuple[bool, str]:
    canonical = {
        "repo": "edithatogo/gtpcnz",
        "pages": "https://edithatogo.github.io/gtpcnz/",
        "streamlit": "https://gtpcnz.streamlit.app/",
    }
    paths = ["README.md", "_quarto.yml", "index.qmd", "docs/STREAMLIT-DEPLOYMENT.md", "docs/REPORTS-AND-DASHBOARD.md"]
    missing_paths = [path for path in paths if not exists(path)]
    if missing_paths:
        return False, f"identity files missing: {missing_paths}"
    combined = "\n".join(read(path) for path in paths)
    missing = [value for value in canonical.values() if value not in combined]
    stale = [
        "edithatogo/primary-care-funding-architecture",
        "https://edithatogo.github.io/primary-care-funding-architecture/",
        "https://primary-care-funding-architecture.streamlit.app/",
    ]
    stale_found = [value for value in stale if value in combined]
    if missing or stale_found:
        return False, f"identity mismatch: missing={missing}, stale={stale_found}"
    return True, "canonical gtpcnz repo, Pages and Streamlit identity is consistent"


def check_conductor_assets() -> tuple[bool, str]:
    required = [
        "conductor/README.md",
        "conductor/templates/repo-hygiene-track-template.md",
        "conductor/templates/streamlit-dashboard-track-template.md",
        "conductor/templates/dependency-edge-track-template.md",
        "conductor/templates/release-publish-track-template.md",
        "conductor/agents/repo-hygiene-agent.md",
        "conductor/agents/dashboard-claims-agent.md",
        "conductor/agents/github-release-agent.md",
        "conductor/agents/dependency-edge-agent.md",
        "conductor/skills/repo-hygiene-skill.md",
        "conductor/skills/dashboard-claims-skill.md",
        "conductor/workflows/repo-hygiene.md",
        "conductor/workflows/branch-publish.md",
        "conductor/workflows/streamlit-dashboard-check.md",
        "conductor/workflows/dependency-edge-check.md",
        "conductor/tracks/043-concern-extraction-strict-validation_20260526/spec.md",
        "conductor/tracks/043-concern-extraction-strict-validation_20260526/plan.md",
    ]
    missing = [path for path in required if not exists(path)]
    if missing:
        return False, f"Conductor assets missing: {missing}"
    return True, "Conductor templates, agents, skills, workflows and active strict-validation track are present"


def check_contract_registries() -> tuple[bool, str]:
    required = [
        "models/primarycare_model/contracts/parameters.py",
        "models/primarycare_model/contracts/inputs.py",
        "models/primarycare_model/contracts/scenarios.py",
        "models/primarycare_model/contracts/results.py",
        "models/primarycare_model/contracts/engine.py",
        "models/primarycare_model/registries/educational_levers.v1.yaml",
        "models/primarycare_model/registries/scenarios.v1.yaml",
        "models/primarycare_model/validation/registry_loader.py",
        "models/primarycare_model/validation/pandera_schemas.py",
    ]
    missing = [path for path in required if not exists(path)]
    if missing:
        return False, f"contract/registry surface missing: {missing}"
    text = read("models/primarycare_model/validation/registry_loader.py")
    if "load_educational_levers_registry" not in text or "educational_levers.v1.yaml" not in text:
        return False, "educational lever registry loader is not the primary API"
    return True, "typed contracts, versioned registries and validation helpers are present"


def check_streamlit_boundary() -> tuple[bool, str]:
    required = ["streamlit_app.py", "models/primarycare_model/app.py", ".streamlit/config.toml", ".streamlit/secrets.toml.example"]
    missing = [path for path in required if not exists(path)]
    if missing:
        return False, f"Streamlit surface missing: {missing}"
    config = read(".streamlit/config.toml")
    if "gatherUsageStats = false" not in config or "headless = true" not in config:
        return False, "Streamlit config must be headless and telemetry-minimised"
    app_text = read("models/primarycare_model/app.py").lower()
    if "toy" in app_text or "primary-care-funding-architecture.streamlit.app" in app_text:
        return False, "public Streamlit surface contains stale wording or URL"
    return True, "Streamlit public surface is deployable, canonical and public-claim bounded"


def check_docs() -> tuple[bool, str]:
    required = [
        "docs/requirements-moscow-v1.8.3.md",
        "docs/design/repo-github-streamlit-design-v1.8.3.md",
        "docs/contracts/repo-github-streamlit-contracts-v1.8.3.md",
        "docs/dependency-policy-v1.8.3.md",
        "docs/bleeding-edge-scorecard-v1.0.md",
        "conductor/state.md",
    ]
    missing = [path for path in required if not exists(path)]
    if missing:
        return False, f"documentation/control files missing: {missing}"
    design = read("docs/design/repo-github-streamlit-design-v1.8.3.md")
    if len(re.findall(r"```mermaid", design)) < 4:
        return False, "design file needs Mermaid architecture diagrams"
    contracts = read("docs/contracts/repo-github-streamlit-contracts-v1.8.3.md")
    if "CON-001" not in contracts or "REQ-001" not in contracts:
        return False, "contract traceability IDs are missing"
    return True, "requirements, design, contracts, dependency policy, scorecard and state docs are present"


def check_ci() -> tuple[bool, str]:
    required = [
        ".github/workflows/ci.yml",
        ".github/workflows/pages.yml",
        ".github/workflows/dependency-canary.yml",
        ".github/dependabot.yml",
    ]
    missing = [path for path in required if not exists(path)]
    if missing:
        return False, f"GitHub automation missing: {missing}"
    ci = read(".github/workflows/ci.yml")
    required_ci = [
        "python scripts/check_repo_health.py",
        "python scripts/check_concern_boundaries.py",
        "python scripts/check_public_source_retrieval_plan.py",
        "python scripts/check_public_source_fetch_scripts.py",
        "python scripts/check_public_source_transform_scripts.py",
        "python scripts/check_public_source_readiness_matrix.py",
        "python scripts/check_transformed_schemas.py",
        "python scripts/check_calibration_target_readiness.py",
        "python scripts/check_calibration_validation_gates.py",
        "python scripts/check_posterior_predictive_checks.py",
        "pytest -q",
        "quarto render --to html",
        "py_compile streamlit_app.py models/primarycare_model/app.py",
    ]
    missing_ci = [item for item in required_ci if item not in ci]
    if missing_ci:
        return False, f"CI missing gates: {missing_ci}"
    canary = read(".github/workflows/dependency-canary.yml")
    if "--upgrade --upgrade-strategy eager -r requirements.txt" not in canary:
        return False, "dependency canary does not run latest-compatible pip lane"
    return True, "CI, Pages, Dependabot and dependency canary gates are configured"


def check_tests() -> tuple[bool, str]:
    required = [
        "models/tests/test_app.py",
        "models/tests/test_dashboard_claims.py",
        "models/tests/test_scenario_service.py",
        "models/tests/test_runtime_lab.py",
        "models/tests/test_conductor_assets.py",
        "models/tests/test_contract_registries.py",
    ]
    missing = [path for path in required if not exists(path)]
    if missing:
        return False, f"test surface missing: {missing}"
    pyproject = read("pyproject.toml")
    if 'testpaths = ["models/tests"]' not in pyproject or '"public"' not in pyproject:
        return False, "pytest collection guard is incomplete"
    return True, "focused model, dashboard, Conductor and registry tests are present"


def check_no_stub_modules() -> tuple[bool, str]:
    forbidden = [
        "models/primarycare_model/abm_stub.py",
        "models/primarycare_model/sd_stub.py",
    ]
    present = [path for path in forbidden if exists(path)]
    if present:
        return False, f"stub modules remain: {present}"
    return True, "tracked ABM/SD stub modules are absent"


def check_claim_boundaries() -> tuple[bool, str]:
    required_paths = ["README.md", "docs/calibration/model-card-v1.7.2.md", "docs/launch/claim-boundaries-v1.7.2.md", "conductor/state.md"]
    missing = [path for path in required_paths if not exists(path)]
    if missing:
        return False, f"claim-boundary evidence missing: {missing}"
    combined = "\n".join(read(path).lower() for path in required_paths)
    required = ["public-data anchored", "linked-data", "patient-level forecast"]
    missing_phrases = [phrase for phrase in required if phrase not in combined]
    if missing_phrases:
        return False, f"claim-boundary phrases missing: {missing_phrases}"
    return True, "public-data, linked-data and patient-level forecast boundaries remain explicit"


def check_concern_boundaries_execute() -> tuple[bool, str]:
    return run([sys.executable, "scripts/check_concern_boundaries.py"])


def check_tests_execute() -> tuple[bool, str]:
    return run([sys.executable, "-m", "pytest", "-q", "-p", "no:cacheprovider", "models/tests"])


CHECKS = [
    ("canonical_identity", check_identity),
    ("conductor_assets", check_conductor_assets),
    ("contract_registries", check_contract_registries),
    ("streamlit_boundary", check_streamlit_boundary),
    ("documentation_controls", check_docs),
    ("github_automation", check_ci),
    ("test_surface", check_tests),
    ("no_stub_modules", check_no_stub_modules),
    ("claim_boundaries", check_claim_boundaries),
    ("concern_boundaries_execute", check_concern_boundaries_execute),
    ("regression_tests_execute", check_tests_execute),
]


def main() -> int:
    from repo_scorecards import bleeding_edge_scorecard

    results = []
    for name, check in CHECKS:
        ok, detail = check()
        results.append({"name": name, "ok": ok, "detail": detail})

    score = sum(1 for result in results if result["ok"])
    payload = {
        "score": score,
        "max_score": len(CHECKS),
        "repo_health_percent": round(score / len(CHECKS) * 100, 1),
        "results": results,
        "supplemental": {"bleeding_edge_scorecard": bleeding_edge_scorecard()},
    }
    print(json.dumps(payload, indent=2))
    return 0 if score == len(CHECKS) else 1


if __name__ == "__main__":
    raise SystemExit(main())

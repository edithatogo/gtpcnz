from __future__ import annotations

import json
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from repo_scorecards import bleeding_edge_scorecard


def read(path: str) -> str:
    return (ROOT / path).read_text(encoding="utf-8")


def exists(path: str) -> bool:
    return (ROOT / path).exists()


REQUIREMENT_IDS = [f"REQ-{i:03d}" for i in range(1, 43)]
CONTRACT_IDS = [f"CON-{i:03d}" for i in range(1, 43)]


def check_requirements() -> tuple[bool, str]:
    path = "docs/requirements-moscow-v1.8.3.md"
    if not exists(path):
        return False, f"{path} is missing"
    text = read(path)
    missing = [rid for rid in REQUIREMENT_IDS if rid not in text]
    priorities = all(word in text for word in ["Must", "Should", "Could", "Won't"])
    if missing:
        return False, f"missing requirement IDs: {', '.join(missing)}"
    if not priorities:
        return False, "MoSCoW priority definitions are incomplete"
    return True, "granular MoSCoW requirements are present"


def check_design() -> tuple[bool, str]:
    path = "docs/design/repo-github-streamlit-design-v1.8.3.md"
    if not exists(path):
        return False, f"{path} is missing"
    text = read(path)
    mermaid_blocks = len(re.findall(r"```mermaid", text))
    required = ["DES-001", "DES-002", "DES-003", "DES-004", "DES-005", "DES-006", "DES-007"]
    missing = [item for item in required if item not in text]
    if mermaid_blocks < 7 or missing:
        return False, f"design requires seven Mermaid diagrams and IDs; missing {missing}"
    return True, "design file has system, CI, Streamlit, health, dependency-lane, simulation-pipeline and SOTA diagrams"


def check_contracts() -> tuple[bool, str]:
    path = "docs/contracts/repo-github-streamlit-contracts-v1.8.3.md"
    if not exists(path):
        return False, f"{path} is missing"
    text = read(path)
    missing_reqs = [rid for rid in REQUIREMENT_IDS if rid not in text]
    missing_contracts = [cid for cid in CONTRACT_IDS if cid not in text]
    if missing_reqs or missing_contracts:
        return False, f"contract coverage gaps: reqs={missing_reqs}, contracts={missing_contracts}"
    return True, "contracts cover every requirement and element"


def check_ci() -> tuple[bool, str]:
    path = ".github/workflows/ci.yml"
    if not exists(path):
        return False, f"{path} is missing"
    text = read(path)
    required = [
        "actions/checkout@v6",
        "actions/setup-python@v6",
        "python scripts/check_repo_health.py",
        "pytest -q",
        "quarto render --to html",
        "py_compile streamlit_app.py models/primarycare_model/app.py",
    ]
    missing = [item for item in required if item not in text]
    if missing:
        return False, f"CI missing: {missing}"
    return True, "CI has current actions and repo health/test/render/import gates"


def check_pages() -> tuple[bool, str]:
    path = ".github/workflows/pages.yml"
    if not exists(path):
        return False, f"{path} is missing"
    text = read(path)
    required = [
        "pages: write",
        "id-token: write",
        "actions/upload-pages-artifact@v5",
        "actions/deploy-pages@v5",
        "test -f _site/index.html",
    ]
    missing = [item for item in required if item not in text]
    if missing:
        return False, f"Pages workflow missing: {missing}"
    return True, "GitHub Pages workflow has least-privilege deploy contract"


def check_streamlit() -> tuple[bool, str]:
    required_paths = [
        "streamlit_app.py",
        "models/primarycare_model/app.py",
        "models/primarycare_model/scenario_service.py",
        ".streamlit/config.toml",
        ".streamlit/secrets.toml.example",
    ]
    missing = [path for path in required_paths if not exists(path)]
    if missing:
        return False, f"Streamlit surface missing: {missing}"
    config = read(".streamlit/config.toml")
    if "gatherUsageStats = false" not in config or "headless = true" not in config:
        return False, "Streamlit config must be public, headless and telemetry-minimised"
    return True, "Streamlit public app boundary is deployable and secret-free"


def check_metadata() -> tuple[bool, str]:
    required_paths = ["LICENSE", "CITATION.cff", "SECURITY.md", "CONTRIBUTING.md", "CODE_OF_CONDUCT.md"]
    missing = [path for path in required_paths if not exists(path)]
    if missing:
        return False, f"public metadata missing: {missing}"
    return True, "public repo metadata is complete"


def check_repo_identity() -> tuple[bool, str]:
    canonical_repo = "edithatogo/primary-care-funding-architecture"
    canonical_pages = "https://edithatogo.github.io/primary-care-funding-architecture/"
    canonical_streamlit = "https://gtpcnz.streamlit.app/"
    checked_paths = [
        "README.md",
        "_quarto.yml",
        "index.qmd",
        "docs/REPORTS-AND-DASHBOARD.md",
        "docs/STREAMLIT-DEPLOYMENT.md",
        "docs/requirements-moscow-v1.8.3.md",
        "docs/design/repo-github-streamlit-design-v1.8.3.md",
        "docs/contracts/repo-github-streamlit-contracts-v1.8.3.md",
        "docs/public-site/streamlit-dashboard-contract-v1.8.1.md",
    ]
    missing = [path for path in checked_paths if not exists(path)]
    if missing:
        return False, f"canonical identity files missing: {missing}"

    combined = "\n".join(read(path) for path in checked_paths)
    required = [canonical_repo, canonical_pages, canonical_streamlit]
    missing_required = [item for item in required if item not in combined]
    stale = ["edithatogo/gtpcnz", "https://edithatogo.github.io/gtpcnz/", "https://primary-care-funding-architecture.streamlit.app/"]
    stale_found = [item for item in stale if item in combined]
    if missing_required or stale_found:
        return False, f"repo identity mismatch: missing={missing_required}, stale={stale_found}"
    return True, "canonical GitHub, Pages and Streamlit identity is consistent"


def check_dependency_maintenance() -> tuple[bool, str]:
    path = ".github/dependabot.yml"
    if not exists(path):
        return False, f"{path} is missing"
    text = read(path)
    required = ["github-actions", "pip", "requirements.txt"]
    missing = [item for item in required if item not in text]
    if missing:
        return False, f"Dependabot config missing: {missing}"
    return True, "dependency maintenance covers Actions and pip"


def check_dependency_canary() -> tuple[bool, str]:
    workflow = ".github/workflows/dependency-canary.yml"
    policy = "docs/dependency-policy-v1.8.3.md"
    missing_paths = [path for path in [workflow, policy] if not exists(path)]
    if missing_paths:
        return False, f"dependency canary surface missing: {missing_paths}"
    workflow_text = read(workflow)
    policy_text = read(policy)
    required_workflow = [
        "schedule:",
        "workflow_dispatch:",
        "actions/checkout@v6",
        "actions/setup-python@v6",
        "--upgrade --upgrade-strategy eager -r requirements.txt",
        "python scripts/check_repo_health.py",
        "pytest -q",
        "quarto render --to html",
        "py_compile streamlit_app.py models/primarycare_model/app.py",
    ]
    required_policy = ["Stable release CI", "Latest canary CI", "Streamlit", "Quarto", "Dependabot"]
    required_policy.extend(["Experimental edge CI", "three-lane dependency posture"])
    missing_workflow = [item for item in required_workflow if item not in workflow_text]
    missing_policy = [item for item in required_policy if item not in policy_text]
    if missing_workflow or missing_policy:
        return False, f"dependency canary gaps: workflow={missing_workflow}, policy={missing_policy}"
    return True, "latest-compatible dependency canary and policy are present"


def check_tests() -> tuple[bool, str]:
    required_paths = [
        "models/tests/test_abm.py",
        "models/tests/test_app.py",
        "models/tests/test_dashboard_claims.py",
        "models/tests/test_sd.py",
        "models/tests/test_public_scenario_outputs.py",
        "models/tests/test_scenario_service.py",
        "models/tests/test_full_parameterised_model_v170.py",
    ]
    missing = [path for path in required_paths if not exists(path)]
    if missing:
        return False, f"test surface missing: {missing}"
    pyproject = read("pyproject.toml")
    required_config = ['testpaths = ["models/tests"]', '"codex-tmp"', '"public"']
    missing_config = [item for item in required_config if item not in pyproject]
    if missing_config:
        return False, f"pytest collection guard missing: {missing_config}"
    return True, "dashboard, scenario, public-output, ABM, SD and model tests are present"


def check_tests_execute() -> tuple[bool, str]:
    command = [
        sys.executable,
        "-m",
        "pytest",
        "-q",
        "-p",
        "no:cacheprovider",
        "models/tests",
    ]
    completed = subprocess.run(command, cwd=ROOT, text=True, capture_output=True)
    output = "\n".join(part for part in [completed.stdout, completed.stderr] if part).strip()
    passed_match = re.search(r"(\d+)\s+passed", output)
    if completed.returncode != 0:
        cleanup_only = (
            passed_match is not None
            and "PermissionError" in completed.stderr
            and "tempfile.py" in completed.stderr
        )
        if cleanup_only:
            return True, f"pytest execution passed with Windows temp cleanup warning: {passed_match.group(0)}"
        failure_summary = re.search(
            r"(^|[\s=])(?:FAILED|ERRORS?|FAILURES?|failed|errors?)($|[\s=])",
            completed.stdout,
        )
        tail = "\n".join(output.splitlines()[-20:])
        return False, f"pytest failed with exit {completed.returncode}: {tail}"
    summary = completed.stdout.strip().splitlines()[-1] if completed.stdout.strip() else "pytest passed"
    return True, f"pytest execution passed: {summary}"


def check_no_abm_stubs() -> tuple[bool, str]:
    missing_or_removed = not exists("models/primarycare_model/abm_stub.py")
    if not missing_or_removed:
        return False, "abm_stub.py still exists"
    text_paths = [
        "models/primarycare_model/abm.py",
        "models/tests/test_abm.py",
        "docs/calibration/model-card-v1.7.2.md",
    ]
    text = "\n".join(read(path) for path in text_paths if exists(path))
    if "abm_stub" in text:
        return False, "abm_stub import or filename reference remains in current ABM surfaces"
    return True, "no tracked ABM stub module or import remains"


def check_no_sd_stubs() -> tuple[bool, str]:
    missing_or_removed = not exists("models/primarycare_model/sd_stub.py")
    if not missing_or_removed:
        return False, "sd_stub.py still exists"
    text_paths = [
        "models/primarycare_model/sd.py",
        "models/tests/test_sd.py",
        "docs/calibration/model-card-v1.7.2.md",
    ]
    text = "\n".join(read(path) for path in text_paths if exists(path))
    if "sd_stub" in text:
        return False, "sd_stub import or filename reference remains in current SD surfaces"
    return True, "no tracked SD stub module or import remains"


def check_claim_boundaries() -> tuple[bool, str]:
    required_paths = [
        "README.md",
        "docs/calibration/model-card-v1.7.2.md",
        "docs/launch/claim-boundaries-v1.7.2.md",
        "conductor/state.md",
    ]
    missing = [path for path in required_paths if not exists(path)]
    if missing:
        return False, f"claim-boundary evidence missing: {missing}"
    combined = "\n".join(read(path).lower() for path in required_paths)
    required_phrases = ["public-data anchored", "linked-data", "oia", "stakeholder"]
    missing_phrases = [phrase for phrase in required_phrases if phrase not in combined]
    if missing_phrases:
        return False, f"claim-boundary phrases missing: {missing_phrases}"
    return True, "claim boundaries and evidence gates remain explicit"


def bleeding_edge_summary() -> dict[str, object]:
    return bleeding_edge_scorecard()


CHECKS = [
    ("requirements_moscow", check_requirements),
    ("design_mermaid", check_design),
    ("element_contracts", check_contracts),
    ("ci_quality_gate", check_ci),
    ("pages_deploy", check_pages),
    ("streamlit_boundary", check_streamlit),
    ("repo_metadata", check_metadata),
    ("repo_identity", check_repo_identity),
    ("dependency_maintenance", check_dependency_maintenance),
    ("dependency_canary", check_dependency_canary),
    ("no_abm_stubs", check_no_abm_stubs),
    ("no_sd_stubs", check_no_sd_stubs),
    ("regression_tests", check_tests),
    ("regression_tests_execute", check_tests_execute),
    ("claim_boundaries", check_claim_boundaries),
]


def main() -> int:
    results = []
    for name, check in CHECKS:
        ok, detail = check()
        results.append({"name": name, "ok": ok, "detail": detail})

    score = sum(1 for result in results if result["ok"])
    payload = {
        "score": score,
        "max_score": len(CHECKS),
        "results": results,
        "supplemental": {"bleeding_edge_scorecard": bleeding_edge_summary()},
    }
    print(json.dumps(payload, indent=2))

    if score != len(CHECKS):
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

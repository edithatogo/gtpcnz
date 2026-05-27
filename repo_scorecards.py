from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parent


def _exists(path: str) -> bool:
    return (ROOT / path).exists()


def bleeding_edge_scorecard() -> dict[str, object]:
    """Return a reproducible score for the repo's edge-readiness posture."""

    checks = [
        ("python_runtime", "Python >=3.11 project metadata", "pyproject.toml", _exists("pyproject.toml")),
        ("streamlit_native_tests", "Streamlit AppTest coverage", "models/tests/test_app.py", _exists("models/tests/test_app.py")),
        ("contract_registries", "Pydantic contracts plus versioned YAML registries", "models/primarycare_model/contracts", _exists("models/primarycare_model/contracts")),
        ("validation_boundaries", "Concern-boundary scanner", "scripts/check_concern_boundaries.py", _exists("scripts/check_concern_boundaries.py")),
        ("conductor_workflows", "Conductor templates, agents, skills and workflows", "conductor/workflows", _exists("conductor/workflows")),
        ("ci_release_lane", "Main PR CI gate", ".github/workflows/ci.yml", _exists(".github/workflows/ci.yml")),
        ("dependency_canary", "Latest-compatible dependency canary lane", ".github/workflows/dependency-canary.yml", _exists(".github/workflows/dependency-canary.yml")),
        ("pages_deploy", "GitHub Pages deployment workflow", ".github/workflows/pages.yml", _exists(".github/workflows/pages.yml")),
        ("dependabot", "Automated dependency maintenance", ".github/dependabot.yml", _exists(".github/dependabot.yml")),
        ("public_claim_controls", "Claim-boundary and model-card docs", "docs/launch/claim-boundaries-v1.7.2.md", _exists("docs/launch/claim-boundaries-v1.7.2.md")),
    ]
    passed = sum(1 for _, _, _, ok in checks if ok)
    return {
        "score": passed,
        "max_score": len(checks),
        "percent": round(passed / len(checks) * 100, 1),
        "posture": "bleeding-edge controlled" if passed == len(checks) else "needs hardening",
        "checks": [
            {"id": item_id, "label": label, "evidence": evidence, "ok": ok}
            for item_id, label, evidence, ok in checks
        ],
    }

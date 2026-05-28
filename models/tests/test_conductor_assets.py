from pathlib import Path

ROOT = Path("conductor")


REQUIRED_ASSETS = [
    "README.md",
    "templates/repo-hygiene-track-template.md",
    "templates/streamlit-dashboard-track-template.md",
    "templates/dependency-edge-track-template.md",
    "templates/release-publish-track-template.md",
    "agents/repo-hygiene-agent.md",
    "agents/dashboard-claims-agent.md",
    "agents/github-release-agent.md",
    "agents/dependency-edge-agent.md",
    "skills/repo-hygiene-skill.md",
    "skills/dashboard-claims-skill.md",
    "workflows/repo-hygiene.md",
    "workflows/branch-publish.md",
    "workflows/streamlit-dashboard-check.md",
    "workflows/dependency-edge-check.md",
]


def test_conductor_operations_assets_exist():
    missing = [path for path in REQUIRED_ASSETS if not (ROOT / path).exists()]
    assert missing == []


def test_repo_hygiene_template_has_safety_gates():
    text = (ROOT / "templates/repo-hygiene-track-template.md").read_text(encoding="utf-8")
    required = [
        "git status -sb",
        "git remote -v",
        "python -m pytest",
        "python scripts/check_repo_health.py",
        "Do not delete untracked files",
        "Do not reset",
    ]
    missing = [item for item in required if item not in text]
    assert missing == []


def test_dashboard_skill_requires_units_and_claim_boundaries():
    text = (ROOT / "skills/dashboard-claims-skill.md").read_text(encoding="utf-8")
    required = [
        "Policy-strength controls",
        "Model-generated indices",
        "illustrative NZD",
        "percent share of need met",
        "public-data anchored benchmark caveat",
    ]
    missing = [item for item in required if item not in text]
    assert missing == []


def test_publish_workflow_protects_main_and_remote_identity():
    text = (ROOT / "workflows/branch-publish.md").read_text(encoding="utf-8")
    required = [
        "git remote -v",
        "origin/main",
        "git push -u origin <branch>",
        "no unique commits",
    ]
    missing = [item for item in required if item not in text]
    assert missing == []

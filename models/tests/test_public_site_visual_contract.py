from pathlib import Path


CANONICAL_STREAMLIT_URL = "https://gtpcnz.streamlit.app/"
REPORT_LINK = "reports/primary_care_architecture.qmd"
PUBLIC_INDEX = Path(__file__).resolve().parents[2] / "index.qmd"

REQUIRED_STRINGS = [
    "Visual reading map",
    "GTPCNZ visual gallery",
    "Read the public report",
    "Open the dashboard",
    "Read the dashboard guide",
    "This is a source-informed parameterised scaffold and educational explainer.",
    "not a real-data calibrated forecast",
    "should not be used to claim precise fiscal savings, hospital-demand reductions, workforce effects, or implementation impacts.",
    "Argument map and thesis",
    "Current reform pathway",
    "Scenario rank chart",
    "Evidence tracker",
    "Calibration readiness",
    "First six launch posts",
    "Game-theory extension",
    "Later game-theory modules",
    "Public surfaces",
    "Public report",
    "Streamlit dashboard",
    "Model card and tracker",
    "Calibration readiness page",
    "Uncapped does not mean uncontrolled; it means scheduled, rules-based, audited, clinically governed and place-accountable.",
]

FIRST_SIX_TITLES = [
    "01. Are we buying hospital growth by rationing cheaper care upstream?",
    "02. Fee-for-service, capitation and blended funding",
    "03. Marginal supply",
    "04. Why formulas do not solve games",
    "05. Current reform pathway",
    "06. What I mean by uncapping primary care funding",
]

STATUS_LABELS = [
    "Conceptual",
    "Toy",
    "Model-generated index",
    "Evidence readiness",
    "Calibration readiness",
]

FORBIDDEN_SNIPPETS = [
    "OneDrive",
    "C:\\Users",
    "C:/Users",
    "substack-ready",
    "private draft",
    "working draft",
    "local filesystem",
]


def read_index() -> str:
    return PUBLIC_INDEX.read_text(encoding="utf-8")


def test_public_homepage_visual_contract_strings():
    text = read_index()

    for snippet in REQUIRED_STRINGS:
        assert snippet in text

    for title in FIRST_SIX_TITLES:
        assert title in text

    for label in STATUS_LABELS:
        assert label in text

    assert REPORT_LINK in text
    assert CANONICAL_STREAMLIT_URL in text
    assert 'href="reports/primary_care_architecture.qmd"' in text
    assert 'href="https://gtpcnz.streamlit.app/"' in text


def test_public_homepage_has_no_private_substack_or_local_paths():
    text = read_index()

    for snippet in FORBIDDEN_SNIPPETS:
        assert snippet not in text

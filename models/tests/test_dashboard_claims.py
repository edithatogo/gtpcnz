from pathlib import Path

CANONICAL_STREAMLIT_URL = "https://gtpcnz.streamlit.app/"
FULL_CAVEAT = (
    "This is a source-informed parameterised scaffold and educational explainer. "
    "It is not a real-data calibrated forecast and should not be used to claim "
    "precise fiscal savings, hospital-demand reductions, workforce effects, or implementation impacts."
)


def test_dashboard_uses_explainer_and_not_forecast_language():
    text = Path("models/primarycare_model/app.py").read_text(encoding="utf-8")
    assert "Funding Architecture Explainer" in text
    assert "not a real-data calibrated forecast" in text
    assert "toy" in text.lower()
    assert "not a calibrated prediction" in text.lower()
    assert "use_container_width" not in text
    assert "How to read this dashboard" in text
    assert "Interpretation rules" in text
    assert "What the reference scenarios mean" in text
    assert "What the toy sliders are for" in text
    assert "What would need to happen next" in text
    assert "Do not convert index differences into dollars saved" in text
    assert "Current state of the policy problem and the project" in text
    assert "Current New Zealand reform pathway used as the comparator" in text
    assert "How the public explainer fits together" in text
    assert "Public project status" in text
    assert "Where the project is mature versus still early" in text
    assert "not an empirical performance result" in text


def test_public_report_has_claim_boundaries():
    text = Path("reports/primary_care_architecture.qmd").read_text(encoding="utf-8")
    assert "Source-confidence label" in text
    assert FULL_CAVEAT in text
    assert "current reform pathway" in text.lower()
    assert "Uncapped does not mean uncontrolled" in text


def test_public_surfaces_include_canonical_streamlit_url_and_full_caveat():
    for path in [
        Path("README.md"),
        Path("index.qmd"),
        Path("docs/REPORTS-AND-DASHBOARD.md"),
        Path("docs/STREAMLIT-DEPLOYMENT.md"),
    ]:
        text = path.read_text(encoding="utf-8")
        assert CANONICAL_STREAMLIT_URL in text

    for path in [
        Path("README.md"),
        Path("index.qmd"),
        Path("docs/REPORTS-AND-DASHBOARD.md"),
        Path("docs/STREAMLIT-DEPLOYMENT.md"),
        Path("reports/primary_care_architecture.qmd"),
    ]:
        text = path.read_text(encoding="utf-8")
        assert "implementation impacts" in text
        assert "not a real-data calibrated forecast" in text


def test_quarto_renders_model_card_and_claim_boundaries():
    text = Path("_quarto.yml").read_text(encoding="utf-8")
    assert "docs/calibration/model-card-v1.7.2.md" in text
    assert "docs/launch/claim-boundaries-v1.7.2.md" in text
    assert "docs/public-site/evidence-tracker-public-v1.8.1.md" in text
    assert "docs/public-site/calibration-readiness-page-v1.8.1.md" in text

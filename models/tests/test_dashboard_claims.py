from pathlib import Path


def test_dashboard_uses_explainer_and_not_forecast_language():
    text = Path("models/primarycare_model/app.py").read_text(encoding="utf-8")
    assert "Funding Architecture Explainer" in text
    assert "not a real-data calibrated forecast" in text
    assert "toy" in text.lower()
    assert "not a calibrated prediction" in text.lower()


def test_public_report_has_claim_boundaries():
    text = Path("reports/primary_care_architecture.qmd").read_text(encoding="utf-8")
    assert "Source-confidence label" in text
    assert "not a real-data calibrated forecast" in text
    assert "current reform pathway" in text.lower()
    assert "Uncapped does not mean uncontrolled" in text


def test_quarto_renders_model_card_and_claim_boundaries():
    text = Path("_quarto.yml").read_text(encoding="utf-8")
    assert "docs/calibration/model-card-v1.7.2.md" in text
    assert "docs/launch/claim-boundaries-v1.7.2.md" in text
    assert "docs/public-site/evidence-tracker-public-v1.8.1.md" in text
    assert "docs/public-site/calibration-readiness-page-v1.8.1.md" in text

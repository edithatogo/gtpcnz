from pathlib import Path


def test_public_report_has_track_032_post_crosswalk():
    text = Path("reports/primary_care_architecture.qmd").read_text(encoding="utf-8")

    assert "How the posts map to this report and dashboard" in text
    for anchor in range(1, 7):
        assert f"#post-0{anchor}" in text

    assert "Post 01. Are we buying hospital growth by rationing cheaper care upstream?" in text
    assert "Post 02. Fee-for-service, capitation and blended funding" in text
    assert "Post 03. Marginal supply" in text
    assert "Post 04. Why formulas do not solve games" in text
    assert "Post 05. Current reform pathway" in text
    assert "Post 06. What I mean by uncapping primary care funding" in text

    assert "game theory and controls" in text.lower()
    assert "payoff matrix" in text.lower()
    assert "best-response loop and controls stack" in text.lower()

    assert "Post 03 diagram 1. Marginal supply threshold" in text
    assert "Post 04 diagram 1. Qualitative payoff matrix for the primary-care incentive game." in text
    assert "Post 04 diagram 2. Best-response loop and controls stack." in text
    assert "Post 06 diagram 1. Controlled uncapping threshold" in text

    assert "current reform pathway" in text.lower()
    assert "F0/current reform remains the comparator" in text
    assert "model-generated index" in text.lower()

    assert text.count("Accessibility description:") >= 6
    assert text.count("Source-confidence label:") >= 7

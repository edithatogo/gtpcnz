from pathlib import Path

from streamlit.testing.v1 import AppTest


SOURCE_PATH = Path(__file__).resolve().parents[1] / "primarycare_model" / "app.py"
APP_PATH = str(SOURCE_PATH)


def _load_app() -> AppTest:
    at = AppTest.from_file(APP_PATH, default_timeout=30)
    at.run()
    assert not at.exception
    return at


def _source_text() -> str:
    return SOURCE_PATH.read_text(encoding="utf-8")


def test_app_smokes_after_post_labs_update():
    _load_app()


def test_post_guide_and_reading_map_are_defined_in_source():
    text = _source_text()

    assert "Post guide / Reading map" in text
    assert "Quarto / report destination" in text
    assert "GitHub Pages card" in text
    assert "Static visual" in text
    assert "Dynamic visual" in text
    assert "01" in text
    assert "02" in text
    assert "03" in text
    assert "04" in text
    assert "05" in text
    assert "06" in text
    assert "Are we buying hospital growth by rationing cheaper care upstream?" in text
    assert "Fee-for-service, capitation and blended funding" in text
    assert "Marginal supply" in text
    assert "Why formulas do not solve games" in text
    assert "Current reform pathway" in text
    assert "What I mean by uncapping primary care funding" in text
    assert "F0` is the current reform pathway used as the baseline" in text
    assert "model-generated indices" in text
    assert "toy teaching simulations" in text
    assert "Microeconomics lab" in text
    assert "Game theory lab" in text


def test_microeconomics_lab_sliders_are_defined_in_source():
    text = _source_text()

    assert "render_microeconomics_lab" in text
    assert "Microeconomics lab 1: marginal supply" in text
    assert "Microeconomics lab 2: capitation budget constraint" in text
    assert "Microeconomics lab 3: scheduled activity payment" in text
    assert "Microeconomics lab 4: co-payment / access barrier" in text
    assert "Marginal payment signal" in text
    assert "Baseline appointment capacity" in text
    assert "Response responsiveness" in text
    assert "Administrative friction" in text
    assert "Enrolled patients" in text
    assert "Capitation rate per enrolled patient" in text
    assert "Expected cost per patient" in text
    assert "Demand growth pressure" in text
    assert "Eligible activity units" in text
    assert "Scheduled payment rate" in text
    assert "Control strength" in text
    assert "Scope flexibility" in text
    assert "Co-payment" in text
    assert "Local in-person care capacity" in text
    assert "Digital access reach" in text
    assert "Equity protection" in text
    assert "Travel and geography friction" in text


def test_game_theory_lab_sliders_are_defined_in_source():
    text = _source_text()

    assert "render_game_theory_lab" in text
    assert "Game theory lab 1: formulas do not solve games" in text
    assert "Game theory lab 2: payoff and best-response" in text
    assert "Game theory lab 3: controls and gaming-risk frontier" in text
    assert "guided toy incentive simulations" in text
    assert "Marginal gain from extra claims" in text
    assert "Audit cost / penalty strength" in text
    assert "Claim rule clarity" in text
    assert "Cooperation gain" in text
    assert "Cherry-pick gain" in text
    assert "Scope flexibility" in text
    assert "Place accountability" in text
    assert "Access gain" in text
    assert "Control strength" in text
    assert "Monitoring cost" in text

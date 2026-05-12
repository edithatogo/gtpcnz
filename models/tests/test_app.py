from streamlit.testing.v1 import AppTest


APP_PATH = "models/primarycare_model/app.py"
DEPLOYMENT_ENTRYPOINT = "streamlit_app.py"

def test_app_smoke():
    """Basic smoke test to ensure the app can be initialized."""
    at = AppTest.from_file(APP_PATH, default_timeout=30)
    at.run()
    assert not at.exception


def test_deployment_entrypoint_smoke():
    """Community Cloud entrypoint should run without crashing."""
    at = AppTest.from_file(DEPLOYMENT_ENTRYPOINT, default_timeout=30)
    at.run()
    assert not at.exception

def test_app_sliders_exist():
    """Verify that the expected sliders are present in the sidebar."""
    at = AppTest.from_file(APP_PATH, default_timeout=30)
    at.run()

    # Check for sliders in sidebar
    assert len(at.sidebar.slider) >= 7

    expected_labels = {
        "Payment for extra primary care activity",
        "Stable population-based base funding",
        "Whole-population local accountability",
        "Claim rules and audit strength",
        "Equity and co-payment protection",
        "Flexible workforce scope",
        "Local in-person care capacity",
    }
    slider_labels = [s.label for s in at.sidebar.slider]
    assert expected_labels.issubset(set(slider_labels))

def test_app_reactive_logic():
    """Verify that changing a slider updates the internal state."""
    at = AppTest.from_file(APP_PATH, default_timeout=30)
    at.run()

    activity_payment_slider = at.sidebar.slider[0]
    activity_payment_slider.set_value(80).run()

    assert not at.exception

def test_app_expander_exists():
    """Verify the educational section is present."""
    at = AppTest.from_file(APP_PATH, default_timeout=30)
    at.run()
    assert len(at.expander) > 0
    assert "Learn the 'Big Words'" in at.expander[0].label

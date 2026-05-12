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
    assert len(at.sidebar.slider) >= 2
    
    # Verify specific sliders by label (using partial match if needed)
    slider_labels = [s.label for s in at.sidebar.slider]
    assert any("Pay-per-visit" in label for label in slider_labels)
    assert any("Subscription" in label for label in slider_labels)

def test_app_reactive_logic():
    """Verify that changing a slider updates the internal state."""
    at = AppTest.from_file(APP_PATH, default_timeout=30)
    at.run()
    
    # Find the FFS slider and change its value
    ffs_slider = at.sidebar.slider[0]
    ffs_slider.set_value(80).run()
    
    # In a real app we might check for specific text changes or plot data updates
    # For now, we just ensure it didn't crash after a state change
    assert not at.exception

def test_app_expander_exists():
    """Verify the educational section is present."""
    at = AppTest.from_file(APP_PATH, default_timeout=30)
    at.run()
    assert len(at.expander) > 0
    assert "Learn the 'Big Words'" in at.expander[0].label

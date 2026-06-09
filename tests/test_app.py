from __future__ import annotations

from pathlib import Path

from streamlit.testing.v1 import AppTest

ROOT = Path(__file__).resolve().parents[1]
MOCK_APP = ROOT / "tests" / "fixtures" / "mock_streamlit_app.py"


def test_mocked_entrypoint_accepts_numeric_updates_and_runs() -> None:
    at = AppTest.from_file(str(MOCK_APP), default_timeout=10)
    at.run()
    assert not at.exception

    at.number_input[0].set_value(2500)
    at.number_input[1].set_value(0.75)
    at.number_input[2].set_value(0.2)
    at.button[0].click()
    at.run()

    assert not at.exception
    assert len(at.metric) == 1
    assert len(at.dataframe) == 1


def test_deployment_entrypoint_renders_without_exceptions() -> None:
    at = AppTest.from_file("streamlit_app.py", default_timeout=90)
    at.run()
    assert not at.exception

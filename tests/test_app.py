from __future__ import annotations

from pathlib import Path
from textwrap import dedent

from streamlit.testing.v1 import AppTest


def test_mocked_entrypoint_accepts_numeric_updates_and_runs(tmp_path: Path) -> None:
    app_file = tmp_path / "mock_streamlit_app.py"
    app_file.write_text(
        dedent(
            """
            import pandas as pd
            import streamlit as st

            st.set_page_config(page_title="GTPCNZ simulation smoke", layout="wide")
            st.title("GTPCNZ simulation smoke")

            consultations = st.number_input("Consultations", min_value=0, value=1000, step=100)
            access_weight = st.number_input("Access weight", min_value=0.0, max_value=1.0, value=0.5, step=0.05)
            fiscal_risk = st.number_input("Fiscal risk", min_value=0.0, max_value=1.0, value=0.1, step=0.05)

            if st.button("Run simulation"):
                net_benefit = consultations * access_weight * (1 - fiscal_risk)
                st.metric("Net benefit index", round(net_benefit, 2))
                st.dataframe(
                    pd.DataFrame(
                        [
                            {
                                "consultations": consultations,
                                "access_weight": access_weight,
                                "fiscal_risk": fiscal_risk,
                                "net_benefit": net_benefit,
                            }
                        ]
                    )
                )
            """
        ),
        encoding="utf-8",
    )

    at = AppTest.from_file(str(app_file), default_timeout=10)
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

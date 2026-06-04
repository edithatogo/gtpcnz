import sys
from pathlib import Path
from typing import NoReturn

ROOT = Path(__file__).resolve().parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

PUBLIC_CAVEAT = (
    "This is a public-data anchored benchmark and educational explainer. "
    "It is not linked-data calibrated and not a patient-level forecast. "
    "It should not be used to claim precise fiscal savings, hospital-demand reductions, "
    "workforce effects, or implementation impacts."
)


def _render_startup_failure(exc: Exception) -> NoReturn:
    import streamlit as st

    st.set_page_config(page_title="GTPCNZ dashboard", layout="wide")
    st.title("GTPCNZ dashboard")
    st.error("The full dashboard could not start in this deployment environment.")
    st.warning(PUBLIC_CAVEAT)
    st.caption(
        "Startup degraded mode. Public claims remain limited to the benchmark/explainer boundary until the "
        "runtime issue is fixed and release gates pass."
    )
    with st.expander("Runtime diagnostic"):
        st.code(f"{type(exc).__name__}: {exc}")
    st.stop()


def main() -> None:
    try:
        from models.primarycare_model.app import render_app

        render_app()
    except Exception as exc:
        _render_startup_failure(exc)


if __name__ == "__main__":
    main()

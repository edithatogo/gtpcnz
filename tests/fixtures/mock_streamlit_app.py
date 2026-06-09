from __future__ import annotations

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

"""
Streamlit page: Bass Diffusion Adoption Animation.
Animated choropleth/line charts of adoption trajectories over 10-15 years.
"""
import time
import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st

from models.primarycare_model.diffusion import (
    BassDiffusionParams, SCENARIO_PRESETS, simulate_bass,
)


def render_page() -> None:
    st.set_page_config(page_title="Bass Diffusion", page_icon=":chart_with_upwards_trend:", layout="wide")
    st.title("Bass Diffusion Adoption Animation")
    st.caption("Animated adoption trajectories: innovation reform rollout over time")

    with st.sidebar:
        st.header("Diffusion Parameters")
        preset_name = st.selectbox("Scenario preset", ["Custom"] + list(SCENARIO_PRESETS.keys()))
        if preset_name != "Custom":
            preset = SCENARIO_PRESETS[preset_name]
            p = st.slider("Innovation (p)", 0.001, 0.100, preset.p, 0.001, format="%.3f")
            q = st.slider("Imitation (q)", 0.05, 1.00, preset.q, 0.01, format="%.2f")
            M = st.number_input("Market potential", 100, 10000, preset.M, 100)
            T = st.slider("Time horizon (years)", 5, 20, preset.T, 1)
        else:
            p = st.slider("Innovation (p)", 0.001, 0.100, 0.030, 0.001, format="%.3f")
            q = st.slider("Imitation (q)", 0.05, 1.00, 0.40, 0.01, format="%.2f")
            M = st.number_input("Market potential", 100, 10000, 1000, 100)
            T = st.slider("Time horizon (years)", 5, 20, 15, 1)
        num_regions = st.slider("Geographic regions", 1, 30, 15, 1)
        speed = st.slider("Animation speed", 0.1, 2.0, 0.5, 0.1)
        play = st.button(":arrow_forward: Animate", type="primary")
        reset = st.button(":stop_button: Reset")


    params = BassDiffusionParams(p=p, q=q, M=M, T=T, num_regions=num_regions)
    result = simulate_bass(params)
    df = result.time_series

    col1, col2 = st.columns([2, 1])
    with col1:
        st.subheader("Adoption S-Curve")
        main_chart = st.empty()
        st.subheader("Yearly New Adopters")
        new_chart = st.empty()
    with col2:
        st.subheader("Regional Adoption")
        region_chart = st.empty()
        st.subheader("Summary")
        metrics_box = st.empty()

    metrics_box.markdown(f"**Final rate:** {df['adoption_rate'].iloc[-1]:.1%}  ")
    metrics_box.markdown(f"**Adopters:** {int(df['adopters'].iloc[-1]):,}/{M:,}  ")
    metrics_box.markdown(f"**p={p:.3f}, q={q:.2f}**")

    if play or "diff_playing" in st.session_state:
        st.session_state.diff_playing = True
        bar = st.progress(0)
        for year in range(1, T+1):
            sub = df[df["year"] <= year]
            fig1 = go.Figure()
            fig1.add_trace(go.Scatter(x=sub["year"], y=sub["adoption_rate"],
                mode="lines+markers", name="Adoption Rate",
                line=dict(width=3, color="#147a4f")))
            fig1.add_trace(go.Scatter(x=sub["year"], y=sub["adopters"],
                mode="lines+markers", name="Cumulative",
                line=dict(width=2, color="#2E86AB"), yaxis="y2"))
            fig1.update_layout(height=350, xaxis=dict(range=[0,T]),
                yaxis=dict(range=[0,1.05], title="Rate", tickformat=".0%"),
                yaxis2=dict(range=[0,M*1.05], title="Adopters", overlaying="y", side="right"))
            main_chart.plotly_chart(fig1, use_container_width=True, key=f"m{year}")

            fig2 = px.bar(sub, x="year", y="new_adopters",
                color_discrete_sequence=["#147a4f"])
            fig2.update_layout(height=250)
            new_chart.plotly_chart(fig2, use_container_width=True, key=f"n{year}")

            if result.region_time_series is not None:
                rs = result.region_time_series[result.region_time_series["year"]==year]
                if not rs.empty:
                    fig3 = px.bar(rs.sort_values("adoption_rate"),
                        x="region", y="adoption_rate", color="adoption_rate",
                        color_continuous_scale="Greens", range_color=[0,1],
                        title=f"Year {year}")
                    fig3.update_layout(height=350, xaxis_tickangle=-45)
                    region_chart.plotly_chart(fig3, use_container_width=True, key=f"r{year}")

            bar.progress(year/T)
            time.sleep(speed*0.3)
        st.session_state.diff_playing = False
        bar.empty()
        st.success("Complete!")

    if reset:
        st.session_state.diff_playing = False
        st.rerun()

if __name__ == "__main__":
    render_page()

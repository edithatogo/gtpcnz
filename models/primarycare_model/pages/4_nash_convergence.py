"""
Streamlit page: Nash Equilibrium Convergence Trace.
Animated gradient path of clinical utility optimisation.
"""
import time

import numpy as np
import plotly.graph_objects as go
import streamlit as st

from models.primarycare_model.nash_opt import (
    GAME_PRESETS,
    compute_payoff_landscape,
    nash_best_response_dynamics,
    run_nash_with_multiple_starts,
)


def render_page() -> None:
    st.set_page_config(page_title="Nash Convergence", page_icon=":game_die:", layout="wide")
    st.title("Nash Equilibrium Convergence Trace")
    st.caption("Step-by-step gradient path of best-response dynamics for funding model games")

    with st.sidebar:
        st.header("Game Configuration")
        game_name = st.selectbox("Game preset", list(GAME_PRESETS.keys()))
        payoff_matrix = GAME_PRESETS[game_name]

        init_cap_p0 = st.slider("Player 0 initial capitation weight", 0.0, 1.0, 0.5, 0.05)
        init_cap_p1 = st.slider("Player 1 initial capitation weight", 0.0, 1.0, 0.5, 0.05)
        lr = st.slider("Learning rate", 0.05, 1.0, 0.5, 0.05)
        max_iter = st.slider("Max iterations", 10, 200, 80, 10)
        multiple_starts = st.checkbox("Multiple starting points", value=True)
        play = st.button(":arrow_forward: Run Dynamics", type="primary")
        step_once = st.button(":footprints: Step Single")
        reset = st.button(":stop_button: Reset")


    init_strat = np.array([init_cap_p0, init_cap_p1])

    # Pre-compute landscape
    landscape_df = compute_payoff_landscape(payoff_matrix)

    col1, col2 = st.columns([2, 1])
    with col1:
        st.subheader("Strategy Space & Convergence Path")
        path_chart = st.empty()
        st.subheader("Convergence Trace (Payoffs)")
        trace_chart = st.empty()
    with col2:
        st.subheader("Strategy Evolution")
        strat_chart = st.empty()
        st.subheader("Game Info")
        info_box = st.empty()
        st.subheader("Nash Equilibrium")
        nash_box = st.empty()

    info_box.markdown(f"**{payoff_matrix.row_label}** vs **{payoff_matrix.col_label}**  ")
    info_box.markdown(f"Strategies: {payoff_matrix.strategy_labels[0]} / {payoff_matrix.strategy_labels[1]}  ")

    # Run dynamics
    existing_trace = st.session_state.get("nash_trace")
    if play or existing_trace is not None:
        if play or existing_trace is None:
            if multiple_starts:
                traces = run_nash_with_multiple_starts(payoff_matrix, num_starts=5, max_iterations=max_iter)
                st.session_state.nash_traces = traces
                trace = traces[0]
            else:
                trace = nash_best_response_dynamics(payoff_matrix, init_strat, max_iter, learning_rate=lr)
                st.session_state.nash_traces = [trace]
            st.session_state.nash_trace = trace
            st.session_state.nash_step = 0

        trace = st.session_state.nash_trace
        trace_df = trace.to_dataframe()
        bar = st.progress(0) if play else None

        total_steps = len(trace_df)
        steps_to_show = max(1, min(st.session_state.get("nash_step", 0) + (1 if step_once else 10), total_steps))

        if step_once:
            steps_to_show = min(st.session_state.get("nash_step", 0) + 1, total_steps)
            st.session_state.nash_step = steps_to_show

        if play:
            steps_to_show = total_steps
            st.session_state.nash_step = total_steps

        for si in range(steps_to_show):
            sub = trace_df.iloc[:si+1]

            # Contour + path
            fig1 = go.Figure()
            z_pivot = landscape_df.pivot_table(
                index="p1_capitation", columns="p0_capitation", values="total_welfare"
            )
            fig1.add_trace(go.Contour(
                z=z_pivot.values, x=z_pivot.columns, y=z_pivot.index,
                colorscale="Viridis", name="Welfare", contours=dict(showlabels=True),
                hovertemplate="P0: %{x:.2f}<br>P1: %{y:.2f}<br>Welfare: %{z:.2f}<extra></extra>"
            ))
            fig1.add_trace(go.Scatter(x=sub["p0_strategy_capitation"], y=sub["p1_strategy_capitation"],
                mode="lines+markers", name="Dynamics Path",
                line=dict(color="red", width=2), marker=dict(size=5)))
            fig1.add_trace(go.Scatter(x=[sub["p0_strategy_capitation"].iloc[-1]], y=[sub["p1_strategy_capitation"].iloc[-1]],
                mode="markers", name="Current", marker=dict(color="red", size=12, symbol="star")))
            fig1.update_layout(height=400, xaxis=dict(range=[0,1], title="P0: Capitation Weight"),
                yaxis=dict(range=[0,1], title="P1: Capitation Weight"))
            path_chart.plotly_chart(fig1, use_container_width=True, key=f"path_{si}")

            # Convergence trace
            fig2 = go.Figure()
            for col in ["p0_payoff", "p1_payoff", "total_welfare"]:
                if col in sub.columns:
                    fig2.add_trace(go.Scatter(x=sub["iteration"], y=sub[col],
                        mode="lines+markers", name=col.replace("_"," ").title()))
            fig2.update_layout(height=300, xaxis_title="Iteration", yaxis_title="Payoff")
            trace_chart.plotly_chart(fig2, use_container_width=True, key=f"trace_{si}")

            # Strategy evolution
            fig3 = go.Figure()
            for col in ["p0_strategy_capitation", "p1_strategy_capitation"]:
                if col in sub.columns:
                    label = "P0 Capitation" if "p0" in col else "P1 Capitation"
                    fig3.add_trace(go.Scatter(x=sub["iteration"], y=sub[col],
                        mode="lines+markers", name=label))
            fig3.update_layout(height=300, xaxis_title="Iteration", yaxis_title="Strategy Weight")
            strat_chart.plotly_chart(fig3, use_container_width=True, key=f"strat_{si}")

            if bar:
                bar.progress((si+1)/total_steps)
                time.sleep(0.05)

        if bar:
            bar.empty()
        nash_box.markdown(f"**Converged:** {trace.converged}  ")
        nash_box.markdown(f"**Iterations:** {trace.num_iterations}  ")
        if trace.final_strategies is not None:
            nash_box.markdown(f"**Equilibrium:** P0={trace.final_strategies[0]:.3f}, P1={trace.final_strategies[1]:.3f}  ")

    if reset:
        st.session_state.pop("nash_trace", None)
        st.session_state.pop("nash_traces", None)
        st.session_state.pop("nash_step", None)
        st.rerun()

if __name__ == "__main__":
    render_page()

"""
Streamlit page: Rolling Monte Carlo Histogram.
Shows uncertainty limits narrowing dynamically as batched iterations run.
"""
import time

import numpy as np
import plotly.graph_objects as go
import streamlit as st

from models.primarycare_model.jax_mc import MCConfig, run_monte_carlo


def render_page() -> None:
    st.set_page_config(page_title="MC Histogram", page_icon=":bar_chart:", layout="wide")
    st.title("Monte Carlo Rolling Histogram")
    st.caption("Uncertainty bounds narrowing dynamically as JAX batched iterations run")

    with st.sidebar:
        st.header("MC Configuration")
        num_iterations = st.slider("Total iterations", 50, 5000, 500, 50)
        num_batches = st.slider("Number of batches", 2, 50, 10, 1)
        pert_std = st.slider("Perturbation width", 0.01, 0.20, 0.08, 0.01, format="%.2f")
        seed = st.number_input("Random seed", 1, 999999, 42, 1)
        target_metric = st.selectbox("Target metric", [
            "access_rate", "hospital_pressure_index",
            "equity_gap_index", "fiscal_risk_index",
            "unmet_need_index", "provider_utilisation",
        ])
        run_btn = st.button(":arrow_forward: Run MC Sweep", type="primary")


    col1, col2 = st.columns([2, 1])
    with col1:
        st.subheader("Rolling Histogram")
        hist_chart = st.empty()
        st.subheader("CI Convergence")
        ci_chart = st.empty()
    with col2:
        st.subheader("Summary Stats")
        stats_box = st.empty()
        st.subheader("Distributions")
        dist_chart = st.empty()

    if run_btn:
        config = MCConfig(num_iterations=num_iterations, num_batches=num_batches,
            perturbation_std=pert_std, seed=seed,
            target_metrics=("access_rate","hospital_pressure_index","equity_gap_index","fiscal_risk_index","unmet_need_index","provider_utilisation"))
        all_metrics = {m: [] for m in config.target_metrics}
        bar = st.progress(0)
        status = st.empty()

        def cb(bi, ba):
            for m,v in ba.items():
                if m in all_metrics:
                    all_metrics[m].append(v)

        status.text(f"Running {num_iterations} iters in {num_batches} batches...")
        result = run_monte_carlo(config=config, progress_callback=cb)

        for bi in range(num_batches):
            current = (bi+1)*(num_iterations//num_batches)
            vals = result.metrics.get(target_metric, np.array([]))[:current]
            if len(vals) > 0:
                fig1 = go.Figure()
                fig1.add_trace(go.Histogram(x=vals, nbinsx=30,
                    name=target_metric.replace("_"," ").title(), marker_color="#147a4f"))
                for p,c in [(np.percentile(vals,5),"red"), (np.percentile(vals,50),"blue"), (np.percentile(vals,95),"red")]:
                    fig1.add_vline(x=p, line=dict(color=c, width=2))
                fig1.update_layout(height=350, title=f"{current} iters")
                hist_chart.plotly_chart(fig1, use_container_width=True, key=f"h{bi}")

                means, lo, hi = result.rolling_ci(target_metric, window=max(10,num_iterations//num_batches))
                if len(means) > 0:
                    fig2 = go.Figure()
                    fig2.add_trace(go.Scatter(x=list(range(len(means))), y=means, mode="lines", name="Mean"))
                    fig2.add_trace(go.Scatter(x=list(range(len(means))), y=lo, mode="lines", name="CI", line=dict(dash="dash")))
                    fig2.add_trace(go.Scatter(x=list(range(len(means))), y=hi, mode="lines", fill="tonexty",
                        line=dict(dash="dash"), fillcolor="rgba(255,0,0,0.1)"))
                    fig2.update_layout(height=300, title="95% CI Convergence")
                    ci_chart.plotly_chart(fig2, use_container_width=True, key=f"ci{bi}")

                stats_box.markdown(f"**Mean:** {np.mean(vals):.4f}  ")
                stats_box.markdown(f"**Std:** {np.std(vals):.4f}  ")
                stats_box.markdown(f"**P5/P50/P95:** {np.percentile(vals,5):.4f}/{np.percentile(vals,50):.4f}/{np.percentile(vals,95):.4f}  ")

                fig3 = go.Figure()
                for m in list(config.target_metrics)[:4]:
                    mv = result.metrics.get(m, np.array([]))[:current]
                    if len(mv) > 0:
                        fig3.add_trace(go.Box(y=mv, name=m.replace("_"," ").title()))
                fig3.update_layout(height=300)
                dist_chart.plotly_chart(fig3, use_container_width=True, key=f"d{bi}")

            bar.progress((bi+1)/num_batches)
            status.text(f"Batch {bi+1}/{num_batches}")
            time.sleep(0.1)

        bar.empty()
        status.text("Complete!")
        st.success(f"Done: {num_iterations} iterations")
        st.balloons()
    else:
        st.info("Configure and press **Run MC Sweep**")

if __name__ == "__main__":
    render_page()

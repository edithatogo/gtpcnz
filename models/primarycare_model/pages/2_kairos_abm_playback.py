"""
Streamlit: kairos ABM Playback - Real-time practice status grid/network viz.
Shows patient flow, provider queues, and funding model status transitions.
"""
import time

import matplotlib.pyplot as plt
import networkx as nx
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st

from models.primarycare_model.abm import ABMParameters, ABMSimulation


def render_page() -> None:
    st.set_page_config(page_title="ABM Playback", page_icon=":arrows_counterclockwise:", layout="wide")
    st.title("kairos ABM Playback")
    st.caption("Real-time practice status: patient flow, provider queues, funding model transitions")

    with st.sidebar:
        st.header("Simulation Controls")
        num_months = st.slider("Simulation months", 6, 60, 24, 6)
        pop_size = st.slider("Population size", 50, 500, 180, 10)
        seed = st.number_input("Random seed", 1, 999999, 42, 1)
        speed = st.slider("Speed (ms per tick)", 50, 1000, 200, 50)
        funding_model = st.selectbox("Funding model", ["capitation", "ffs", "hybrid"])
        play = st.button(":arrow_forward: Play", type="primary")
        reset = st.button(":stop_button: Reset")

    params = ABMParameters(months=num_months, population_size=pop_size, seed=seed)
    col1, col2 = st.columns([2, 1])

    with col1:
        st.subheader("Patient Flow Over Time")
        flow_chart = st.empty()
        st.subheader("Provider Queue Status")
        prov_chart = st.empty()

    with col2:
        st.subheader("Network Graph")
        net_placeholder = st.empty()
        st.subheader("Funding Model")
        trans_placeholder = st.empty()
        st.subheader("Key Metrics")
        metrics_placeholder = st.empty()

    if "abm_history" not in st.session_state or reset:
        st.session_state.abm_history = []
        st.session_state.abm_month = 0
        st.session_state.abm_running = False

    if play:
        st.session_state.abm_running = True
    if reset:
        st.session_state.abm_history = []
        st.session_state.abm_month = 0
        st.session_state.abm_running = False


    if st.session_state.abm_running and st.session_state.abm_month < num_months:
        sim = ABMSimulation(params)
        result = sim.run()
        monthly_df = result.monthly
        progress_bar = st.progress(0)
        status_text = st.empty()

        for month_idx in range(num_months):
            if month_idx >= len(monthly_df):
                break
            row = monthly_df.iloc[month_idx]
            st.session_state.abm_history.append(row.to_dict())
            st.session_state.abm_month = month_idx + 1

            history_df = pd.DataFrame(st.session_state.abm_history)
            if not history_df.empty and "month" in history_df.columns:
                fig1 = go.Figure()
                for col in ["total_demand_contacts", "resolved_contacts", "unresolved_contacts"]:
                    if col in history_df.columns:
                        fig1.add_trace(go.Scatter(x=history_df["month"], y=history_df[col],
                            mode="lines+markers", name=col.replace("_"," ").title()))
                fig1.update_layout(height=300, margin=dict(l=20,r=20,t=20,b=20))
                flow_chart.plotly_chart(fig1, use_container_width=True, key=f"f{month_idx}")

            avail = [c for c in ["access_rate","provider_utilisation","equity_gap_index"] if c in history_df.columns]
            if avail:
                fig2 = go.Figure()
                for c in avail:
                    fig2.add_trace(go.Bar(x=[c.replace("_"," ").title()], y=[history_df[c].iloc[-1]], name=c.replace("_"," ").title()))
                fig2.update_layout(height=250, margin=dict(l=20,r=20,t=20,b=20))
                prov_chart.plotly_chart(fig2, use_container_width=True, key=f"p{month_idx}")

            G = nx.Graph()
            for p in sim.providers[:10]:
                G.add_node(f"P{p.provider_id}", type="provider")
            for pat in sim.patients[:30]:
                G.add_node(f"C{pat.patient_id}", type="patient")
            for i, pat in enumerate(sim.patients[:10]):
                if sim.providers:
                    G.add_edge(
                        f"C{pat.patient_id}",
                        f"P{sim.providers[i % len(sim.providers)].provider_id}",
                    )
            fig3, ax3 = plt.subplots(figsize=(4,3))
            colors = ["red" if n[0]=="P" else "lightblue" for n in G.nodes()]
            nx.draw(G, pos=nx.spring_layout(G, seed=42, k=0.5), ax=ax3, node_color=colors, node_size=50, with_labels=False)
            net_placeholder.pyplot(fig3)
            plt.close(fig3)

            td = pd.DataFrame({"Model":["Capitation","FFS","Hybrid"],"Status":[1.0 if funding_model=="capitation" else 0.3, 1.0 if funding_model=="ffs" else 0.3, 1.0 if funding_model=="hybrid" else 0.3]})
            fig4 = px.bar(td, x="Model", y="Status", range_y=[0,1.2], color="Model", title=f"Active: {funding_model.title()}")
            fig4.update_layout(height=200, showlegend=False, margin=dict(l=20,r=20,t=30,b=20))
            trans_placeholder.plotly_chart(fig4, use_container_width=True, key=f"t{month_idx}")

            metrics_data = {"Access Rate":f"{row.get('access_rate',0):.3f}", "Hospital Pressure":f"{row.get('hospital_pressure_index',0):.3f}", "Equity Gap":f"{row.get('equity_gap_index',0):.3f}", "Fiscal Risk":f"{row.get('fiscal_risk_index',0):.3f}"}
            metrics_placeholder.markdown("\n".join([f"**{k}:** {v}" for k,v in metrics_data.items()]))

            progress_bar.progress((month_idx+1)/num_months)
            status_text.text(f"Month {month_idx+1}/{num_months}")
            time.sleep(speed/1000.0)

        st.session_state.abm_running = False
        progress_bar.empty()
        status_text.text("Complete!")
        st.success(f"Completed {num_months} months")
    else:
        st.info("Press **Play** to start")

if __name__ == "__main__":
    render_page()

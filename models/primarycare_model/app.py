import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os

# Set page config
st.set_page_config(
    page_title="Primary Care Pulse",
    page_icon="🩺",
    layout="wide"
)

# Title and Introduction
st.title("🩺 Primary Care Pulse: The Funding Dashboard")
st.markdown("""
### How should we pay our neighborhood doctors?
Welcome to the interactive funding simulator! This dashboard helps you explore different ways to pay for healthcare. 

**The Goal:** Keep people healthy in their neighborhoods (Supply) and reduce the number of people who have to go to the Emergency Room (Hospital Pressure).
""")

# Sidebar for Controls
st.sidebar.header("🕹️ Change the Rules")

st.sidebar.markdown("""
Use these sliders to change how doctors are paid.
""")

# Simulation Parameters
benefit_level = st.sidebar.slider(
    "💰 Pay-per-visit (FFS) Level", 
    0, 100, 50, 
    help="How much extra we pay a doctor every time they see a patient. This is called 'Fee-for-Service' (FFS)."
)

capitation_weight = st.sidebar.slider(
    "📦 'Subscription' (Capitation) Weight", 
    0, 100, 70,
    help="How much we pay a doctor just for having you on their list, even if you don't visit. This is called 'Capitation'."
)

equity_focus = st.sidebar.select_slider(
    "🤝 Equity & Fairness Focus",
    options=["Low", "Medium", "High"],
    value="Medium",
    help="How much extra help we give to people who need it most (like those living in rural areas or with less money)."
)

# Main Dashboard View
tab1, tab2 = st.tabs(["📊 Funding Simulator", "📁 Evidence & OIA Tracker"])

with tab1:
    col1, col2 = st.columns(2)

    # Load existing results for comparison
    # Use robust path resolution
    base_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    results_path = os.path.join(base_dir, "outputs", "full-parameterised-summary-results-v1.7.0.csv")

    if not os.path.exists(results_path):
        st.error(f"Could not find results file at {results_path}")
        df = pd.DataFrame(columns=["scenario_name", "hybrid_viability_score", "supply_generation_score", "hospital_pressure_score"])
    else:
        df = pd.read_csv(results_path)

    with col1:
        st.subheader("📈 Model Comparison")
        st.write("Here is how your choices compare to our simulated models.")
        
        # Simple reactive calculation (demonstrative)
        user_score = (benefit_level * 0.4) + (capitation_weight * 0.3) + (10 if equity_focus == "High" else 5)
        
        # Plotting
        fig, ax = plt.subplots()
        ax.barh(df["scenario_name"], df["hybrid_viability_score"], color='lightgrey', alpha=0.5, label="Simulated Models")
        ax.barh("YOUR MODEL", user_score, color='green', label="Your Settings")
        ax.set_xlabel("Overall System Score")
        ax.set_title("How Viable is Your Funding Model?")
        ax.legend()
        st.pyplot(fig)

    with col2:
        st.subheader("🏥 Hospital Pressure vs. 🏥 Doctor Supply")
        st.markdown("""
        In a good system:
        1. **Doctor Supply** should be **HIGH** (lots of appointments).
        2. **Hospital Pressure** should be **LOW** (ER isn't crowded).
        """)
        
        # Scatter plot
        fig2, ax2 = plt.subplots()
        ax2.scatter(df["supply_generation_score"], df["hospital_pressure_score"], color='blue', alpha=0.6)
        
        # Your point (demonstrative)
        your_supply = benefit_level * 0.8
        your_pressure = 100 - (benefit_level * 0.5 + capitation_weight * 0.2)
        ax2.scatter(your_supply, your_pressure, color='red', s=100, label="Your Settings")
        
        ax2.set_xlabel("Doctor Supply (Appointments)")
        ax2.set_ylabel("Hospital Pressure (ER Crowding)")
        ax2.legend()
        st.pyplot(fig2)

with tab2:
    st.subheader("🔍 Official Information Act (OIA) Tracker")
    st.markdown("""
    To move this model from a "demonstrative simulation" to a real-world predictive tool, we need accurate administrative data. 
    Below is the status of our public information requests.
    """)
    
    tracker_path = os.path.join(base_dir, "docs", "audit", "oia-request-tracker.csv")
    if os.path.exists(tracker_path):
        oia_df = pd.read_csv(tracker_path)
        
        # Style the dataframe based on status
        def color_status(val):
            color = 'orange' if val == 'Pending' else 'green' if val == 'Complete' else 'red' if val == 'Rejected' else 'white'
            return f'color: {color}'
        
        st.dataframe(oia_df.style.map(color_status, subset=['status']), use_container_width=True)
    else:
        st.warning("OIA Tracker database not found.")
    
    st.info("No relevant existing OIA responses were found on FYI.org.nz. We are proceeding with drafting original requests.")

# Educational Section
with st.expander("📚 Learn the 'Big Words'"):
    st.markdown("""
    - **Capitation:** Like a 'subscription fee' for your doctor. They get a set amount of money to look after you all year.
    - **FFS (Fee-for-Service):** Paying the doctor for each specific thing they do (like a visit or a blood test).
    - **Uncapped:** There is no hard limit on the total budget for visits. If people need help, the money is there.
    - **SOTA (State-of-the-Art):** Using the best and newest methods available!
    """)

st.info("💡 **Pro-Tip:** High 'Pay-per-visit' usually increases supply, but high 'Subscription' focus helps keep doctors' offices open even in quiet times.")

st.markdown("---")
st.caption("Created for the Primary Care Funding Architecture Project (v1.7.2). This is a demonstrative simulator.")

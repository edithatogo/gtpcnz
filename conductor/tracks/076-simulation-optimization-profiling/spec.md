# Track 076 - Simulation optimization and profiling

Optimize the public runtime calculations used by the Dash and Streamlit surfaces without increasing claims or weakening reproducibility.

This track covers:

- profiling the Streamlit-free runtime path with Scalene where available;
- preserving seeded deterministic behavior and current caps unless benchmark evidence supports changes;
- reducing avoidable DataFrame churn and repeated runtime calculations;
- deciding whether any additional pytest stress/repeat plugin is useful after package verification.

This track does not add private data, increase model claims, or remove existing safety caps without a measured gate.


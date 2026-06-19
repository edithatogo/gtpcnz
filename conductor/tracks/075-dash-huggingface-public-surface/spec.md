# Track 075 - Dash Hugging Face public surface

Migrate the future public interactive dashboard from Streamlit Cloud to a Plotly Dash app hosted on Hugging Face Spaces, while keeping GitHub Pages as the public front door.

This track covers:

- a Streamlit-free dashboard service layer for public-safe chart, table, download, and caveat payloads;
- a Dash application with four stable routes: Start, Compare scenarios, Simulation lab, Evidence and methods;
- a Hugging Face Space bundle using Docker and the public source/model artefacts needed by the app;
- public docs and tests that distinguish GitHub Pages, Hugging Face, and Streamlit compatibility.

This track does not remove Streamlit until Dash parity and deployment gates pass.


# Track 077 - Pixi reproducible dashboard runtime

Introduce Prefix.dev Pixi as the primary runner for the new Dash/Hugging Face path while preserving existing `uv` compatibility until the Pixi path is validated.

This track covers:

- Pixi workspace, environment, and task configuration in `pyproject.toml`;
- Hugging Face Docker and GitHub Actions updates to run the Dash app through Pixi;
- local command guidance that avoids the existing `pixi.exe` name collision with a Pixiv downloader;
- generated `pixi.lock` using the real Prefix.dev Pixi binary.

This track does not delete `uv.lock` or rewrite the Streamlit deployment path until Pixi parity gates pass.

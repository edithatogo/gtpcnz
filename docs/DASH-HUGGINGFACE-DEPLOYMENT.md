# Dash Hugging Face Deployment

Canonical GitHub Pages front door: https://edithatogo.github.io/gtpcnz/

Hugging Face interactive lab: https://edithatogo-gtpcnz-dashboard.hf.space/

Legacy Streamlit compatibility dashboard: https://gtpcnz.streamlit.app/

This is a public-data anchored benchmark and educational explainer. It is not linked-data calibrated and not a patient-level forecast. It should not be used to claim precise fiscal savings, ED reductions, hospital-demand reductions, workforce effects, implementation impacts, or causal effects.

## Runtime

The Dash lab is packaged for Hugging Face Spaces with Docker and Prefix.dev Pixi.

Source files:

- `dash_app/app.py`
- `dash_app/assets/styles.css`
- `dash_app/Dockerfile`
- `dash_app/README.hf.md`
- `models/primarycare_model/dashboard_service.py`

The root repository remains the source of truth. The GitHub Action builds a minimal Space bundle and pushes it to `edithatogo/gtpcnz-dashboard` when `HF_TOKEN` is configured.

## Local Commands

Use the repo-local Prefix.dev Pixi wrapper:

```bash
python scripts/bootstrap_prefix_pixi.py
python scripts/run_pixi.py run dash
python scripts/run_pixi.py run -e dev test-dash
python scripts/run_pixi.py run -e dev test-runtime
python scripts/run_pixi.py run -e dev test-public-gates
```

On this Windows workspace, the bare `pixi` command may resolve to a Pixiv downloader rather than Prefix.dev Pixi. Use `scripts/run_pixi.py` unless PATH has been checked with `python scripts/run_pixi.py --version`.

```bash
python scripts/run_pixi.py --version
```

## Deployment

The deployment workflow is:

- `.github/workflows/huggingface-space.yml`

Required repository secret:

- `HF_TOKEN` configured in `edithatogo/gtpcnz` on 2026-06-19

Optional repository variable:

- `HF_SPACE_REPO`, default `edithatogo/gtpcnz-dashboard`

The Space bundle contains the Dash app, runtime model package, current summary CSV, version files, and Pixi project metadata. The workflow validates with focused tests inside the bundle, then removes validation-only tests, Python caches, and Streamlit compatibility entrypoints before pushing to Hugging Face.

## Release Gate

The manual Hugging Face Space deployment has been verified on the free CPU Docker path. The lock-aware runtime was verified at commit `14789d30e9fa58338a7d8acc37a67bd6f036bcc9`, and the Space artifact was then trimmed and live-smoked at commit `a3df917fa4480ca410db1f6de19a4fb749c804c4` to remove validation-only tests, Python caches, and Streamlit-only entrypoints.

The Dash migration release gate is complete when:

- focused Dash/service tests pass;
- runtime and claim-boundary gates pass;
- the GitHub Actions deployment path validates the same bundle with the configured `HF_TOKEN`;
- GitHub Pages links resolve to the Hugging Face lab;
- Streamlit remains clearly labelled as compatibility rather than the future target.

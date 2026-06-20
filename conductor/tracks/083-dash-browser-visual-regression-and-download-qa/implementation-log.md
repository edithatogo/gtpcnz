# Implementation Log

## 2026-06-20

- Added `scripts/check_dash_browser_smoke.py` for real Playwright checks against a local Dash server.
- Added a fast default smoke over Start, Reference scenarios and Runtime health at desktop and mobile widths, with `--full` reserved for heavier live-model and scenario-builder checks.
- Fixed a smoke-harness deadlock by redirecting local Dash server output to `DEVNULL`.
- Verified `python scripts/run_pixi.py run -e dev test-browser-dash` passes.

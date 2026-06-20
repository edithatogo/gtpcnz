# Implementation Log

## 2026-06-20

- Added repo-local Prefix.dev Pixi bootstrap and runner scripts.
- Updated the Pixi guard to prefer `PIXI_EXE`, then `.tools/pixi/0.66.0/pixi.exe`, then PATH, so the local Pixiv downloader conflict is detected without blocking correct repo-local Pixi use.
- Verified `python scripts/run_pixi.py --version` reports `pixi 0.66.0`.
- Verified `python scripts/run_pixi.py run check-pixi` passes against the repo-local Prefix.dev Pixi binary.

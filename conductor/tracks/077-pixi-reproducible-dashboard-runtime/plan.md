# Plan

1. Add `[tool.pixi.workspace]`, environments, and tasks to `pyproject.toml`.
2. Make the Hugging Face Dash Dockerfile use the official Prefix.dev Pixi image and `pixi run dash-prod`.
3. Make the Hugging Face workflow validate with `prefix-dev/setup-pixi`.
4. Document the local `pixi` PATH collision and require the Prefix.dev binary for `pixi.lock` generation.
5. Generate and commit `pixi.lock` with the correct Prefix.dev Pixi binary.

Required checks:

```powershell
pixi run -e dev test-dash
pixi run -e dev test-runtime
pixi run -e dev test-public-gates
```

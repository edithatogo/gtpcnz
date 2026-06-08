from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def main() -> int:
    required = ["pyproject.toml", "uv.lock", "Dockerfile", ".devcontainer/devcontainer.json"]
    missing = [path for path in required if not (ROOT / path).exists()]
    if missing:
        print(f"missing dependency runtime files: {missing}")
        return 1
    legacy = ["requirements.txt", "requirements-dev.txt", "requirements-edge.txt"]
    present = [path for path in legacy if (ROOT / path).exists()]
    if present:
        print(f"legacy pip requirements files remain after uv migration: {present}")
        return 1
    print("uv dependency lock surface passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

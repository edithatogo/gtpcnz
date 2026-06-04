from __future__ import annotations

from pathlib import Path


def test_dependency_files_exist() -> None:
    for path in ["requirements.txt", "requirements-dev.txt", "requirements-edge.txt", "uv.lock", "Dockerfile", ".devcontainer/devcontainer.json"]:
        assert Path(path).exists()

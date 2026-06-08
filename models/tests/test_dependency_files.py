from __future__ import annotations

from pathlib import Path


def test_dependency_files_exist() -> None:
    for path in ["pyproject.toml", "uv.lock", "Dockerfile", ".devcontainer/devcontainer.json"]:
        assert Path(path).exists()


def test_legacy_requirements_files_are_removed() -> None:
    for path in ["requirements.txt", "requirements-dev.txt", "requirements-edge.txt"]:
        assert not Path(path).exists()

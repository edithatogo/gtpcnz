from __future__ import annotations

import importlib.util
import sys
from pathlib import Path


def _load_guard_module():
    path = Path("scripts/check_pixi_package_manager.py")
    spec = importlib.util.spec_from_file_location("check_pixi_package_manager", path)
    assert spec is not None
    assert spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


def test_pixi_guard_rejects_pixiv_downloader_help() -> None:
    guard = _load_guard_module()

    ok, message = guard.classify_pixi_help("Commands: artist bookmarks illust auth Pixiv")

    assert ok is False
    assert "Pixiv downloader" in message


def test_pixi_guard_accepts_prefix_dev_command_shape() -> None:
    guard = _load_guard_module()

    ok, message = guard.classify_pixi_help("Pixi workspace environment task run shell")

    assert ok is True
    assert "Prefix.dev Pixi" in message


def test_run_pixi_detects_selected_environment() -> None:
    path = Path("scripts/run_pixi.py")
    spec = importlib.util.spec_from_file_location("run_pixi", path)
    assert spec is not None
    assert spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)

    assert module._selected_environment(["run", "-e", "dev", "test-dash"]) == "dev"
    assert module._selected_environment(["run", "--environment=edge", "test"]) == "edge"
    assert module._selected_environment(["run", "dash"]) is None

from __future__ import annotations

import os
import subprocess
import sys
from pathlib import Path

from check_pixi_package_manager import check_pixi

ROOT = Path(__file__).resolve().parents[1]


def _selected_environment(args: list[str]) -> str | None:
    for index, arg in enumerate(args):
        if arg in {"-e", "--environment"} and index + 1 < len(args):
            return args[index + 1]
        if arg.startswith("--environment="):
            return arg.split("=", 1)[1]
    return None


def _with_windows_site_packages(env: dict[str, str], args: list[str]) -> dict[str, str]:
    if sys.platform != "win32":
        return env
    environment = _selected_environment(args) or "default"
    environment_root = ROOT / ".pixi" / "envs" / environment
    stdlib = environment_root / "Lib"
    site_packages = stdlib / "site-packages"
    if not stdlib.exists() or not site_packages.exists():
        return env
    existing = env.get("PYTHONPATH")
    pixi_paths = os.pathsep.join([str(stdlib), str(site_packages)])
    env["PYTHONPATH"] = pixi_paths if not existing else f"{pixi_paths}{os.pathsep}{existing}"
    return env


def main(argv: list[str] | None = None) -> int:
    args = list(sys.argv[1:] if argv is None else argv)
    check = check_pixi()
    if not check.ok or check.executable is None:
        print(check.message, file=sys.stderr)
        print("Run: python scripts/bootstrap_prefix_pixi.py", file=sys.stderr)
        return 1
    env = os.environ.copy()
    env = _with_windows_site_packages(env, args)
    return subprocess.call([check.executable, *args], env=env)


if __name__ == "__main__":
    raise SystemExit(main())

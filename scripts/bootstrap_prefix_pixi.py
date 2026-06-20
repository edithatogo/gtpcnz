from __future__ import annotations

import argparse
import shutil
import sys
import tempfile
import urllib.request
import zipfile
from pathlib import Path

from check_pixi_package_manager import PIXI_VERSION, classify_pixi_help, repo_pixi_path


def _download(url: str, destination: Path) -> None:
    with urllib.request.urlopen(url, timeout=120) as response:
        destination.write_bytes(response.read())


def _install_windows_x64(version: str, destination: Path, force: bool) -> Path:
    pixi_exe = destination / "pixi.exe"
    if pixi_exe.exists() and not force:
        return pixi_exe

    destination.mkdir(parents=True, exist_ok=True)
    archive_url = f"https://github.com/prefix-dev/pixi/releases/download/v{version}/pixi-x86_64-pc-windows-msvc.zip"
    with tempfile.TemporaryDirectory(prefix="gtpcnz-pixi-") as temp_dir:
        archive_path = Path(temp_dir) / "pixi.zip"
        _download(archive_url, archive_path)
        with zipfile.ZipFile(archive_path) as archive:
            member = next((name for name in archive.namelist() if name.lower().endswith("pixi.exe")), None)
            if member is None:
                raise RuntimeError(f"Archive did not contain pixi.exe: {archive_url}")
            extracted = Path(archive.extract(member, temp_dir))
            shutil.copy2(extracted, pixi_exe)
    return pixi_exe


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Install pinned Prefix.dev Pixi into the repo-local tool cache.")
    parser.add_argument("--version", default=PIXI_VERSION)
    parser.add_argument("--force", action="store_true")
    args = parser.parse_args(argv)

    if sys.platform != "win32":
        print("Repo-local Pixi bootstrap currently supports Windows x64 only; use the official installer on this platform.")
        return 2

    pixi_exe = _install_windows_x64(args.version, repo_pixi_path(args.version).parent, args.force)
    import subprocess

    result = subprocess.run([str(pixi_exe), "--help"], check=False, capture_output=True, text=True, timeout=30)
    ok, message = classify_pixi_help(f"{result.stdout}\n{result.stderr}")
    print(f"pixi executable: {pixi_exe}")
    print(message)
    if not ok:
        return 1
    print(f"Use this binary directly, or run: {sys.executable} scripts/run_pixi.py --help")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

from __future__ import annotations

import os
import shutil
import subprocess
from dataclasses import dataclass
from pathlib import Path

PIXI_VERSION = "0.66.0"
ROOT = Path(__file__).resolve().parents[1]


@dataclass(frozen=True)
class PixiCheck:
    executable: str | None
    ok: bool
    message: str


def repo_pixi_path(version: str = PIXI_VERSION) -> Path:
    return ROOT / ".tools" / "pixi" / version / "pixi.exe"


def pixi_candidates() -> tuple[Path, ...]:
    candidates: list[Path] = []
    env_path = os.environ.get("PIXI_EXE")
    if env_path:
        candidates.append(Path(env_path))
    candidates.append(repo_pixi_path())
    path_executable = shutil.which("pixi")
    if path_executable is not None:
        candidates.append(Path(path_executable))

    unique: list[Path] = []
    seen: set[str] = set()
    for candidate in candidates:
        key = str(candidate).lower()
        if key not in seen:
            unique.append(candidate)
            seen.add(key)
    return tuple(unique)


def classify_pixi_help(help_text: str) -> tuple[bool, str]:
    lowered = help_text.lower()
    if "pixiv" in lowered or "bookmarks" in lowered or "illust" in lowered:
        return False, "The pixi executable appears to be a Pixiv downloader, not Prefix.dev Pixi."
    if "task" in lowered and ("run" in lowered or "shell" in lowered) and ("environment" in lowered or "workspace" in lowered):
        return True, "Prefix.dev Pixi command shape detected."
    if "prefix.dev" in lowered or "pixi is a package management" in lowered:
        return True, "Prefix.dev Pixi help text detected."
    return False, "Unable to confirm Prefix.dev Pixi from help text."


def check_pixi() -> PixiCheck:
    checked: list[str] = []
    for candidate in pixi_candidates():
        executable = str(candidate)
        if not candidate.exists():
            checked.append(f"{executable}: not found")
            continue
        try:
            result = subprocess.run(
                [executable, "--help"],
                check=False,
                capture_output=True,
                text=True,
                timeout=15,
            )
        except OSError as exc:
            checked.append(f"{executable}: could not execute: {exc}")
            continue
        except subprocess.TimeoutExpired:
            checked.append(f"{executable}: pixi --help timed out")
            continue
        ok, message = classify_pixi_help(f"{result.stdout}\n{result.stderr}")
        if ok:
            return PixiCheck(executable, True, message)
        checked.append(f"{executable}: {message}")

    if not checked:
        return PixiCheck(None, False, "Prefix.dev Pixi was not found. Run: python scripts/bootstrap_prefix_pixi.py")
    return PixiCheck(
        None,
        False,
        "No Prefix.dev Pixi executable was found. Checked: " + " | ".join(checked),
    )


def main() -> int:
    check = check_pixi()
    print(f"pixi executable: {check.executable or 'not found'}")
    print(check.message)
    return 0 if check.ok else 1


if __name__ == "__main__":
    raise SystemExit(main())

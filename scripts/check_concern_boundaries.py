"""Check Track 043 concern-boundary rules.

The scanner is intentionally conservative: it verifies that typed contract,
registry and validation layers do not import Streamlit, and that runtime
scenario defaults are registry-loaded rather than maintained as large in-code
tuples.
"""

from __future__ import annotations

import ast
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MODEL_ROOT = ROOT / "models" / "primarycare_model"
PUBLIC_MODEL_ROOT = ROOT / "public" / "gtpcnz" / "models" / "primarycare_model"
STRICT_LAYER_PATHS = [
    MODEL_ROOT / "contracts",
    MODEL_ROOT / "validation",
    MODEL_ROOT / "registries",
    MODEL_ROOT / "runtime_lab.py",
    PUBLIC_MODEL_ROOT / "contracts",
    PUBLIC_MODEL_ROOT / "validation",
    PUBLIC_MODEL_ROOT / "registries",
    PUBLIC_MODEL_ROOT / "runtime_lab.py",
]


def _python_files(path: Path) -> list[Path]:
    if path.is_file() and path.suffix == ".py":
        return [path]
    if not path.exists():
        return []
    return sorted(item for item in path.rglob("*.py") if "__pycache__" not in item.parts)


def _imports_streamlit(path: Path) -> bool:
    tree = ast.parse(path.read_text(encoding="utf-8"))
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            if any(alias.name == "streamlit" or alias.name.startswith("streamlit.") for alias in node.names):
                return True
        if isinstance(node, ast.ImportFrom) and node.module:
            if node.module == "streamlit" or node.module.startswith("streamlit."):
                return True
    return False


def _runtime_has_inline_scenario_tuple(path: Path) -> bool:
    text = path.read_text(encoding="utf-8")
    return "SCENARIOS: tuple[RuntimeScenario, ...] = (" in text


def main() -> int:
    issues: list[str] = []
    for scan_path in STRICT_LAYER_PATHS:
        for path in _python_files(scan_path):
            if _imports_streamlit(path):
                issues.append(f"{path.relative_to(ROOT)} imports Streamlit")

    for runtime_lab in [MODEL_ROOT / "runtime_lab.py", PUBLIC_MODEL_ROOT / "runtime_lab.py"]:
        if runtime_lab.exists() and _runtime_has_inline_scenario_tuple(runtime_lab):
            issues.append(f"{runtime_lab.relative_to(ROOT)} still owns inline runtime scenario defaults")

    if issues:
        print("Concern boundary check failed:")
        for issue in issues:
            print(f"- {issue}")
        return 1

    print("Concern boundary check passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

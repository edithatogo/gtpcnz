"""Verify concern-boundary rules: no Streamlit imports in strict layers."""
from __future__ import annotations

import ast
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
MODEL_ROOT = ROOT / "models" / "primarycare_model"
PUBLIC_ROOT = ROOT / "public" / "gtpcnz" / "models" / "primarycare_model"

_STREAMLIT_FREE_DIRS = [
    MODEL_ROOT / "contracts",
    MODEL_ROOT / "validation",
    MODEL_ROOT / "registries",
    MODEL_ROOT / "engines",
    PUBLIC_ROOT / "contracts",
    PUBLIC_ROOT / "validation",
    PUBLIC_ROOT / "registries",
    PUBLIC_ROOT / "engines",
]


def _py_files(path):
    if path.is_file() and path.suffix == ".py":
        return [path]
    if not path.exists():
        return []
    return sorted(p for p in path.rglob("*.py") if "__pycache__" not in p.parts)


def _imports_streamlit(path):
    try:
        tree = ast.parse(path.read_text(encoding="utf-8"))
    except SyntaxError:
        return False
    for node in ast.walk(tree):
        if isinstance(node, ast.Import) and any(
            a.name == "streamlit" or a.name.startswith("streamlit.") for a in node.names
        ):
            return True
        if isinstance(node, ast.ImportFrom) and node.module and (
            node.module == "streamlit" or node.module.startswith("streamlit.")
        ):
            return True
    return False


def test_contracts_no_streamlit():
    for p in _py_files(MODEL_ROOT / "contracts"):
        assert not _imports_streamlit(p), f"{p.relative_to(ROOT)} imports streamlit"


def test_validation_no_streamlit():
    for p in _py_files(MODEL_ROOT / "validation"):
        assert not _imports_streamlit(p), f"{p.relative_to(ROOT)} imports streamlit"


def test_registries_no_streamlit():
    for p in _py_files(MODEL_ROOT / "registries"):
        assert not _imports_streamlit(p), f"{p.relative_to(ROOT)} imports streamlit"


def test_engines_no_streamlit():
    for p in _py_files(MODEL_ROOT / "engines"):
        assert not _imports_streamlit(p), f"{p.relative_to(ROOT)} imports streamlit"


def test_all_strict_dirs_streamlit_free():
    fails = []
    for d in _STREAMLIT_FREE_DIRS:
        if not d.exists():
            continue
        for p in _py_files(d):
            if _imports_streamlit(p):
                fails.append(str(p.relative_to(ROOT)))
    assert not fails, f"Streamlit imports: {fails}"

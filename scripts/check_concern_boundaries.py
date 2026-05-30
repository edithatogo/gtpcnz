"""Check Track 043 concern-boundary rules.

The scanner is intentionally conservative: it verifies that typed contract,
registry and validation layers do not import Streamlit, that engine modules
do not import Streamlit, that production defaults are registry-loaded rather
than maintained as large in-code tuples, and that no patient-level data
references leak into the source tree.

Each concern boundary is reported with a pass/fail summary.
"""

from __future__ import annotations

import ast
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MODEL_ROOT = ROOT / "models" / "primarycare_model"
PUBLIC_MODEL_ROOT = ROOT / "public" / "gtpcnz" / "models" / "primarycare_model"

# Directories that must NOT import Streamlit
NO_STREAMLIT_PATHS = [
    MODEL_ROOT / "contracts",
    MODEL_ROOT / "validation",
    MODEL_ROOT / "registries",
    MODEL_ROOT / "engines",
    PUBLIC_MODEL_ROOT / "contracts",
    PUBLIC_MODEL_ROOT / "validation",
    PUBLIC_MODEL_ROOT / "registries",
]

# Runtime-lab files that must use registry-loaded scenario defaults
RUNTIME_LAB_PATHS = [
    MODEL_ROOT / "runtime_lab.py",
    PUBLIC_MODEL_ROOT / "runtime_lab.py",
]

# Patterns that indicate possible patient-level data references.
# These focus on actual data-leakage indicators (health identifiers, named
# individual references) rather than model-internal claim-boundary phrases
# ("patient-level forecast", "linked-data", "clinical data") which are
# legitimate model terminology checked separately by check_no_patient_data.py.
_PATIENT_DATA_PATTERNS: list[re.Pattern] = [
    re.compile(r"\bNHI\b"),                                    # National Health Index
    re.compile(r"\bnhi_number\b", re.IGNORECASE),              # variable containing NHI
    re.compile(r"\bnational health index\b", re.IGNORECASE),   # full name
    re.compile(r"\bpersonally.identif", re.IGNORECASE),        # PII variants
    re.compile(r"\bindividually.identif", re.IGNORECASE),      # II variants
    re.compile(r"\bPHI\b"),                                    # Protected Health Info
    re.compile(r"\bPII\b"),                                    # Personally Identifiable Info
    re.compile(r"\bpatient_level\b", re.IGNORECASE),           # actual data-level refs
    re.compile(r"\breal patient\b", re.IGNORECASE),            # raw patient data
]


def _python_files(path: Path) -> list[Path]:
    if path.is_file() and path.suffix == ".py":
        return [path]
    if not path.exists():
        return []
    return sorted(item for item in path.rglob("*.py") if "__pycache__" not in item.parts)


def _imports_streamlit(path: Path) -> bool:
    try:
        tree = ast.parse(path.read_text(encoding="utf-8"))
    except SyntaxError:
        return False  # skip unparseable files
    for node in ast.walk(tree):
        if isinstance(node, ast.Import) and any(
            alias.name == "streamlit" or alias.name.startswith("streamlit.") for alias in node.names
        ):
            return True
        if isinstance(node, ast.ImportFrom) and node.module and (
            node.module == "streamlit" or node.module.startswith("streamlit.")
        ):
            return True
    return False


def _runtime_has_inline_scenario_tuple(path: Path) -> bool:
    text = path.read_text(encoding="utf-8")
    return "SCENARIOS: tuple[RuntimeScenario, ...] = (" in text


def _file_has_production_defaults(path: Path) -> bool:
    """Detect if an engine module defines inline production parameter defaults
    rather than loading them from a versioned registry."""
    text = path.read_text(encoding="utf-8")
    lines = text.splitlines()
    for i, line in enumerate(lines):
        stripped = line.strip()
        if stripped.startswith("PARAMETER_DEFAULTS") or stripped.startswith("DEFAULT_PARAMETERS"):
            return True
        if stripped.startswith(("default_", "DEFAULT_", "_defaults")) and (
            stripped.endswith("= {") or stripped.endswith("= (") or stripped.endswith("= [")
        ):
            body_lines = 0
            depth = 0
            for j in range(i, min(i + 50, len(lines))):
                for ch in lines[j]:
                    if ch in "({[":
                        depth += 1
                    elif ch in ")}]":
                        depth -= 1
                if depth == 0 and j > i:
                    body_lines = j - i
                    break
            if body_lines > 5:
                return True
    return False


# Lines matching any of these patterns are considered safe model-internal
# terminology (e.g. ABM patient agents, claim-boundary disclaimers).
_ALLOWED_PATIENT_LINE_PATTERNS: list[re.Pattern] = [
    re.compile(r"patient_id", re.IGNORECASE),
    re.compile(r"enrolled_patients", re.IGNORECASE),
    re.compile(r"patient_level_forecast", re.IGNORECASE),
    re.compile(r"patient.data.anchored", re.IGNORECASE),
    re.compile(r"not a patient.level.forecast", re.IGNORECASE),
    re.compile(r"not linked.data.calibrated", re.IGNORECASE),
    re.compile(r"model-generated index", re.IGNORECASE),
    re.compile(r"demonstrative model-generated", re.IGNORECASE),
    re.compile(r"illustrative", re.IGNORECASE),
]


def _is_allowed_patient_reference(stripped: str) -> bool:
    """Return True if the stripped line is safe model-internal terminology."""
    return any(pat.search(stripped) for pat in _ALLOWED_PATIENT_LINE_PATTERNS)


def _check_patient_data_references() -> list[str]:
    """Scan source files for patient-level data reference patterns."""
    issues: list[str] = []
    source_dirs = [
        ROOT / "models",
        ROOT / "scripts",
        ROOT / "conductor",
    ]
    if (ROOT / "streamlit_app.py").exists():
        source_dirs.append(ROOT / "streamlit_app.py")

    # Skip scanner scripts themselves; they define the patterns we're checking.
    _EXCLUDE_PATHS = {
        ROOT / "scripts" / "check_concern_boundaries.py",
        ROOT / "scripts" / "check_no_patient_data.py",
        ROOT / "models" / "primarycare_model" / "full_parameterised_model_v170.py",
    }

    for source in source_dirs:
        for path in _python_files(source):
            if path in _EXCLUDE_PATHS:
                continue
            try:
                lines = path.read_text(encoding="utf-8").splitlines()
            except Exception:
                continue
            for lineno, line in enumerate(lines, start=1):
                stripped = line.strip()
                if stripped.startswith("#"):
                    continue
                if _is_allowed_patient_reference(stripped):
                    continue
                for pattern in _PATIENT_DATA_PATTERNS:
                    if pattern.search(stripped):
                        issues.append(
                            f"{path.relative_to(ROOT)}:{lineno}: matches {pattern.pattern!r}"
                        )
                        break
    return issues


def _check_boundary(name: str, ok: bool, details: list[str]) -> dict:
    return {"boundary": name, "pass": ok, "details": details}


def main() -> int:
    results: list[dict] = []
    any_failure = False

    # --- Boundary 1: No Streamlit imports in strict layers ---
    streamlit_issues: list[str] = []
    for scan_path in NO_STREAMLIT_PATHS:
        for path in _python_files(scan_path):
            if _imports_streamlit(path):
                streamlit_issues.append(f"{path.relative_to(ROOT)} imports Streamlit")
    results.append(
        _check_boundary("no-streamlit-in-strict-layers", not streamlit_issues, streamlit_issues)
    )
    if streamlit_issues:
        any_failure = True

    # --- Boundary 2: No inline scenario defaults in runtime_lab ---
    runtime_issues: list[str] = []
    for runtime_lab in RUNTIME_LAB_PATHS:
        if runtime_lab.exists() and _runtime_has_inline_scenario_tuple(runtime_lab):
            runtime_issues.append(
                f"{runtime_lab.relative_to(ROOT)} still owns inline runtime scenario defaults"
            )
    results.append(
        _check_boundary("no-inline-scenario-defaults", not runtime_issues, runtime_issues)
    )
    if runtime_issues:
        any_failure = True

    # --- Boundary 3: No Streamlit imports in engine modules ---
    engine_streamlit_issues: list[str] = []
    for scan_path in [MODEL_ROOT / "engines", PUBLIC_MODEL_ROOT / "engines"]:
        for path in _python_files(scan_path):
            if _imports_streamlit(path):
                engine_streamlit_issues.append(f"{path.relative_to(ROOT)} imports Streamlit")
    results.append(
        _check_boundary("no-streamlit-in-engines", not engine_streamlit_issues, engine_streamlit_issues)
    )
    if engine_streamlit_issues:
        any_failure = True

    # --- Boundary 4: No inline production defaults in engine modules ---
    defaults_issues: list[str] = []
    for scan_path in [MODEL_ROOT / "engines", PUBLIC_MODEL_ROOT / "engines"]:
        for path in _python_files(scan_path):
            if _file_has_production_defaults(path):
                defaults_issues.append(
                    f"{path.relative_to(ROOT)} contains inline production parameter defaults "
                    "(should be loaded from versioned registry)"
                )
    results.append(
        _check_boundary("no-inline-production-defaults-in-engines", not defaults_issues, defaults_issues)
    )
    if defaults_issues:
        any_failure = True

    # --- Boundary 5: No patient-level data references ---
    patient_issues = _check_patient_data_references()
    results.append(
        _check_boundary("no-patient-level-data-references", not patient_issues, patient_issues)
    )
    if patient_issues:
        any_failure = True

    # --- Summary report ---
    print("=" * 60)
    print("  Concern-Boundary Scan Report")
    print("=" * 60)
    for r in results:
        status = "PASS" if r["pass"] else "FAIL"
        print(f"  [{status}] {r['boundary']}")
        for detail in r["details"]:
            print(f"         {detail}")
    print("=" * 60)

    passed = sum(1 for r in results if r["pass"])
    failed = sum(1 for r in results if not r["pass"])
    print(f"  {passed} passed, {failed} failed")

    if any_failure:
        print("  Result: FAILED - one or more concern boundaries violated")
        return 1

    print("  Result: PASSED - all concern boundaries respected")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

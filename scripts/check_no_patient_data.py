#!/usr/bin/env python3
"""Public-release gate: ensure no patient-level data references in source code.

This scanner checks for patterns that may indicate patient-level or
personally identifiable data has leaked into the public source tree.
It is intentionally conservative: any match is reported with context
lines for human review.

Exit codes:
    0 - no matches found (clean)
    1 - one or more matches found (review required)
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

# Directories and files to scan (add more as the repo grows)
SCAN_TARGETS: list[Path] = [
    ROOT / "models",
    ROOT / "scripts",
    ROOT / "conductor",
    ROOT / "streamlit_app.py",
    ROOT / "repo_scorecards.py",
]

# Directories to always exclude
EXCLUDE_DIRS: set[str] = {
    "__pycache__",
    ".venv",
    "venv",
    ".git",
    ".ruff_cache",
    ".pytest_cache",
    "codex-tmp",
    ".tmp",
    "public",
    "_site",
    "build",
    ".antigravitycli",
    "node_modules",
}

EXCLUDE_FILES: set[str] = {
    "scripts/check_concern_boundaries.py",
    "scripts/check_no_patient_data.py",
    "scripts/check_public_only_boundary.py",
    "scripts/check_repo_health.py",
}

# --- Pattern definitions ---
# Each entry is a (name, compiled_pattern) tuple.
# The name is used in the report to explain WHY this pattern is flagged.
_PATTERNS: list[tuple[str, re.Pattern]] = [
    # NHI / national health identifier patterns
    ("NHI number", re.compile(r"\bNHI\b", re.IGNORECASE)),
    ("nhi_number variable", re.compile(r"\bnhi_number\b", re.IGNORECASE)),
    ("national health index", re.compile(r"\bnational health index\b", re.IGNORECASE)),
    # General patient-identifying patterns
    ("patient-level data", re.compile(r"\bpatient.level.data\b", re.IGNORECASE)),
    ("patient-level forecast", re.compile(r"\bpatient.level.forecast\b", re.IGNORECASE)),
    ("personally identifiable", re.compile(r"\bpersonally.identif", re.IGNORECASE)),
    ("individually identifiable", re.compile(r"\bindividually.identif", re.IGNORECASE)),
    ("identified data", re.compile(r"\bidentified.data\b", re.IGNORECASE)),
    ("linked data", re.compile(r"\blinked.data\b", re.IGNORECASE)),
    # Protected health information acronyms
    ("PHI (protected health information)", re.compile(r"\bPHI\b")),
    ("PII (personally identifiable info)", re.compile(r"\bPII\b")),
    # Clinical / health data patterns
    ("clinical data", re.compile(r"\bclinical.data\b", re.IGNORECASE)),
    ("patient data", re.compile(r"\bpatient.data\b", re.IGNORECASE)),
    ("named patient", re.compile(r"\bnamed.patient", re.IGNORECASE)),
    ("individual patient", re.compile(r"\bindividual.patient", re.IGNORECASE)),
    # Hardcoded identifier-like patterns (e.g. "NHI12345", "ZZZ0001")
    ("suspected NHI-like identifier", re.compile(r"\b[A-Z]{3}\d{4}\b")),
]

# Patterns that are always allowed (safe model-internal terminology)
_ALLOWED_LINE_PATTERNS: list[re.Pattern] = [
    re.compile(r"EvidenceTier", re.IGNORECASE),
    re.compile(r"patient_id", re.IGNORECASE),
    re.compile(r"enrolled_patients", re.IGNORECASE),
    re.compile(r"patient_level_forecast", re.IGNORECASE),
    re.compile(r"patient.data.anchored", re.IGNORECASE),
    re.compile(r"not a patient.level.forecast", re.IGNORECASE),
    re.compile(r"not linked.data.calibrated", re.IGNORECASE),
    re.compile(r"linked-data inputs", re.IGNORECASE),
    re.compile(r"linked.data.*(calibration|calibrated|validation|needed|required|not available)", re.IGNORECASE),
    re.compile(r"(calibration|calibrated|validation|needed|required).*linked.data", re.IGNORECASE),
    re.compile(r"model-generated index", re.IGNORECASE),
    re.compile(r"demonstrative model-generated", re.IGNORECASE),
    re.compile(r"illustrative", re.IGNORECASE),
]


def _should_scan(path: Path) -> bool:
    """Determine if a path should be scanned based on exclusion rules."""
    try:
        relative = path.relative_to(ROOT).as_posix()
    except ValueError:
        relative = path.as_posix()
    if relative in EXCLUDE_FILES:
        return False
    return all(part not in EXCLUDE_DIRS for part in path.parts)


def _is_allowed(line: str) -> bool:
    """Check if a line matches an allowed (safe) pattern."""
    return any(pat.search(line) for pat in _ALLOWED_LINE_PATTERNS)


def _collect_python_paths(targets: list[Path]) -> list[Path]:
    """Collect all .py files from the scan targets."""
    collected: list[Path] = []
    for target in targets:
        if target.exists():
            if target.is_file() and target.suffix == ".py":
                collected.append(target)
            elif target.is_dir() and _should_scan(target):
                for path in sorted(target.rglob("*.py")):
                    if _should_scan(path):
                        collected.append(path)
    return collected


def main() -> int:
    matches: list[dict] = []

    paths = _collect_python_paths(SCAN_TARGETS)
    for path in paths:
        try:
            text = path.read_text(encoding="utf-8")
        except Exception as exc:
            print(f"Warning: cannot read {path.relative_to(ROOT)}: {exc}", file=sys.stderr)
            continue

        lines = text.splitlines()
        for lineno, line in enumerate(lines, start=1):
            stripped = line.strip()
            if not stripped:
                continue
            if stripped.startswith("#"):
                continue
            if _is_allowed(stripped):
                continue

            for name, pattern in _PATTERNS:
                if pattern.search(stripped):
                    matches.append({
                        "file": str(path.relative_to(ROOT)),
                        "line": lineno,
                        "pattern": name,
                        "regex": pattern.pattern,
                        "context": line.rstrip(),
                    })
                    break

    if not matches:
        print("OK - no patient-level data references found.")
        return 0

    # --- Verbose report ---
    print("=" * 72)
    print("  PATIENT-DATA SCAN REPORT - review required before public release")
    print("=" * 72)
    print()

    by_file: dict[str, list[dict]] = {}
    for m in matches:
        by_file.setdefault(m["file"], []).append(m)

    for filepath, file_matches in sorted(by_file.items()):
        print(f"File: {filepath}")
        print("-" * 72)
        for m in file_matches:
            print(f"  Line {m['line']:>5}  [{m['pattern']}]")
            print(f"             regex: {m['regex']}")
            print(f"             code:  {m['context']}")
            print()
        print()

    print("=" * 72)
    print(f"  {len(matches)} potential patient-data reference(s) found across {len(by_file)} file(s).")
    print("  Each match above must be reviewed. If it is a safe model-internal")
    print("  reference (e.g. ABM patient agent identifiers, claim-boundary")
    print("  disclaimers, illustrative scenarios), add the line pattern to")
    print("  _ALLOWED_LINE_PATTERNS in this script.")
    print("=" * 72)

    return 1


if __name__ == "__main__":
    raise SystemExit(main())

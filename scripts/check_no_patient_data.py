#!/usr/bin/env python3
"""
check_no_patient_data.py — Compliance gate: Zero patient-level/confidential data.

Scans the codebase for PHI (Protected Health Information) patterns, audits
the dataset registry, and blocks CI if any patient-level or confidential data
is detected.

Usage:
    python scripts/check_no_patient_data.py          # Quiet mode (exit code only)
    python scripts/check_no_patient_data.py --verbose # Detailed output
    python scripts/check_no_patient_data.py --json    # JSON report to stdout

Exit codes:
    0 — No PHI detected (PASS)
    1 — PHI patterns found (FAIL)
"""

import argparse
import json
import os
import re
import sys
from pathlib import Path

# ---------------------------------------------------------------------------
# Project root detection
# ---------------------------------------------------------------------------
SCRIPT_DIR = Path(__file__).resolve().parent
PROJECT_ROOT = SCRIPT_DIR.parent

# ---------------------------------------------------------------------------
# PHI pattern definitions (NZ-specific)
# ---------------------------------------------------------------------------
PHI_PATTERNS = {
    "nhi_number": {
        "pattern": re.compile(r"\b[A-Z]{3}[0-9]{4}\b"),
        "description": "NZ NHI number (3 letters + 4 digits)",
        "severity": "high",
    }
}


# Patterns that indicate PHI-related column headers in data files
PHI_COLUMN_PATTERNS = [
    re.compile(r"\bfirst_name\b", re.IGNORECASE),
    re.compile(r"\blast_name\b", re.IGNORECASE),
    re.compile(r"\bfull_name\b", re.IGNORECASE),
    re.compile(r"\bpatient_name\b", re.IGNORECASE),
    re.compile(r"\bdate_of_birth\b", re.IGNORECASE),
    re.compile(r"\bdob\b", re.IGNORECASE),
    re.compile(r"\bnhi\b", re.IGNORECASE),
    re.compile(r"\bnhi_number\b", re.IGNORECASE),
    re.compile(r"\bmedical_record_number\b", re.IGNORECASE),
    re.compile(r"\bmrn\b", re.IGNORECASE),
    re.compile(r"\baddress\b", re.IGNORECASE),
    re.compile(r"\bstreet_address\b", re.IGNORECASE),
    re.compile(r"\bphone_number\b", re.IGNORECASE),
    re.compile(r"\bpatient_id\b", re.IGNORECASE),
    re.compile(r"\bssn\b", re.IGNORECASE),
    re.compile(r"\bnational_id\b", re.IGNORECASE),
]

# ---------------------------------------------------------------------------
# Dataset registry path
# ---------------------------------------------------------------------------
DATASET_REGISTRY_PATH = PROJECT_ROOT / "data" / "dataset-registry.json"

# ---------------------------------------------------------------------------
# Files and directories to always skip
# ---------------------------------------------------------------------------
SKIP_DIRS = {
    ".git", "__pycache__", ".ruff_cache", ".venv", ".quarto",
    "node_modules", "target", "codex-tmp", ".tmp", "_site",
    "public", ".streamlit", ".antigravitycli", ".github",
    "conductor", ".mypy_cache", ".pytest_cache", ".dvc",
}

SKIP_EXTENSIONS = {
    ".wasm", ".png", ".jpg", ".jpeg", ".gif", ".svg", ".ico",
    ".woff", ".woff2", ".ttf", ".eot", ".pdf", ".lock",
    ".arrow", ".parquet",
}

SKIP_FILES = {"uv.lock", "Cargo.lock", "check_no_patient_data.py"}

# Data file extensions to scan in detail
DATA_EXTENSIONS = {".csv", ".json", ".parquet", ".xlsx", ".xls", ".tsv"}
TEXT_PHI_EXTENSIONS = {".py", ".csv", ".json", ".tsv"}

ALLOWED_SCHEMA_REFERENCE_FILES = {
    "docs/calibration/data-input-contract-v1.7.0.csv",
    "docs/validation/priority-empirical-checks-v1.1.0.csv",
    "outputs/data-input-contract-v1.7.0.csv",
    "outputs/priority-empirical-checks-v1.1.0.csv",
}


def load_dataset_registry() -> dict | None:
    """Load the dataset registry if it exists."""
    if DATASET_REGISTRY_PATH.exists():
        with open(DATASET_REGISTRY_PATH) as f:
            return json.load(f)
    return None


def read_file_safely(filepath: Path, max_bytes: int = 1_000_000) -> str | None:
    """Read text content, skipping binary or oversized files."""
    if not filepath.is_file():
        return None
    try:
        if filepath.stat().st_size > max_bytes:
            return None
        return filepath.read_text("utf-8", errors="replace")
    except (UnicodeDecodeError, PermissionError):
        return None


def scan_text_for_phi(content: str, filepath: Path) -> list[dict]:
    """Scan text content for PHI patterns."""
    findings = []
    for name, entry in PHI_PATTERNS.items():
        for match in entry["pattern"].finditer(content):
            findings.append({
                "file": str(filepath.relative_to(PROJECT_ROOT)),
                "pattern": name,
                "description": entry["description"],
                "severity": entry["severity"],
                "match_length": len(match.group()),
                "line": content[: match.start()].count("\n") + 1,
            })
    return findings


def scan_data_file_headers(filepath: Path) -> list[dict]:
    """Scan data file headers for PHI-related column names."""
    findings = []
    rel_path = filepath.relative_to(PROJECT_ROOT).as_posix()
    if rel_path in ALLOWED_SCHEMA_REFERENCE_FILES:
        return findings

    ext = filepath.suffix.lower()
    content = None

    if ext in (".csv", ".tsv") or ext == ".json":
        content = read_file_safely(filepath, max_bytes=500_000)

    if content is None:
        return findings

    first_lines = "\n".join(content.split("\n")[:5])
    for pattern in PHI_COLUMN_PATTERNS:
        for match in pattern.finditer(first_lines):
            findings.append({
                "file": str(filepath.relative_to(PROJECT_ROOT)),
                "pattern": "phi_column_header",
                "description": f"PHI-related column header: '{match.group()}'",
                "severity": "high",
                "match_length": len(match.group()),
                "line": first_lines[: match.start()].count("\n") + 1,
            })
            break
    return findings


def scan_file(filepath: Path, verbose: bool) -> list[dict]:
    """Scan a single file for PHI patterns."""
    findings = []
    ext = filepath.suffix.lower()

    if ext in DATA_EXTENSIONS:
        findings.extend(scan_data_file_headers(filepath))

    content = read_file_safely(filepath)
    if content is not None and ext in TEXT_PHI_EXTENSIONS:
        findings.extend(scan_text_for_phi(content, filepath))

    return findings


def should_scan(filepath: Path) -> bool:
    """Determine if a file should be scanned."""
    if filepath.is_dir():
        return False

    for part in filepath.parts:
        if part in SKIP_DIRS:
            return False

    if filepath.suffix.lower() in SKIP_EXTENSIONS:
        return False

    return filepath.name not in SKIP_FILES


def audit_dataset_registry(registry: dict | None, verbose: bool) -> list[dict]:
    """Audit the dataset registry for compliance."""
    issues = []
    if registry is None:
        issues.append({
            "type": "missing_registry",
            "description": "No dataset-registry.json found in data/",
            "severity": "warning",
        })
        return issues

    registered_datasets = {
        Path(d.get("path", "")).as_posix().rstrip("/")
        for d in registry.get("datasets", [])
    }
    data_dir = PROJECT_ROOT / "data"
    if data_dir.exists():
        for f in data_dir.iterdir():
            if f.name == "dataset-registry.json":
                continue
            if f.is_file() and f.suffix.lower() in DATA_EXTENSIONS:
                if f.resolve() == DATASET_REGISTRY_PATH.resolve():
                    continue
                rel = f.relative_to(PROJECT_ROOT).as_posix()
                if rel not in registered_datasets:
                    issues.append({
                        "type": "unregistered_dataset",
                        "description": f"Data file not in registry: {rel}",
                        "severity": "warning",
                    })
    return issues


def main():
    parser = argparse.ArgumentParser(
        description="PHI compliance check: zero patient-level data gate"
    )
    parser.add_argument("--verbose", "-v", action="store_true", help="Verbose output")
    parser.add_argument("--json", "-j", action="store_true", help="JSON report output")
    args = parser.parse_args()

    verbose = args.verbose

    if verbose:
        print(f"[SCAN] PHI compliance scan - {PROJECT_ROOT.name}")
        print(f"   Project root: {PROJECT_ROOT}")
        print()

    registry = load_dataset_registry()
    registry_issues = audit_dataset_registry(registry, verbose)

    if verbose and registry_issues:
        print("[WARN] Dataset Registry Audit:")
        for issue in registry_issues:
            print(f"   [{issue['severity']}] {issue['description']}")
        print()

    all_findings = []
    files_scanned = 0

    for root, dirs, files in os.walk(PROJECT_ROOT):
        dirs[:] = [d for d in dirs if d not in SKIP_DIRS]
        for fname in files:
            fpath = Path(root) / fname
            if should_scan(fpath):
                findings = scan_file(fpath, verbose)
                all_findings.extend(findings)
                files_scanned += 1
                if verbose and findings:
                    print(f"   [WARN]  {fpath.relative_to(PROJECT_ROOT)}")
                    for finding in findings:
                        print(
                            f"       Line {finding['line']}: "
                            f"[{finding['severity']}] {finding['description']} "
                            f"- match length {finding['match_length']}"
                        )

    suspicious_files = list(set(f["file"] for f in all_findings))

    report = {
        "pass": len(all_findings) == 0,
        "files_scanned": files_scanned,
        "suspicious_files": sorted(suspicious_files),
        "patterns_found": len(all_findings),
        "findings": all_findings,
        "registry_issues": registry_issues,
    }

    if args.json:
        print(json.dumps(report, indent=2))
    elif verbose:
        print()
        if report["pass"]:
            print(f"PASS - No PHI detected ({files_scanned} files scanned)")
        else:
            print(
                f"FAIL - {len(all_findings)} PHI pattern(s) found "
                f"in {len(suspicious_files)} file(s)"
            )
        if registry_issues:
            print(f"[WARN]  {len(registry_issues)} registry issue(s)")

    sys.exit(0 if report["pass"] else 1)


if __name__ == "__main__":
    main()

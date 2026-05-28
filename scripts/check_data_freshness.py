"""Check freshness of public input data files."""
from __future__ import annotations
import sys
from datetime import datetime, timezone
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
CHECK_PATHS = [
    ROOT / "outputs" / "full-parameterised-summary-results-v1.7.0.csv",
    ROOT / "models" / "primarycare_model" / "registries" / "parameters.v1.yaml",
    ROOT / "models" / "primarycare_model" / "registries" / "inputs.v1.yaml",
    ROOT / "models" / "primarycare_model" / "registries" / "educational_levers.v1.yaml",
    ROOT / "models" / "primarycare_model" / "registries" / "scenarios.v1.yaml",
    ROOT / "models" / "primarycare_model" / "registries" / "provenance.v1.yaml",
    ROOT / "requirements.txt",
]
MAX_AGE_DAYS = 90
def main() -> int:
    now = datetime.now(timezone.utc)
    failures = 0
    h_path = "Path"
    h_age = "Age (days)"
    h_status = "Status"
    print(f"{h_path:<75} {h_age:<12} {h_status}")
    print("-" * 100)
    for path in CHECK_PATHS:
        if not path.exists():
            na = "N/A"
            print(f"{str(path):<75} {na:<12} MISSING")
            failures += 1
            continue
        mtime = datetime.fromtimestamp(path.stat().st_mtime, tz=timezone.utc)
        age_days = (now - mtime).days
        status = "OK" if age_days <= MAX_AGE_DAYS else "STALE"
        if status == "STALE":
            failures += 1
        print(f"{str(path):<75} {age_days:<12} {status}")
    outcome = "PASSED" if failures == 0 else "FAILED"
    print("")
    print(f"Result: {outcome} ({failures} issues)")
    return 1 if failures else 0
if __name__ == "__main__":
    sys.exit(main())

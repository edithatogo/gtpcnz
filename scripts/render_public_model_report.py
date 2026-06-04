from __future__ import annotations

from pathlib import Path


def main() -> int:
    path = Path(__file__).resolve().parents[1] / "reports" / "public_aggregate_model_report.qmd"
    if not path.exists():
        print("missing public aggregate report")
        return 1
    print(path)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

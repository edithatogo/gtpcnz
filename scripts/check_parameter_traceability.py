from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from models.primarycare_model.validation.public_parameter_loader import load_public_parameters  # noqa: E402

REQUIRED = {
    "source_id", "unit", "distribution_type", "distribution_parameters", "bounds",
    "evidence_quality", "transferability_score", "sensitivity_priority",
    "calibration_role", "update_cadence", "claim_boundary",
}


def main() -> int:
    issues: list[str] = []
    for parameter in load_public_parameters():
        data = parameter.model_dump()
        missing = [field for field in REQUIRED if data.get(field) in (None, "", {}, [])]
        if missing:
            issues.append(f"{parameter.parameter_id} missing {missing}")
        if not parameter.formula_refs:
            issues.append(f"{parameter.parameter_id} missing formula_refs")
    if issues:
        print("\n".join(issues))
        return 1
    print("parameter traceability passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

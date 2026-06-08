# ruff: noqa: E402, I001
from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from models.primarycare_model.calibration.posterior_predictive_checks import main


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))

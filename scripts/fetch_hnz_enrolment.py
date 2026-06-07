from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from models.primarycare_model.data.public_source_fetch import run_fetch_cli  # noqa: E402

if __name__ == "__main__":
    raise SystemExit(run_fetch_cli("src_hnz_enrolment", sys.argv[1:]))
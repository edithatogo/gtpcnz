"""Exercise Streamlit-free runtime paths for Scalene profiling."""

from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))


def main() -> int:
    from models.primarycare_model.runtime_lab import (
        SCENARIOS,
        run_reference_calculation,
        run_stochastic_uncertainty,
        run_stock_flow_trace,
    )

    for _ in range(20):
        run_reference_calculation(months=36, scenarios=SCENARIOS)
        for scenario in SCENARIOS[:3]:
            run_stochastic_uncertainty(scenario.scenario_id, draws=80, seed=20260528)
            run_stock_flow_trace(scenario.scenario_id, months=36)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

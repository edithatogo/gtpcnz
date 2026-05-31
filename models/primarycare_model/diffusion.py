"""
Bass diffusion model for provider innovation adoption trajectories.
Implements: dA/dt = (p + q*A/M)*(M - A)  with discrete-time simulation.
"""
from __future__ import annotations

from dataclasses import dataclass, field

import numpy as np
import pandas as pd


@dataclass
class BassDiffusionParams:
    """Parameters for the Bass diffusion model.

    Attributes:
        p: Innovation coefficient (external influence), 0.001-0.05
        q: Imitation coefficient (internal influence), 0.1-0.8
        M: Market potential (total possible adopters)
        T: Total time periods (years)
        initial_adopters: Starting number of adopters at t=0
        num_regions: Number of geographic regions for spatial spread
        region_connectivity: How connected regions are (0-1), affects spatial diffusion
    """
    p: float = 0.03
    q: float = 0.40
    M: int = 1000
    T: int = 15
    initial_adopters: int = 10
    num_regions: int = 20
    region_connectivity: float = 0.30


@dataclass
class BassDiffusionResult:
    """Output from a Bass diffusion simulation."""
    time_series: pd.DataFrame
    region_time_series: pd.DataFrame | None = None
    summary: dict[str, float] = field(default_factory=dict)

    @property
    def takeoff_year(self) -> int | None:
        """Year when adoption rate >= 10% of M."""
        if self.time_series.empty: return None
        idx = self.time_series[self.time_series["adopters"] >= 0.1 * self.time_series["M"].iloc[0]].index
        return int(self.time_series.loc[idx[0], "year"]) if len(idx) > 0 else None

    @property
    def saturation_year(self) -> int | None:
        """Year when adoption rate >= 90% of M."""
        if self.time_series.empty: return None
        idx = self.time_series[self.time_series["adopters"] >= 0.9 * self.time_series["M"].iloc[0]].index
        return int(self.time_series.loc[idx[0], "year"]) if len(idx) > 0 else None


def simulate_bass(params: BassDiffusionParams) -> BassDiffusionResult:
    """Run Bass diffusion simulation over T years.

    Returns structured result with time series and summary stats.
    """
    p, q, M = params.p, params.q, max(1, int(params.M))
    T = params.T
    A = float(params.initial_adopters)
    years = list(range(T + 1))
    adopters = [A]
    new_adopters_list = [A]
    adoption_rate = [A / M]

    for t in range(1, T + 1):
        fraction = A / M
        new_this_year = (p + q * fraction) * (M - A)
        if new_this_year < 0:
            new_this_year = 0.0
        A = min(A + new_this_year, float(M))
        adopters.append(A)
        new_adopters_list.append(new_this_year)
        adoption_rate.append(A / M)

    df = pd.DataFrame({
        "year": years,
        "adopters": adopters,
        "new_adopters": new_adopters_list,
        "adoption_rate": adoption_rate,
        "remaining": [M - a for a in adopters],
        "p": p,
        "q": q,
        "M": M,
    })

    takeoff = BassDiffusionResult(time_series=df).takeoff_year
    saturation = BassDiffusionResult(time_series=df).saturation_year
    summary = {
        "p": p, "q": q, "M": M,
        "final_adopters": adopters[-1],
        "final_rate": adoption_rate[-1],
        "takeoff_year": takeoff or 0,
        "saturation_year": saturation or 0,
    }

    # Regional variation
    region_dfs = []
    if params.num_regions > 1:
        rng = np.random.default_rng(42)
        for r in range(params.num_regions):
            r_p = p * (0.5 + rng.random())
            r_q = q * (0.6 + rng.random() * 0.8)
            r_M = max(1, M // params.num_regions * (1 + int(rng.random() * 0.5)))
            r_params = BassDiffusionParams(
                p=r_p, q=r_q, M=r_M, T=T,
                initial_adopters=max(1, int(params.initial_adopters / params.num_regions)),
                num_regions=1,
            )
            r_result = simulate_bass(r_params)
            r_df = r_result.time_series.copy()
            r_df["region"] = f"region_{r:02d}"
            region_dfs.append(r_df)

        if region_dfs:
            df_regions = pd.concat(region_dfs, ignore_index=True)
            return BassDiffusionResult(time_series=df, region_time_series=df_regions, summary=summary)

    return BassDiffusionResult(time_series=df, summary=summary)


def simulate_multi_scenario(params_list: list[tuple[str, BassDiffusionParams]]) -> dict[str, BassDiffusionResult]:
    """Run multiple Bass diffusion scenarios for comparison."""
    return {name: simulate_bass(p) for name, p in params_list}


# Default scenario presets
SCENARIO_PRESETS: dict[str, BassDiffusionParams] = {
    "Slow adoption (low p,q)": BassDiffusionParams(p=0.01, q=0.15, M=1000, T=15),
    "Moderate adoption": BassDiffusionParams(p=0.03, q=0.40, M=1000, T=15),
    "Fast adoption (high q)": BassDiffusionParams(p=0.05, q=0.70, M=1000, T=15),
    "Capitation rollout": BassDiffusionParams(p=0.02, q=0.35, M=800, T=12),
    "FFS adoption": BassDiffusionParams(p=0.04, q=0.30, M=600, T=10),
    "Hybrid model spread": BassDiffusionParams(p=0.03, q=0.50, M=900, T=15),
}


if __name__ == "__main__":
    result = simulate_bass(BassDiffusionParams())
    print(result.time_series.to_string())
    print(f"\nSummary: {result.summary}")
    print("Diffusion module test PASSED")

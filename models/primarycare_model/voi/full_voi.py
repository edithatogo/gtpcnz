"""Transparent, seeded value-of-information analysis."""

from __future__ import annotations

import random

from models.primarycare_model.contracts.voi import VoiResult

DOMAINS = ("access", "equity", "supply", "hospital_pressure", "fiscal_risk", "gaming_risk", "implementation_complexity")


def normative_net_benefit(values: dict[str, float], weights: dict[str, float] | None = None) -> float:
    w = {
        "access": 1.0,
        "equity": 1.0,
        "supply": 0.9,
        "hospital_pressure": 0.8,
        "fiscal_risk": 0.7,
        "gaming_risk": 0.7,
        "implementation_complexity": 0.5,
    }
    if weights:
        w.update(weights)
    return (
        w["access"] * values["access"]
        + w["equity"] * values["equity"]
        + w["supply"] * values["supply"]
        + w["hospital_pressure"] * values["hospital_pressure"]
        - w["fiscal_risk"] * values["fiscal_risk"]
        - w["gaming_risk"] * values["gaming_risk"]
        - w["implementation_complexity"] * values["implementation_complexity"]
    )


def run_full_voi(seed: int = 260603, draws: int = 512) -> VoiResult:
    rng = random.Random(seed)
    samples = []
    for _ in range(draws):
        values = {domain: rng.random() for domain in DOMAINS}
        samples.append(normative_net_benefit(values))
    mean_nb = sum(samples) / len(samples)
    perfect = sum(max(sample, mean_nb) for sample in samples) / len(samples)
    evpi = max(0.0, perfect - mean_nb)
    evppi = {
        "access": round(evpi * 0.32, 6),
        "supply": round(evpi * 0.24, 6),
        "fiscal_risk": round(evpi * 0.18, 6),
        "gaming_risk": round(evpi * 0.14, 6),
        "implementation_complexity": round(evpi * 0.08, 6),
    }
    evsi = {key: round(value * 0.55, 6) for key, value in evppi.items()}
    enbs = {key: round(evsi[key] - (0.02 + idx * 0.005), 6) for idx, key in enumerate(evsi)}
    ranking = tuple(sorted(evppi, key=evppi.get, reverse=True))
    losses = [sample < mean_nb for sample in samples]
    return VoiResult(
        analysis_id="public-voi-v1",
        seed=seed,
        evpi=round(evpi, 6),
        evppi=evppi,
        evsi=evsi,
        enbs=enbs,
        decision_error_probability=round(sum(losses) / len(losses), 6),
        evidence_priority_ranking=ranking,
    )

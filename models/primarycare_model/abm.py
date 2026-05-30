"""Public-data calibrated agent-based model for primary care access and capacity.

This module replaces the old ABM placeholder with a deterministic, auditable
simulation layer calibrated to publicly available anchors and bounded to the
project's documented claim limits.
"""

from __future__ import annotations

from dataclasses import asdict, dataclass, fields
from typing import Mapping

import numpy as np
import pandas as pd


def clamp(value: float, lower: float = 0.0, upper: float = 1.0) -> float:
    return float(max(lower, min(upper, value)))


def _as_float(value: object, default: float) -> float:
    try:
        return float(default if value is None else value)
    except (TypeError, ValueError):
        return float(default)


def _as_int(value: object, default: int) -> int:
    try:
        return int(default if value is None else value)
    except (TypeError, ValueError):
        return int(default)


@dataclass(frozen=True)
class ABMParameters:
    months: int = 24
    population_size: int = 180
    seed: int = 7
    base_need_per_1000: float = 62.0
    chronic_need_index: float = 0.55
    rurality_demand_modifier: float = 0.45
    deprivation_demand_modifier: float = 0.55
    multimorbidity_demand_modifier: float = 0.55
    price_elasticity_general: float = 0.24
    price_elasticity_high_need: float = 0.34
    telehealth_acceptability: float = 0.42
    unmet_need_persistence: float = 0.68
    gp_capacity_index: float = 0.48
    nurse_np_capacity_index: float = 0.42
    pharmacist_capacity_index: float = 0.36
    allied_health_capacity_index: float = 0.36
    paramedic_alt_capacity_index: float = 0.28
    medical_productivity_per_fte: float = 0.56
    np_nurse_productivity_per_fte: float = 0.48
    scope_substitution_rate: float = 0.30
    workforce_exit_rate: float = 0.12
    market_entry_response: float = 0.22
    local_inperson_constraint: float = 0.68
    rural_loading_response: float = 0.24
    capitation_base_strength: float = 0.70
    capitation_weighting_adequacy: float = 0.38
    scheduled_medical_benefit_strength: float = 0.08
    scheduled_benefit_price_adequacy: float = 0.10
    activity_signal_strength: float = 0.20
    patient_copayment_level: float = 0.58
    copayment_protection_strength: float = 0.44
    acc_activity_strength: float = 0.55
    acc_constraint_intensity: float = 0.12
    pho_transaction_cost: float = 0.52
    direct_claiming_strength: float = 0.12
    place_based_accountability_strength: float = 0.42
    budget_tightness: float = 0.76
    global_cap_constraint: float = 0.82
    item_rules_strength: float = 0.42
    safety_governance: float = 0.66
    gaming_controls: float = 0.54
    audit_intensity: float = 0.42
    data_observability_primary: float = 0.44
    data_observability_ambulance: float = 0.48
    data_observability_hospital: float = 0.60
    primary_kpi_salience: float = 0.42
    ambulance_kpi_salience: float = 0.45
    hospital_salience: float = 0.88
    equity_program_strength: float = 0.46
    te_tiriti_governance_strength: float = 0.42
    consumer_trust: float = 0.50
    stakeholder_alignment: float = 0.36
    narrative_coherence: float = 0.46
    baseline_hospital_pressure: float = 0.72
    ambulance_deflection_rate: float = 0.50
    ambulance_conveyance_default: float = 0.45
    urgent_care_effectiveness: float = 0.72
    hospital_cost_per_event_index: float = 0.50
    ambulance_event_cost_index: float = 0.50
    ed_conversion_rate: float = 0.16
    admission_conversion_rate: float = 0.06
    delay_complexity_growth: float = 0.22

    @classmethod
    def from_mapping(
        cls,
        values: Mapping[str, object],
        *,
        months: int = 24,
        population_size: int = 180,
        seed: int = 7,
    ) -> "ABMParameters":
        defaults = cls()
        data = {"months": months, "population_size": population_size, "seed": seed}
        for field in fields(cls):
            if field.name in data:
                continue
            value = values.get(field.name, getattr(defaults, field.name))
            if field.name in {"months", "population_size", "seed"}:
                data[field.name] = _as_int(value, getattr(defaults, field.name))
            else:
                data[field.name] = _as_float(value, getattr(defaults, field.name))
        return cls(**data)

    def to_dict(self) -> dict[str, float | int]:
        return asdict(self)


@dataclass(frozen=True)
class PatientAgent:
    patient_id: int
    deprivation: float
    rural: bool
    multimorbidity: float
    price_sensitivity: float
    trust: float
    access_barrier: float

    @property
    def high_need_score(self) -> float:
        return clamp(0.40 * self.deprivation + 0.30 * self.multimorbidity + 0.30 * float(self.rural))


@dataclass(frozen=True)
class ProviderAgent:
    provider_id: int
    provider_type: str
    capacity: int
    benefit_eligible: bool
    scope: tuple[str, ...]
    place_accountability: float
    audit_strength: float
    direct_claiming: float

    def can_deliver(self, contact_type: str) -> bool:
        return self.benefit_eligible and contact_type in self.scope


@dataclass(frozen=True)
class ABMResult:
    monthly: pd.DataFrame
    summary: pd.DataFrame
    patients: pd.DataFrame
    providers: pd.DataFrame


CONTACT_TYPES: tuple[str, ...] = (
    "routine",
    "urgent",
    "chronic",
    "medicines_review",
    "care_coordination",
    "telehealth",
)

CONTACT_TYPE_WEIGHTS = {
    "routine": 0.34,
    "urgent": 0.20,
    "chronic": 0.20,
    "medicines_review": 0.10,
    "care_coordination": 0.08,
    "telehealth": 0.08,
}

PROVIDER_SCOPES = {
    "gp": ("routine", "urgent", "chronic", "care_coordination", "telehealth"),
    "nurse_np": ("routine", "urgent", "chronic", "care_coordination", "telehealth"),
    "pharmacist": ("routine", "medicines_review", "telehealth"),
    "allied": ("routine", "chronic", "care_coordination", "telehealth"),
    "paramedic": ("urgent", "care_coordination", "telehealth"),
}


def _vector(rng: np.random.Generator, mean: float, spread: float, size: int) -> np.ndarray:
    return np.clip(rng.normal(mean, spread, size=size), 0.0, 1.0)


def _weighted_choice(rng: np.random.Generator, weights: Mapping[str, float]) -> str:
    items = list(weights.items())
    labels = [label for label, _ in items]
    probs = np.asarray([max(0.0, w) for _, w in items], dtype=float)
    total = probs.sum()
    if total <= 0:
        return labels[0]
    probs = probs / total
    return str(rng.choice(labels, p=probs))


def build_patients(params: ABMParameters, rng: np.random.Generator) -> list[PatientAgent]:
    deprivation = _vector(rng, params.deprivation_demand_modifier, 0.18, params.population_size)
    rural = rng.random(params.population_size) < clamp(0.08 + 0.45 * params.rurality_demand_modifier)
    multimorbidity = _vector(rng, params.multimorbidity_demand_modifier, 0.16, params.population_size)
    price_sensitivity = np.clip(
        0.18
        + 0.42 * deprivation
        + 0.10 * multimorbidity
        + 0.15 * rural.astype(float)
        + 0.10 * params.price_elasticity_general,
        0.0,
        1.0,
    )
    trust = np.clip(
        0.36
        + 0.28 * params.consumer_trust
        + 0.14 * params.equity_program_strength
        + 0.08 * params.te_tiriti_governance_strength
        - 0.12 * price_sensitivity,
        0.0,
        1.0,
    )
    access_barrier = np.clip(
        0.20
        + 0.25 * params.patient_copayment_level
        + 0.18 * params.local_inperson_constraint
        + 0.15 * price_sensitivity
        + 0.12 * rural.astype(float),
        0.0,
        1.0,
    )
    return [
        PatientAgent(
            patient_id=i + 1,
            deprivation=float(deprivation[i]),
            rural=bool(rural[i]),
            multimorbidity=float(multimorbidity[i]),
            price_sensitivity=float(price_sensitivity[i]),
            trust=float(trust[i]),
            access_barrier=float(access_barrier[i]),
        )
        for i in range(params.population_size)
    ]


def build_providers(params: ABMParameters) -> list[ProviderAgent]:
    counts = {
        "gp": max(1, round(params.population_size / 72 * (0.9 + params.gp_capacity_index))),
        "nurse_np": max(1, round(params.population_size / 96 * (0.8 + params.nurse_np_capacity_index))),
        "pharmacist": max(1, round(params.population_size / 130 * (0.7 + params.pharmacist_capacity_index))),
        "allied": max(1, round(params.population_size / 140 * (0.7 + params.allied_health_capacity_index))),
        "paramedic": max(1, round(params.population_size / 180 * (0.7 + params.paramedic_alt_capacity_index))),
    }
    capacity_base = {
        "gp": max(8, round(14 + 24 * params.medical_productivity_per_fte)),
        "nurse_np": max(6, round(11 + 18 * params.np_nurse_productivity_per_fte)),
        "pharmacist": max(4, round(8 + 10 * params.pharmacist_capacity_index)),
        "allied": max(4, round(7 + 9 * params.allied_health_capacity_index)),
        "paramedic": max(3, round(6 + 8 * params.paramedic_alt_capacity_index)),
    }
    provider_bias = {
        "gp": 0.15,
        "nurse_np": 0.13,
        "pharmacist": 0.10,
        "allied": 0.10,
        "paramedic": 0.11,
    }
    providers: list[ProviderAgent] = []
    provider_id = 1
    for provider_type, count in counts.items():
        for _ in range(count):
            providers.append(
                ProviderAgent(
                    provider_id=provider_id,
                    provider_type=provider_type,
                    capacity=capacity_base[provider_type],
                    benefit_eligible=True,
                    scope=PROVIDER_SCOPES[provider_type],
                    place_accountability=clamp(params.place_based_accountability_strength + provider_bias[provider_type]),
                    audit_strength=clamp(params.audit_intensity + 0.05 * params.item_rules_strength),
                    direct_claiming=clamp(params.direct_claiming_strength + 0.04 * params.scheduled_medical_benefit_strength),
                )
            )
            provider_id += 1
    return providers


def abm_parameters_from_mapping(
    values: Mapping[str, object],
    *,
    months: int = 24,
    population_size: int = 180,
    seed: int = 7,
) -> ABMParameters:
    return ABMParameters.from_mapping(values, months=months, population_size=population_size, seed=seed)


class ABMSimulation:
    def __init__(self, params: ABMParameters):
        self.params = params
        self.rng = np.random.default_rng(params.seed)
        self.patients = build_patients(params, self.rng)
        self.providers = build_providers(params)
        self._provider_base_capacity = {provider.provider_id: provider.capacity for provider in self.providers}
        self._patient_lookup = {patient.patient_id: patient for patient in self.patients}
        self._group_threshold = float(np.median([patient.high_need_score for patient in self.patients]))

    def _access_probability(self, patient: PatientAgent) -> float:
        need_pressure = 0.28 + 0.20 * patient.high_need_score
        payment_penalty = self.params.patient_copayment_level * (1 - self.params.copayment_protection_strength)
        price_penalty = payment_penalty * (0.68 + 0.52 * patient.price_sensitivity)
        rural_penalty = self.params.local_inperson_constraint * (0.55 if patient.rural else 0.22)
        supply_support = (
            0.22 * self.params.capitation_base_strength
            + 0.22 * self.params.scheduled_medical_benefit_strength
            + 0.14 * self.params.scheduled_benefit_price_adequacy
            + 0.12 * self.params.activity_signal_strength
            + 0.12 * self.params.place_based_accountability_strength
            + 0.10 * self.params.telehealth_acceptability
            + 0.08 * self.params.equity_program_strength
        )
        trust = 0.14 * patient.trust
        access = 0.25 + supply_support + trust - 0.42 * price_penalty - 0.18 * rural_penalty - 0.10 * self.params.global_cap_constraint - 0.08 * need_pressure
        return clamp(access)

    def _contact_weights(self, patient: PatientAgent) -> dict[str, float]:
        return {
            "routine": CONTACT_TYPE_WEIGHTS["routine"] + 0.05 * (1 - patient.multimorbidity),
            "urgent": CONTACT_TYPE_WEIGHTS["urgent"] + 0.10 * patient.multimorbidity + 0.06 * self.params.urgent_care_effectiveness,
            "chronic": CONTACT_TYPE_WEIGHTS["chronic"] + 0.10 * patient.multimorbidity,
            "medicines_review": CONTACT_TYPE_WEIGHTS["medicines_review"] + 0.06 * self.params.scope_substitution_rate,
            "care_coordination": CONTACT_TYPE_WEIGHTS["care_coordination"] + 0.05 * self.params.place_based_accountability_strength,
            "telehealth": CONTACT_TYPE_WEIGHTS["telehealth"] + 0.08 * self.params.telehealth_acceptability + (0.04 if patient.rural else 0.0),
        }

    def _available_providers(self, contact_type: str, capacities: dict[int, int]) -> list[ProviderAgent]:
        return [
            provider
            for provider in self.providers
            if capacities[provider.provider_id] > 0 and provider.can_deliver(contact_type)
        ]

    def _choose_provider(
        self,
        contact_type: str,
        capacities: dict[int, int],
    ) -> ProviderAgent | None:
        candidates = self._available_providers(contact_type, capacities)
        if not candidates:
            return None
        weights = []
        for provider in candidates:
            remaining = capacities[provider.provider_id]
            base = 1.0 + 0.08 * remaining
            if provider.provider_type == "gp":
                base += 0.14
            elif provider.provider_type == "nurse_np":
                base += 0.12
            elif provider.provider_type == "pharmacist":
                base += 0.08
            elif provider.provider_type == "allied":
                base += 0.06
            elif provider.provider_type == "paramedic":
                base += 0.05
            base += 0.10 * provider.place_accountability + 0.08 * provider.audit_strength + 0.06 * provider.direct_claiming
            if contact_type in {"urgent", "care_coordination"} and provider.provider_type in {"gp", "paramedic"}:
                base += 0.12
            if contact_type == "medicines_review" and provider.provider_type == "pharmacist":
                base += 0.20
            weights.append(max(0.01, base))
        probs = np.asarray(weights, dtype=float)
        probs = probs / probs.sum()
        choice = int(self.rng.choice(len(candidates), p=probs))
        return candidates[choice]

    def _provider_capacity_schedule(self, month: int) -> dict[int, int]:
        stress = (
            0.22 * self.params.budget_tightness
            + 0.18 * self.params.global_cap_constraint
            + 0.10 * self.params.pho_transaction_cost
            - 0.10 * self.params.market_entry_response
            - 0.08 * self.params.rural_loading_response
        )
        capacity_scale = clamp(1.0 + 0.18 * self.params.capitation_base_strength + 0.14 * self.params.scheduled_medical_benefit_strength - 0.16 * stress)
        scheduled = {}
        for provider in self.providers:
            base = self._provider_base_capacity[provider.provider_id]
            if month == 1:
                adjustment = 1.0
            else:
                adjustment = 1.0 - min(0.30, self.params.workforce_exit_rate * (0.30 + stress))
            monthly_capacity = max(1, round(base * capacity_scale * adjustment))
            scheduled[provider.provider_id] = monthly_capacity
        return scheduled

    def run(self) -> ABMResult:
        monthly_rows: list[dict[str, float | int | str]] = []
        patient_rows: list[dict[str, float | int | bool]] = []
        provider_rows = [
            {
                "provider_id": provider.provider_id,
                "provider_type": provider.provider_type,
                "capacity": provider.capacity,
                "benefit_eligible": provider.benefit_eligible,
                "scope": "|".join(provider.scope),
                "place_accountability": provider.place_accountability,
                "audit_strength": provider.audit_strength,
                "direct_claiming": provider.direct_claiming,
            }
            for provider in self.providers
        ]

        unmet_need_stock = 0.0
        hospital_pressure_stock = 0.0

        for month in range(1, self.params.months + 1):
            scheduled_capacities = self._provider_capacity_schedule(month)
            capacities = scheduled_capacities.copy()
            total_demand = 0
            resolved = 0
            unresolved = 0
            gaming_events = 0
            low_value_events = 0
            public_cost = 0.0
            ed_events = 0.0
            admissions = 0.0
            ambulance_events = 0.0
            high_need_attempts = 0
            low_need_attempts = 0
            high_need_resolved = 0
            low_need_resolved = 0

            seasonal = 1.0 + 0.045 * np.sin(2 * np.pi * month / 12.0)
            for patient in self.patients:
                patient_lambda = (
                    (self.params.base_need_per_1000 / 1000.0)
                    * self.params.population_size
                    / max(1, self.params.population_size)
                    * seasonal
                    * (0.72 + 0.42 * patient.high_need_score + 0.18 * self.params.chronic_need_index)
                )
                patient_lambda = max(0.01, patient_lambda)
                demand = int(self.rng.poisson(patient_lambda))
                if demand <= 0:
                    continue
                total_demand += demand
                access_probability = self._access_probability(patient)
                for _ in range(demand):
                    contact_type = _weighted_choice(self.rng, self._contact_weights(patient))
                    high_need_attempts += 1 if patient.high_need_score >= self._group_threshold else 0
                    low_need_attempts += 1 if patient.high_need_score < self._group_threshold else 0
                    if self.rng.random() > access_probability:
                        unresolved += 1
                        unmet_need_stock += 1.0 + 0.3 * patient.high_need_score
                        continue
                    provider = self._choose_provider(contact_type, capacities)
                    if provider is None:
                        unresolved += 1
                        unmet_need_stock += 1.0 + 0.2 * patient.high_need_score
                        continue
                    capacities[provider.provider_id] -= 1
                    resolved += 1
                    if patient.high_need_score >= self._group_threshold:
                        high_need_resolved += 1
                    else:
                        low_need_resolved += 1

                    provider_cost = {
                        "gp": 1.00,
                        "nurse_np": 0.82,
                        "pharmacist": 0.64,
                        "allied": 0.70,
                        "paramedic": 0.78,
                    }[provider.provider_type]
                    payment_signal = (
                        0.52 * self.params.scheduled_medical_benefit_strength
                        + 0.24 * self.params.activity_signal_strength
                        + 0.16 * self.params.acc_activity_strength
                        + 0.08 * self.params.capitation_base_strength
                    )
                    cost_multiplier = 1.0 + 0.14 * self.params.scheduled_benefit_price_adequacy
                    public_cost += provider_cost * cost_multiplier * (0.72 + 0.50 * payment_signal)

                    low_value_prob = clamp(
                        0.04
                        + 0.20 * self.params.scheduled_medical_benefit_strength
                        + 0.11 * self.params.direct_claiming_strength
                        + 0.08 * self.params.global_cap_constraint
                        - 0.16 * self.params.item_rules_strength
                        - 0.16 * self.params.gaming_controls
                        - 0.12 * self.params.audit_intensity
                        - 0.08 * provider.audit_strength
                    )
                    if self.rng.random() < low_value_prob:
                        low_value_events += 1

                    gaming_prob = clamp(
                        0.03
                        + 0.12 * self.params.scheduled_medical_benefit_strength
                        + 0.10 * self.params.direct_claiming_strength
                        + 0.08 * self.params.pho_transaction_cost
                        - 0.14 * self.params.item_rules_strength
                        - 0.14 * self.params.gaming_controls
                        - 0.10 * self.params.audit_intensity
                        - 0.06 * provider.place_accountability
                    )
                    if self.rng.random() < gaming_prob:
                        gaming_events += 1

                    if contact_type == "urgent":
                        ambulance_events += 0.18
                    if contact_type in {"urgent", "care_coordination"} and provider.provider_type in {"gp", "paramedic"}:
                        ambulance_events += 0.07

            access_rate = resolved / total_demand if total_demand else 0.0
            high_need_access_rate = high_need_resolved / high_need_attempts if high_need_attempts else 0.0
            low_need_access_rate = low_need_resolved / low_need_attempts if low_need_attempts else 0.0
            equity_gap = low_need_access_rate - high_need_access_rate

            unmet_need_stock = max(
                0.0,
                self.params.unmet_need_persistence * unmet_need_stock
                + max(0, total_demand - resolved)
                + 0.40 * unresolved
                - 0.16 * self.params.place_based_accountability_strength
                - 0.10 * self.params.equity_program_strength
                - 0.08 * self.params.telehealth_acceptability,
            )
            admissions = (
                0.12 * unresolved
                + 0.20 * ambulance_events
                + 0.08 * self.params.delay_complexity_growth * unmet_need_stock
            )
            ed_events = (
                0.14 * unresolved
                + 0.18 * hospital_pressure_stock
                + 0.06 * self.params.ed_conversion_rate * unmet_need_stock
            )
            hospital_pressure_stock = max(
                0.0,
                hospital_pressure_stock * 0.86
                + 0.015 * unmet_need_stock
                + 0.30 * self.params.baseline_hospital_pressure
                + 0.08 * self.params.hospital_salience
                + 0.012 * ambulance_events
                + 0.020 * admissions
                - 0.030 * access_rate
                - 0.020 * self.params.ambulance_deflection_rate
            )
            fiscal_risk_index = clamp(
                0.18
                + 0.22 * self.params.global_cap_constraint
                + 0.16 * self.params.patient_copayment_level
                + 0.10 * self.params.pho_transaction_cost
                + 0.14 * (gaming_events / max(1, resolved))
                + 0.08 * low_value_events
                + 0.12 * self.params.budget_tightness
                - 0.18 * access_rate
                - 0.10 * self.params.item_rules_strength
            )
            gaming_risk_index = clamp(
                0.12
                + 0.20 * self.params.scheduled_medical_benefit_strength
                + 0.16 * self.params.direct_claiming_strength
                + 0.12 * self.params.pho_transaction_cost
                - 0.18 * self.params.item_rules_strength
                - 0.16 * self.params.gaming_controls
                - 0.10 * self.params.audit_intensity
                - 0.08 * self.params.safety_governance
            )
            public_cost_index = public_cost + 0.05 * admissions + 0.04 * ed_events + 0.03 * ambulance_events
            scheduled_total_capacity = sum(scheduled_capacities.values())
            supply_utilisation = resolved / scheduled_total_capacity if scheduled_total_capacity else 0.0

            monthly_rows.append(
                {
                    "month": month,
                    "seed": self.params.seed,
                    "population_size": self.params.population_size,
                    "total_demand_contacts": total_demand,
                    "resolved_contacts": resolved,
                    "unresolved_contacts": unresolved,
                    "access_rate": access_rate,
                    "high_need_access_rate": high_need_access_rate,
                    "low_need_access_rate": low_need_access_rate,
                    "equity_gap_index": equity_gap,
                    "unmet_need_index": unmet_need_stock,
                    "hospital_pressure_index": hospital_pressure_stock,
                    "fiscal_risk_index": fiscal_risk_index,
                    "gaming_risk_index": gaming_risk_index,
                    "public_cost_index": public_cost_index,
                    "provider_capacity": scheduled_total_capacity,
                    "provider_utilisation": supply_utilisation,
                    "low_value_events": low_value_events,
                    "gaming_events": gaming_events,
                    "ed_events_index": ed_events,
                    "admissions_index": admissions,
                    "ambulance_events_index": ambulance_events,
                }
            )

        monthly = pd.DataFrame(monthly_rows)
        patients = pd.DataFrame([asdict(patient) for patient in self.patients])
        providers = pd.DataFrame(provider_rows)
        summary = pd.DataFrame(
            [
                {
                    "metric": "resolved_contacts",
                    "value": int(monthly["resolved_contacts"].sum()),
                },
                {
                    "metric": "unresolved_contacts",
                    "value": int(monthly["unresolved_contacts"].sum()),
                },
                {
                    "metric": "final_unmet_need_index",
                    "value": round(float(monthly.iloc[-1]["unmet_need_index"]), 3),
                },
                {
                    "metric": "final_hospital_pressure_index",
                    "value": round(float(monthly.iloc[-1]["hospital_pressure_index"]), 3),
                },
                {
                    "metric": "mean_access_rate",
                    "value": round(float(monthly["access_rate"].mean()), 3),
                },
                {
                    "metric": "mean_equity_gap_index",
                    "value": round(float(monthly["equity_gap_index"].mean()), 3),
                },
                {
                    "metric": "mean_fiscal_risk_index",
                    "value": round(float(monthly["fiscal_risk_index"].mean()), 3),
                },
                {
                    "metric": "mean_gaming_risk_index",
                    "value": round(float(monthly["gaming_risk_index"].mean()), 3),
                },
            ]
        )
        return ABMResult(monthly=monthly, summary=summary, patients=patients, providers=providers)


def run_abm(
    params: ABMParameters | Mapping[str, object],
    *,
    months: int | None = None,
    population_size: int | None = None,
    seed: int | None = None,
) -> ABMResult:
    if isinstance(params, ABMParameters):
        model_params = params
    else:
        default_params = ABMParameters()
        model_params = ABMParameters.from_mapping(
            params,
            months=months if months is not None else default_params.months,
            population_size=population_size if population_size is not None else default_params.population_size,
            seed=seed if seed is not None else default_params.seed,
        )
    simulation = ABMSimulation(model_params)
    return simulation.run()


def run_abm_scenario(
    scenario_id: str = "F4",
    *,
    months: int = 24,
    population_size: int = 180,
    seed: int = 7,
) -> ABMResult:
    from models.primarycare_model.full_parameterised_model_v170 import scenario_parameters

    return run_abm(
        scenario_parameters(scenario_id),
        months=months,
        population_size=population_size,
        seed=seed,
    )

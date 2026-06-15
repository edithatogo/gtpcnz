"""Privacy module."""
from __future__ import annotations

import numpy as np


def laplace_noise(scale, size=1, rng=None):
    if rng is None:
        rng = np.random.default_rng()
    if scale <= 0.0:
        return np.zeros(size)
    u = rng.uniform(low=-0.5, high=0.5, size=size)
    return scale * np.sign(u) * np.log(1.0 - 2.0 * np.abs(u))


def add_laplace_noise(value, sensitivity, epsilon, rng=None):
    return value + laplace_noise(sensitivity / max(epsilon, 1e-12), 1, rng)[0]


SENS = {"age": 120.0, "deprivation_index": 9.0, "total_patients": 1.0, "total_funding": 100000.0}
EPS = 0.5
PII = {"nhi", "patient_id", "name", "dob", "address", "phone", "email"}


def check_no_patient_data(data):
    return [k for k in data if k.lower().replace(" ", "_") in PII]


def assert_aggregate_only(data):
    d = check_no_patient_data(data)
    if d:
        raise ValueError(f"Patient data: {d}")


def strip_patient_data(records):
    return [{k: v for k, v in r.items() if k.lower().replace(" ", "_") not in PII} for r in records]


def noisify_metric(name, value, epsilon=0.5, rng=None):
    return add_laplace_noise(value, SENS.get(name, 1.0), epsilon, rng)


def noisify_metrics(metrics, epsilon=0.5, rng=None):
    return {k: noisify_metric(k, v, epsilon, rng) for k, v in metrics.items()}


class PrivacyBudget:
    def __init__(self, total=1.0):
        self.total = total
        self.spent = 0.0

    @property
    def remaining(self):
        return max(0.0, self.total - self.spent)

    def consume(self, eps):
        if eps > self.remaining:
            raise ValueError(f"{eps}>{self.remaining}")
        self.spent += eps
        return eps

    def reset(self):
        self.spent = 0.0

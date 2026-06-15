"""
Property-based tests using Hypothesis for the PCA simulation.
Fuzzes entity generation rules, tests invariants under random inputs.
"""
from __future__ import annotations

import pytest

pytest.importorskip("hypothesis")
from hypothesis import assume, given, settings, stateful
from hypothesis import strategies as st
from primarycare_model.abm import ABMParameters, run_abm
from primarycare_model.jax_mc import run_deterministic
from primarycare_model.schemas import (
    Ethnicity,
    FundingModel,
    Gender,
    PatientProfile,
    PolicyParams,
    ProviderProfile,
    ProviderType,
    ScenarioParams,
    SimulationConfig,
)


def gs(): return st.sampled_from(list(Gender))
def es(): return st.sampled_from(list(Ethnicity))
def ens(): return st.sampled_from(list(Ethnicity))
def pts(): return st.sampled_from(list(ProviderType))
def fms(): return st.sampled_from(list(FundingModel))


def patient_s():
    return st.builds(PatientProfile,
        age=st.integers(0, 120), gender=gs(), ethnicity=es(),
        deprivation_index=st.integers(1, 10),
        comorbidities=st.lists(
            st.sampled_from(["diabetes","asthma","copd","hypertension","cancer"]),
            max_size=5),
        enrollment_status=st.sampled_from(
            ["enrolled","casual","pending","declined"]))


def provider_s():
    return st.builds(ProviderProfile,
        id=st.text(min_size=1, max_size=20), type=pts(),
        region=st.sampled_from(["Auckland","Canterbury","Waikato"]),
        patient_list=st.lists(st.text(min_size=1), max_size=50),
        capacity=st.integers(0, 5000),
        capitation_panel_size=st.integers(0, 5000))


def config_s():
    return st.builds(SimulationConfig,
        seed=st.integers(0, 2**31-1),
        num_patients=st.integers(1, 100000),
        num_providers=st.integers(1, 500),
        time_horizon_months=st.integers(1, 120),
        tick_interval_days=st.sampled_from([1,2,3,5,6,10,15,30]))


def policy_s():
    return st.builds(
        PolicyParams,
        name=st.text(min_size=1, max_size=30),
        parameters=st.dictionaries(st.text(min_size=1), st.floats(allow_nan=False), max_size=3),
        start_month=st.integers(0, 60),
    )


def scenario_s():
    common = {
        "name": st.text(min_size=1, max_size=50),
        "description": st.one_of(st.none(), st.text(max_size=200)),
        "policy_params": st.lists(policy_s(), max_size=3),
    }
    return st.one_of(
        st.builds(
            ScenarioParams,
            **common,
            funding_model=st.just(FundingModel.CAPITATION),
            capitation_rate=st.floats(0, 500, allow_nan=False),
            ffs_fee_schedule=st.none(),
        ),
        st.builds(
            ScenarioParams,
            **common,
            funding_model=st.just(FundingModel.FFS),
            capitation_rate=st.none(),
            ffs_fee_schedule=st.dictionaries(
                st.sampled_from(["gp_visit", "nurse_visit"]),
                st.floats(0, 200, allow_nan=False),
                min_size=1,
                max_size=3,
            ),
        ),
        st.builds(
            ScenarioParams,
            **common,
            funding_model=st.just(FundingModel.HYBRID),
            capitation_rate=st.floats(0, 500, allow_nan=False),
            ffs_fee_schedule=st.dictionaries(
                st.sampled_from(["gp_visit", "nurse_visit"]),
                st.floats(0, 200, allow_nan=False),
                min_size=1,
                max_size=3,
            ),
        ),
    )

# Property-based tests placeholder



class TestPatientFuzzing:
    @given(patient_s())
    @settings(max_examples=200)
    def test_invariants(self, p):
        assert 0 <= p.age <= 120
        assert 1 <= p.deprivation_index <= 10
        assert len(p.comorbidities) == len(set(p.comorbidities))

    @given(patient_s())
    @settings(max_examples=100)
    def test_roundtrip(self, p):
        assert PatientProfile.model_validate(p.model_dump(mode="json")) == p


class TestProviderFuzzing:
    @given(provider_s())
    @settings(max_examples=200)
    def test_invariants(self, p):
        assert p.capacity >= 0 and p.capitation_panel_size >= 0

    @given(provider_s())
    @settings(max_examples=100)
    def test_roundtrip(self, p):
        assert ProviderProfile.model_validate(p.model_dump(mode="json")) == p


class TestConfigFuzzing:
    @given(config_s())
    @settings(max_examples=200)
    def test_invariants(self, c):
        assert c.num_patients > 0 and c.num_providers > 0
        assert 30 % c.tick_interval_days == 0

    @given(config_s())
    @settings(max_examples=100)
    def test_roundtrip(self, c):
        assert SimulationConfig.model_validate(c.model_dump(mode="json")) == c


class TestScenarioFuzzing:
    @given(scenario_s())
    @settings(max_examples=200)
    def test_invariants(self, s):
        assert len(s.name) >= 1

    @given(scenario_s())
    @settings(max_examples=100)
    def test_roundtrip(self, s):
        assert ScenarioParams.model_validate(s.model_dump(mode="json")) == s


class TestABM:
    @given(seed=st.integers(0, 1023), pop=st.integers(10, 200), mo=st.integers(1, 12))
    @settings(max_examples=15)
    def test_determinism(self, seed, pop, mo):
        p = ABMParameters(seed=seed, population_size=pop, months=mo)
        assert run_abm(p).monthly.equals(run_abm(p).monthly)

    @given(seed=st.integers(0, 1023), pop=st.integers(50, 200), mo=st.integers(1, 6))
    @settings(max_examples=15)
    def test_capacity(self, seed, pop, mo):
        r = run_abm(ABMParameters(seed=seed, population_size=pop, months=mo))
        assert (r.monthly["provider_capacity"] >= r.monthly["resolved_contacts"]).all()

    @given(seed=st.integers(0, 1023), pop=st.integers(50, 200), mo=st.integers(1, 6))
    @settings(max_examples=15)
    def test_access_bounds(self, seed, pop, mo):
        r = run_abm(ABMParameters(seed=seed, population_size=pop, months=mo))
        assert (r.monthly["access_rate"] >= 0).all()
        assert (r.monthly["access_rate"] <= 1).all()


class TestJaxMC:
    @given(seed=st.integers(0, 1023), mo=st.integers(1, 12))
    @settings(max_examples=10)
    def test_non_negative(self, seed, mo):
        c = SimulationConfig(seed=seed, time_horizon_months=mo,
                             num_patients=1000, num_providers=50)
        s = ScenarioParams(name=f"t{seed}", funding_model=FundingModel.CAPITATION,
                          capitation_rate=80.0)
        r = run_deterministic(c, s)
        for m in r.monthly_metrics:
            assert m.total_patients >= 0
            assert m.total_providers >= 0
            assert m.total_visits >= 0
            assert m.total_funding >= 0.0

    @given(seed=st.integers(0, 1023), mo=st.integers(1, 12))
    @settings(max_examples=10)
    def test_determinism(self, seed, mo):
        c = SimulationConfig(seed=seed, time_horizon_months=mo,
                             num_patients=1000, num_providers=50)
        s = ScenarioParams(name=f"d{seed}", funding_model=FundingModel.CAPITATION,
                          capitation_rate=80.0)
        r1, r2 = run_deterministic(c, s), run_deterministic(c, s)
        for a, b in zip(r1.monthly_metrics, r2.monthly_metrics, strict=False):
            assert a.total_funding == b.total_funding

    @given(seed=st.integers(0, 1023), mo=st.integers(1, 6))
    @settings(max_examples=10)
    def test_shape(self, seed, mo):
        c = SimulationConfig(seed=seed, time_horizon_months=mo,
                             num_patients=1000, num_providers=50)
        s = ScenarioParams(name=f"s{seed}", funding_model=FundingModel.CAPITATION,
                          capitation_rate=80.0)
        assert len(run_deterministic(c, s).monthly_metrics) == mo


class ProviderAssignmentMachine(stateful.RuleBasedStateMachine):
    def __init__(self):
        super().__init__()
        self.providers = {}
        self.initial_capacity = {}
        self.assignments = {}

    @stateful.rule(pid=st.text(min_size=1), cap=st.integers(1, 100))
    def add_provider(self, pid, cap):
        self.providers[pid] = cap
        self.initial_capacity[pid] = cap
        self.assignments.setdefault(pid, [])

    @stateful.rule(pid=st.text(min_size=1), pat=st.text(min_size=1))
    def assign(self, pid, pat):
        assume(pid in self.providers and self.providers[pid] > 0)
        self.providers[pid] -= 1
        self.assignments[pid].append(pat)

    @stateful.invariant()
    def cap_never_negative(self):
        assert all(v >= 0 for v in self.providers.values())

    @stateful.invariant()
    def assignment_count_matches_consumed_capacity(self):
        for pid, patients in self.assignments.items():
            assert len(patients) + self.providers.get(pid, 0) == self.initial_capacity.get(pid, 0)


TestProviderAssignment = ProviderAssignmentMachine.TestCase

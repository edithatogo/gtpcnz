"""Regression tests for game-theory formula validation (Track 044)."""

from __future__ import annotations

import inspect
import re

import numpy as np

from models.primarycare_model.runtime_lab import clamp, diminishing_return, strategic_response


def _rsq(values):
    x = np.arange(len(values), dtype=float)
    coefficients = np.polyfit(x, values, 1)
    prediction = np.poly1d(coefficients)
    residual = np.sum((np.array(values) - prediction(x)) ** 2)
    total = np.sum((np.array(values) - np.mean(values)) ** 2)
    return 1.0 if total == 0 else float(1.0 - residual / total)


def _claims(audit_levels, governance=62, admin_cost=58, quality=72, place=64):
    honest = []
    gaming = []
    for audit_level in audit_levels:
        audit = audit_level / 100.0
        governance_norm = governance / 100.0
        quality_norm = quality / 100.0
        place_norm = place / 100.0
        admin_norm = admin_cost / 100.0
        honest_base = strategic_response(0.42 * quality_norm + 0.34 * place_norm + 0.24 * audit, 0.48, 7.0)
        deterrence = strategic_response(0.55 * audit + 0.25 * admin_norm + 0.20 * place_norm, 0.46, 7.0)
        gaming_base = strategic_response(0.62 * governance_norm + 0.22 * (1 - quality_norm) + 0.16 * (1 - place_norm), 0.42, 7.0)
        honest.append(round(48 + 34 * honest_base + 14 * diminishing_return(governance_norm) - 8 * audit, 1))
        gaming.append(round(48 + 42 * gaming_base - 36 * deterrence - 8 * audit**1.2, 1))
    return honest, gaming


def _coop(place_levels, cooperation_gain=55, cherry_pick_gain=48, equity=64, scope=60):
    cooperate = []
    cherry_pick = []
    for place_level in place_levels:
        place_norm = place_level / 100.0
        cooperation_signal = 0.38 * cooperation_gain / 100 + 0.25 * equity / 100 + 0.20 * scope / 100 + 0.24 * place_norm
        cherry_pick_signal = 0.56 * cherry_pick_gain / 100 + 0.12 * (1 - equity / 100) + 0.10 * (1 - scope / 100) - 0.34 * place_norm
        cooperate.append(round(46 + 48 * strategic_response(cooperation_signal, 0.48, 7.0), 1))
        cherry_pick.append(round(46 + 48 * strategic_response(cherry_pick_signal, 0.32, 7.0), 1))
    return cooperate, cherry_pick


def _front(control_levels, activity_gain=58, monitoring_cost=34, place_accountability=66):
    gaming_risk = []
    access = []
    for control_level in control_levels:
        control = control_level / 100.0
        activity = activity_gain / 100.0
        monitoring = monitoring_cost / 100.0
        place = place_accountability / 100.0
        risk_signal = 0.54 * activity - 0.42 * control - 0.16 * place + 0.14 * monitoring
        access_signal = 0.48 * activity + 0.18 * diminishing_return(control) + 0.16 * place - 0.10 * monitoring**1.2
        gaming_risk.append(round(clamp(100 * strategic_response(risk_signal, 0.10, 7.0)), 1))
        access.append(round(clamp(100 * strategic_response(access_signal, 0.35, 6.5)), 1))
    return gaming_risk, access


class TestClaimsAuditNonlinear:
    def test_claims_audit_payoff_nonlinear(self):
        audit_levels = list(range(0, 101, 5))
        honest, gaming = _claims(audit_levels)
        assert _rsq(honest) < 0.98, f"Honest too linear Rsq={_rsq(honest)}"
        assert _rsq(gaming) < 0.999, f"Gaming too linear Rsq={_rsq(gaming)}"


class TestCoordinationNonlinear:
    def test_coordination_payoff_nonlinear(self):
        place_levels = list(range(0, 101, 5))
        cooperate, cherry_pick = _coop(place_levels)
        second_diff = np.diff(np.diff(cooperate))
        assert np.any(np.abs(second_diff) > 0.01), "Cooperate payoff has no curvature"
        cherry_second_diff = np.diff(np.diff(cherry_pick))
        assert np.any(np.abs(cherry_second_diff) > 0.01), "Cherry-pick payoff has no curvature"


class TestFrontierNonlinear:
    def test_frontier_curves_nonlinear(self):
        control_levels = list(range(0, 101, 5))
        gaming_risk, access = _front(control_levels)
        second_diff = np.diff(np.diff(gaming_risk))
        assert np.any(np.abs(second_diff) > 0.01), "Gaming-risk frontier has no curvature"
        assert _rsq(access) < 0.98, f"Access frontier too linear Rsq={_rsq(access)}"


class TestCurveCrossing:
    def test_claims_audit_crossing_threshold(self):
        audit_levels = list(range(0, 101, 5))
        honest, gaming = _claims(audit_levels, governance=90, admin_cost=30, quality=20, place=20)
        crossing = next(
            (
                audit_level
                for audit_level, (honest_value, gaming_value) in zip(audit_levels, zip(honest, gaming, strict=False), strict=False)
                if honest_value >= gaming_value
            ),
            None,
        )
        assert crossing is not None, "No crossing between honest and gaming"
        assert 0 < crossing < 100, f"Crossing at boundary {crossing}"

    def test_coordination_crossing_threshold(self):
        place_levels = list(range(0, 101, 5))
        cooperate, cherry_pick = _coop(place_levels)
        crossing = next(
            (place_levels[i] for i, (cooperate_value, cherry_value) in enumerate(zip(cooperate, cherry_pick, strict=False)) if cooperate_value >= cherry_value),
            None,
        )
        assert crossing is not None, "No crossing between cooperate and cherry-pick"
        assert 0 < crossing <= 100, f"Crossing at boundary {crossing}"


class TestSharedHelpersUsed:
    def test_claims_audit_uses_helpers(self):
        from models.primarycare_model import app

        source = inspect.getsource(app.render_claims_audit_game_lab)
        assert re.search(r"strategic_response\(", source)
        assert re.search(r"diminishing_return\(", source)

    def test_coordination_uses_helpers(self):
        from models.primarycare_model import app

        source = inspect.getsource(app.render_coordination_game_lab)
        assert re.search(r"strategic_response\(", source)

    def test_frontier_uses_helpers(self):
        from models.primarycare_model import app

        source = inspect.getsource(app.render_gaming_risk_frontier_lab)
        assert re.search(r"strategic_response\(", source)
        assert re.search(r"diminishing_return\(", source)


class TestMicroeconomicsSaturation:
    def test_marginal_supply_saturates(self):
        lever_levels = list(range(0, 101, 5))
        recurrent_rate = 48
        base_cost = 130
        admin_friction = 30
        curve_values = []
        for level in lever_levels:
            saturation = level / (level + 18 + admin_friction * 0.45) if level else 0.0
            value = max(0, min(300, base_cost + (recurrent_rate + 18) * saturation * (0.55 + base_cost / 520) - admin_friction * 0.35))
            curve_values.append(round(value, 1))
        second_diff = np.diff(np.diff(curve_values))
        assert np.any(second_diff < -0.01), "No diminishing returns"
        midpoint = len(curve_values) // 2
        assert curve_values[-1] - curve_values[midpoint] < curve_values[midpoint] - curve_values[0] + 0.5, "Upper half not flatter"

    def test_capitation_budget_headroom_erodes(self):
        levels = list(range(0, 101, 10))
        headroom = [round(max(0, 1400 * 120 - 1400 * 100 * (1 + demand / 220)), 1) for demand in levels]
        assert all(delta <= 0 for delta in np.diff(headroom)), "Not monotonic decreasing"
        assert _rsq(headroom) < 0.98, f"Budget headroom too linear Rsq={_rsq(headroom)}"

    def test_access_mix_barrier_is_nonlinear(self):
        levels = list(range(0, 101, 10))
        deferred = []
        for equity in levels:
            barrier = 24 * 0.45 + 34 * 0.18 + (100 - equity) * 0.10
            local = 64 * 1.0 * (1.0 - 34 / 260) * (1.0 - 24 / 260)
            digital = 52 * (1.0 - (1.0 - 0.92) * 0.45) * (0.55 + equity / 180)
            value = max(0.0, 100 - local - digital - equity * 0.18 + barrier * 0.22)
            deferred.append(round(value, 1))
        second_diff = np.diff(np.diff(deferred))
        assert np.any(np.abs(second_diff) > 0.01), "Deferred share has no curvature"

    def test_strategic_response_is_sigmoid(self):
        values = [strategic_response(x, 0.0, 6.0) for x in np.linspace(-2, 2, 50)]
        assert _rsq(values) < 0.95, "strategic_response nearly linear"
        second_diff = np.diff(np.diff(values))
        assert np.any(second_diff > 0.001) and np.any(second_diff < -0.001), "No sigmoid curvature"

    def test_diminishing_return_is_concave(self):
        values = [diminishing_return(x) for x in np.linspace(0, 1, 50)]
        assert np.all(np.diff(values) >= 0), "Not monotonic"
        assert np.any(np.diff(np.diff(values)) < -0.001), "No concave curvature"

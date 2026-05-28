"""Tests for validation schemas."""

from __future__ import annotations

from types import SimpleNamespace

import pandas as pd

from models.primarycare_model.validation.pandera_schemas import (
    REFERENCE_RESULT_COLUMNS,
    SCORE_COLUMNS,
    validate_reference_results_frame,
)
from models.primarycare_model.validation.runtime_checks import (
    check_parameter_value,
    check_result_frame_bounds,
    check_scenario_overrides,
    format_validation_issues,
)

EXPECTED_IDS = {"F0", "F1", "F2", "F3", "F4", "F5", "F6", "F7", "F8", "F9"}


def _valid_frame():
    rows = []
    for index, scenario_id in enumerate(sorted(EXPECTED_IDS), 1):
        rows.append(
            {
                "scenario_id": scenario_id,
                "scenario_name": f"S {scenario_id}",
                "description": "test",
                "hybrid_viability_score": 50 + index,
                "access_score": 40,
                "supply_generation_score": 40,
                "equity_legitimacy_score": 40,
                "governance_resilience_score": 40,
                "hospital_deflection_score": 40,
                "fiscal_risk_score": 30,
                "gaming_risk_score": 30,
                "hospital_pressure_score": 70,
                "mean_last12_public_cost_index": 1.0,
                "rank_by_hybrid_viability": index,
            }
        )
    return pd.DataFrame(rows)


def _fake_def(value_type, lower_bound=None, upper_bound=None, category_values=()):
    return SimpleNamespace(
        parameter_id="test",
        value_type=value_type,
        lower_bound=lower_bound,
        upper_bound=upper_bound,
        category_values=category_values,
    )


def test_validate_reference_results_frame_accepts_valid():
    issues = validate_reference_results_frame(_valid_frame(), None)
    assert issues == []


def test_validate_reference_results_frame_rejects_out_of_bounds():
    df = _valid_frame()
    df.loc[0, "hybrid_viability_score"] = 120
    issues = validate_reference_results_frame(df, None)
    assert any("outside 0-100" in issue for issue in issues)


def test_validate_reference_results_frame_rejects_negative():
    df = _valid_frame()
    df.loc[0, "access_score"] = -5
    issues = validate_reference_results_frame(df, None)
    assert any("outside 0-100" in issue for issue in issues)


def test_validate_reference_results_frame_finds_missing_columns():
    df = _valid_frame().drop(columns=["gaming_risk_score"])
    issues = validate_reference_results_frame(df, None)
    assert any("missing columns" in issue for issue in issues)


def test_validate_reference_results_frame_missing_scenario_ids():
    df = _valid_frame()
    df.loc[0, "scenario_id"] = "BAD"
    issues = validate_reference_results_frame(df, EXPECTED_IDS)
    assert any("missing expected scenarios" in issue for issue in issues)


def test_score_columns_are_subset_of_reference_columns():
    assert set(SCORE_COLUMNS).issubset(REFERENCE_RESULT_COLUMNS)


def test_reference_columns_count():
    assert len(REFERENCE_RESULT_COLUMNS) == 14


def test_check_parameter_value_passes_for_valid_int():
    assert check_parameter_value(50, _fake_def("integer", 0, 100)) == []


def test_check_parameter_value_rejects_wrong_type():
    issues = check_parameter_value(50.0, _fake_def("integer"))
    assert any("expected integer" in issue for issue in issues)


def test_check_parameter_value_rejects_below_lower_bound():
    issues = check_parameter_value(5.0, _fake_def("number", 10.0, 100.0))
    assert any("below lower bound" in issue for issue in issues)


def test_check_parameter_value_rejects_above_upper_bound():
    issues = check_parameter_value(150.0, _fake_def("number", 0.0, 100.0))
    assert any("above upper bound" in issue for issue in issues)


def test_check_parameter_value_rejects_categorical_not_in_list():
    issues = check_parameter_value("d", _fake_def("categorical", category_values=("a", "b", "c")))
    assert any("not in allowed values" in issue for issue in issues)


def test_check_parameter_value_boolean_skips_bounds():
    assert check_parameter_value(True, _fake_def("boolean", 0.0, 1.0)) == []


def test_check_parameter_value_unknown_type():
    issues = check_parameter_value(42, _fake_def("unknown"))
    assert any("unknown value_type" in issue for issue in issues)


def test_check_result_frame_bounds_accepts_valid():
    assert check_result_frame_bounds(_valid_frame()) == []


def test_check_result_frame_bounds_rejects_out_of_range():
    df = _valid_frame()
    df.loc[0, "hybrid_viability_score"] = 120
    assert any("outside" in issue for issue in check_result_frame_bounds(df))


def test_check_result_frame_bounds_rejects_missing_score_column():
    df = _valid_frame().drop(columns=["access_score"])
    assert any("missing score column" in issue for issue in check_result_frame_bounds(df))


def test_check_result_frame_bounds_detects_empty_scenario_id():
    df = _valid_frame()
    df.loc[0, "scenario_id"] = ""
    assert any("empty scenario_id" in issue for issue in check_result_frame_bounds(df))


def test_check_scenario_overrides_empty():
    assert check_scenario_overrides([], {"F0"}) == []


def test_check_scenario_overrides_rejects_unknown_id():
    issues = check_scenario_overrides([{"target_id": "BAD"}], {"F0", "F1"})
    assert any("not in known IDs" in issue for issue in issues)


def test_check_scenario_overrides_rejects_missing_target():
    issues = check_scenario_overrides([{"x": "y"}], {"F0"})
    assert any("missing" in issue for issue in issues)


def test_check_scenario_overrides_rejects_non_dict():
    issues = check_scenario_overrides(["bad"], {"F0"})
    assert any("expected dict" in issue for issue in issues)


def test_format_validation_issues_empty():
    assert format_validation_issues([]) == ""


def test_format_validation_issues_produces_bullets():
    result = format_validation_issues(["e1", "e2"])
    assert "Validation issues detected" in result
    assert "- e1" in result
    assert "- e2" in result

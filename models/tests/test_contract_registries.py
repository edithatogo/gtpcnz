import pandas as pd
import pytest
from pydantic import ValidationError

from models.primarycare_model.contracts.inputs import InputDataset
from models.primarycare_model.contracts.parameters import ParameterDefinition
from models.primarycare_model.contracts.scenarios import EducationalLeverDefinition, RuntimeScenarioDefinition
from models.primarycare_model.runtime_lab import SCENARIOS
from models.primarycare_model.scenario_service import (
    EDUCATIONAL_LEVER_DEFINITIONS,
    EXPECTED_SCENARIO_IDS,
    validate_scenario_results,
)
from models.primarycare_model.validation.registry_loader import (
    educational_lever_defaults,
    export_all_registry_json_schemas,
    export_registry_json_schemas,
    input_dataset_defaults,
    load_educational_levers_registry,
    load_inputs_registry,
    load_parameters_registry,
    load_runtime_scenarios_registry,
    parameter_defaults,
)


def _minimal_results_frame() -> pd.DataFrame:
    rows = []
    for idx, scenario_id in enumerate(sorted(EXPECTED_SCENARIO_IDS), start=1):
        rows.append(
            {
                "scenario_id": scenario_id,
                "scenario_name": f"Scenario {scenario_id}",
                "description": "Test scenario",
                "hybrid_viability_score": 50 + idx,
                "access_score": 40,
                "supply_generation_score": 40,
                "equity_legitimacy_score": 40,
                "governance_resilience_score": 40,
                "hospital_deflection_score": 40,
                "fiscal_risk_score": 30,
                "gaming_risk_score": 30,
                "hospital_pressure_score": 70,
                "mean_last12_public_cost_index": 1.0,
                "rank_by_hybrid_viability": idx,
            }
        )
    return pd.DataFrame(rows)


# ── Educational lever registry ───────────────────────────────────────


def test_educational_lever_registry_drives_definitions_and_defaults():
    registry = load_educational_levers_registry()

    assert len(registry) == 7
    assert {item.field_name for item in registry} == {item.field_name for item in EDUCATIONAL_LEVER_DEFINITIONS}
    assert educational_lever_defaults()["scheduled_benefit_level"] == 55
    assert all(0 <= item.default_value <= 100 for item in registry)


def test_educational_lever_registry_every_entry_conforms_to_contract():
    registry = load_educational_levers_registry()
    for lever in registry:
        assert isinstance(lever, EducationalLeverDefinition)
        assert len(lever.field_name) > 0
        assert len(lever.public_label) > 0
        assert 0 <= lever.default_value <= 100
        assert 0 <= lever.lower_bound <= 100
        assert 0 <= lever.upper_bound <= 100
        assert lever.lower_bound <= lever.upper_bound
        assert lever.lower_bound <= lever.default_value <= lever.upper_bound
        assert lever.step >= 1
        assert len(lever.source) > 0
        assert len(lever.claim_boundary) > 0


# ── Runtime scenario registry ───────────────────────────────────────


def test_runtime_scenario_registry_drives_runtime_lab_scenarios():
    registry = load_runtime_scenarios_registry()

    assert {item.scenario_id for item in registry} == {f"F{i}" for i in range(10)}
    assert {item.scenario_id for item in registry} == {item.scenario_id for item in SCENARIOS}
    assert registry[4].scenario_id == "F4"
    assert registry[4].claim_boundary


def test_runtime_scenario_registry_every_entry_conforms_to_contract():
    registry = load_runtime_scenarios_registry()
    for scenario in registry:
        assert isinstance(scenario, RuntimeScenarioDefinition)
        assert len(scenario.scenario_id) > 0
        assert len(scenario.scenario_name) > 0
        assert len(scenario.description) > 0
        assert 0 <= scenario.activity_signal <= 100
        assert 0 <= scenario.capitation <= 100
        assert 0 <= scenario.place_accountability <= 100
        assert 0 <= scenario.scope_capacity <= 100
        assert 0 <= scenario.urgent_ambulance <= 100
        assert 0 <= scenario.data_visibility <= 100
        assert 0 <= scenario.governance <= 100
        assert 0 <= scenario.equity_protection <= 100
        assert 0 <= scenario.copayment_burden <= 100
        assert 0 <= scenario.budget_tightness <= 100
        assert 0 <= scenario.hospital_salience <= 100
        assert 0 <= scenario.complexity <= 100
        assert len(scenario.source) > 0
        assert len(scenario.claim_boundary) > 0


# ── Parameter registry ──────────────────────────────────────────────


def test_parameters_registry_loads_and_validates():
    registry = load_parameters_registry()
    assert len(registry) >= 15
    for param in registry:
        assert isinstance(param, ParameterDefinition)
        assert len(param.parameter_id) > 0
        assert len(param.label) > 0


def test_parameters_registry_all_defaults_within_bounds():
    registry = load_parameters_registry()
    for param in registry:
        if param.value_type in ("integer", "number"):
            dv = float(param.default_value)
            if param.lower_bound is not None:
                assert dv >= param.lower_bound, (
                    f"{param.parameter_id}: default {dv} < lower_bound {param.lower_bound}"
                )
            if param.upper_bound is not None:
                assert dv <= param.upper_bound, (
                    f"{param.parameter_id}: default {dv} > upper_bound {param.upper_bound}"
                )
        if param.value_type == "categorical":
            assert param.default_value in param.category_values


def test_parameters_registry_type_bounds_are_consistent():
    registry = load_parameters_registry()
    for param in registry:
        if param.lower_bound is not None and param.upper_bound is not None:
            assert param.lower_bound <= param.upper_bound, (
                f"{param.parameter_id}: lower_bound {param.lower_bound} > upper_bound {param.upper_bound}"
            )


def test_parameter_defaults_dict_keys():
    defaults = parameter_defaults()
    registry = load_parameters_registry()
    assert set(defaults.keys()) == {p.parameter_id for p in registry}
    assert defaults["base_capitation_rate"] == 195.0
    assert defaults["enrolled_population_count"] == 4500000


# ── Input dataset registry ──────────────────────────────────────────


def test_inputs_registry_loads_and_validates():
    registry = load_inputs_registry()
    assert len(registry) >= 5
    for ds in registry:
        assert isinstance(ds, InputDataset)
        assert len(ds.dataset_id) > 0
        assert len(ds.label) > 0
        assert len(ds.fields) > 0


def test_inputs_registry_every_field_has_type():
    registry = load_inputs_registry()
    for ds in registry:
        for field in ds.fields:
            assert len(field.field_name) > 0
            assert len(field.data_type) > 0
            assert isinstance(field.required, bool)


def test_input_dataset_defaults_summary():
    summary = input_dataset_defaults()
    registry = load_inputs_registry()
    assert set(summary.keys()) == {ds.dataset_id for ds in registry}
    for _ds_id, fields in summary.items():
        assert len(fields) > 0
        assert any(required for required in fields.values())



# ── Duplicate detection ─────────────────────────────────────────────


def test_registry_duplicate_field_name_rejected():
    """Verify that _check_unique catches duplicates in educational levers."""
    from models.primarycare_model.validation.registry_loader import _check_unique

    levers = (
        EducationalLeverDefinition(
            field_name="dup_field", public_label="A",
            health_economics_meaning="x", high_value_meaning="x",
            educational_output_effect="x", slider_help="x",
            default_value=50, source="test", claim_boundary="test",
        ),
        EducationalLeverDefinition(
            field_name="dup_field", public_label="B",
            health_economics_meaning="x", high_value_meaning="x",
            educational_output_effect="x", slider_help="x",
            default_value=60, source="test", claim_boundary="test",
        ),
    )
    with pytest.raises(ValueError, match="Duplicate field_name"):
        _check_unique(levers, "field_name", "educational lever")


def test_scenario_duplicate_id_rejected():
    """Verify that _check_unique catches duplicate scenario IDs."""
    from models.primarycare_model.validation.registry_loader import _check_unique

    scenarios = (
        RuntimeScenarioDefinition(
            scenario_id="F99", scenario_name="A", description="x",
            activity_signal=50.0, capitation=50.0,
            place_accountability=50.0, scope_capacity=50.0,
            urgent_ambulance=50.0, data_visibility=50.0,
            governance=50.0, equity_protection=50.0,
            copayment_burden=50.0, budget_tightness=50.0,
            hospital_salience=50.0, complexity=50.0,
            source="test", claim_boundary="test",
        ),
        RuntimeScenarioDefinition(
            scenario_id="F99", scenario_name="B", description="x",
            activity_signal=50.0, capitation=50.0,
            place_accountability=50.0, scope_capacity=50.0,
            urgent_ambulance=50.0, data_visibility=50.0,
            governance=50.0, equity_protection=50.0,
            copayment_burden=50.0, budget_tightness=50.0,
            hospital_salience=50.0, complexity=50.0,
            source="test", claim_boundary="test",
        ),
    )
    with pytest.raises(ValueError, match="Duplicate scenario_id"):
        _check_unique(scenarios, "scenario_id", "runtime scenario")

# ── Contract boundary validation ────────────────────────────────────


def test_contracts_reject_unknown_fields_and_out_of_range_values():
    with pytest.raises(ValidationError):
        EducationalLeverDefinition(
            field_name="bad", public_label="Bad",
            health_economics_meaning="Bad", high_value_meaning="Bad",
            educational_output_effect="Bad", slider_help="Bad",
            default_value=101, source="test", claim_boundary="test",
        )

    with pytest.raises(ValidationError):
        RuntimeScenarioDefinition(
            scenario_id="BAD", scenario_name="Bad", description="Bad",
            activity_signal=120.0, capitation=50.0,
            place_accountability=50.0, scope_capacity=50.0,
            urgent_ambulance=50.0, data_visibility=50.0,
            governance=50.0, equity_protection=50.0,
            copayment_burden=50.0, budget_tightness=50.0,
            hospital_salience=50.0, complexity=50.0,
            source="test", claim_boundary="test",
        )


def test_educational_lever_rejects_lower_bound_exceeding_upper():
    with pytest.raises(ValidationError, match="lower_bound cannot exceed"):
        EducationalLeverDefinition(
            field_name="bad_bounds", public_label="Bad bounds",
            health_economics_meaning="x", high_value_meaning="x",
            educational_output_effect="x", slider_help="x",
            default_value=50, lower_bound=80, upper_bound=20,
            source="test", claim_boundary="test",
        )


def test_educational_lever_rejects_default_outside_bounds():
    # Use bounds wide enough to pass field-level checks but trigger model validator
    with pytest.raises(ValidationError, match=r"default_value must sit within|less than or equal|greater than or equal"):
        EducationalLeverDefinition(
            field_name="bad_default", public_label="Bad default",
            health_economics_meaning="x", high_value_meaning="x",
            educational_output_effect="x", slider_help="x",
            default_value=120, lower_bound=0, upper_bound=200,
            source="test", claim_boundary="test",
        )


def test_runtime_scenario_rejects_negative_activity_signal():
    with pytest.raises(ValidationError):
        RuntimeScenarioDefinition(
            scenario_id="F99", scenario_name="Test", description="Test",
            activity_signal=-1.0, capitation=50.0,
            place_accountability=50.0, scope_capacity=50.0,
            urgent_ambulance=50.0, data_visibility=50.0,
            governance=50.0, equity_protection=50.0,
            copayment_burden=50.0, budget_tightness=50.0,
            hospital_salience=50.0, complexity=50.0,
            source="test", claim_boundary="test",
        )


def test_runtime_scenario_rejects_empty_scenario_id():
    with pytest.raises(ValidationError):
        RuntimeScenarioDefinition(
            scenario_id="", scenario_name="Test", description="Test",
            activity_signal=50.0, capitation=50.0,
            place_accountability=50.0, scope_capacity=50.0,
            urgent_ambulance=50.0, data_visibility=50.0,
            governance=50.0, equity_protection=50.0,
            copayment_burden=50.0, budget_tightness=50.0,
            hospital_salience=50.0, complexity=50.0,
            source="test", claim_boundary="test",
        )


# ── JSON schema export ──────────────────────────────────────────────


def test_registry_json_schemas_are_exportable():
    schemas = export_registry_json_schemas()

    assert "educational_lever" in schemas
    assert "runtime_scenario" in schemas
    assert schemas["runtime_scenario"]["title"] == "RuntimeScenarioDefinition"


def test_export_all_registry_json_schemas_includes_all():
    schemas = export_all_registry_json_schemas()

    assert "educational_lever" in schemas
    assert "toy_lever" in schemas
    assert "runtime_scenario" in schemas
    assert "parameter" in schemas
    assert "input_dataset" in schemas

# ── Reference result validation ─────────────────────────────────────


def test_reference_result_validation_rejects_out_of_range_scores():
    df = _minimal_results_frame()
    df.loc[0, "hybrid_viability_score"] = 120
    issues = validate_scenario_results(df)
    assert any("outside 0-100" in issue for issue in issues)


def test_reference_result_validation_rejects_negative_scores():
    df = _minimal_results_frame()
    df.loc[0, "access_score"] = -10
    issues = validate_scenario_results(df)
    assert any("outside 0-100" in issue for issue in issues)


def test_reference_result_validation_rejects_missing_columns():
    df = _minimal_results_frame().drop(columns=["supply_generation_score"])
    issues = validate_scenario_results(df)
    assert any("missing columns" in issue for issue in issues)


def test_reference_result_validation_rejects_wrong_scenario_ids():
    df = _minimal_results_frame()
    df.loc[0, "scenario_id"] = "BAD_SCENARIO"
    issues = validate_scenario_results(df)
    assert any("missing expected scenarios" in issue for issue in issues)


def test_reference_result_validation_accepts_valid_frame():
    df = _minimal_results_frame()
    issues = validate_scenario_results(df)
    assert issues == []


def test_json_schemas_have_property_details():
    schemas = export_all_registry_json_schemas()
    param_schema = schemas["parameter"]
    props = param_schema.get("properties", {})
    assert "parameter_id" in props
    assert "label" in props
    assert "default_value" in props


def test_strict_contract_rejects_extra_fields():
    from models.primarycare_model.contracts.parameters import StrictContract

    class TestContract(StrictContract):
        name: str

    with pytest.raises(ValidationError, match=r"extra fields not permitted|Extra inputs are not permitted"):
        TestContract(name="ok", unexpected_field="bad")



def test_parameters_duplicate_id_rejected():
    """Parameter registry should reject duplicate parameter_id values."""
    from models.primarycare_model.validation.registry_loader import _check_unique

    params = (
        ParameterDefinition(
            parameter_id="dup_param", label="A", value_type="number",
            unit="x", default_value=1.0, description="d", source="s",
        ),
        ParameterDefinition(
            parameter_id="dup_param", label="B", value_type="number",
            unit="x", default_value=2.0, description="d", source="s",
        ),
    )
    with pytest.raises(ValueError, match="Duplicate parameter_id"):
        _check_unique(params, "parameter_id", "parameter")

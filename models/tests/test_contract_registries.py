import pandas as pd
import pytest
from pydantic import ValidationError

from models.primarycare_model.contracts.scenarios import RuntimeScenarioDefinition, ToyLeverDefinition
from models.primarycare_model.runtime_lab import SCENARIOS
from models.primarycare_model.scenario_service import (
    EDUCATIONAL_LEVER_DEFINITIONS,
    EXPECTED_SCENARIO_IDS,
    validate_scenario_results,
)
from models.primarycare_model.validation.registry_loader import (
    export_registry_json_schemas,
    load_runtime_scenarios_registry,
    load_toy_levers_registry,
    toy_lever_defaults,
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


def test_toy_lever_registry_drives_legacy_definitions_and_defaults():
    registry = load_toy_levers_registry()

    assert len(registry) == 7
    assert {item.field_name for item in registry} == {item.field_name for item in EDUCATIONAL_LEVER_DEFINITIONS}
    assert toy_lever_defaults()["scheduled_benefit_level"] == 55
    assert all(0 <= item.default_value <= 100 for item in registry)


def test_runtime_scenario_registry_drives_runtime_lab_scenarios():
    registry = load_runtime_scenarios_registry()

    assert {item.scenario_id for item in registry} == {f"F{i}" for i in range(10)}
    assert {item.scenario_id for item in registry} == {item.scenario_id for item in SCENARIOS}
    assert registry[4].scenario_id == "F4"
    assert registry[4].claim_boundary


def test_contracts_reject_unknown_fields_and_out_of_range_values():
    with pytest.raises(ValidationError):
        ToyLeverDefinition(
            field_name="bad",
            public_label="Bad",
            health_economics_meaning="Bad",
            high_value_meaning="Bad",
            educational_output_effect="Bad",
            slider_help="Bad",
            default_value=101,
            source="test",
            claim_boundary="test",
        )

    with pytest.raises(ValidationError):
        RuntimeScenarioDefinition(
            scenario_id="BAD",
            scenario_name="Bad",
            description="Bad",
            activity_signal=120.0,
            capitation=50.0,
            place_accountability=50.0,
            scope_capacity=50.0,
            urgent_ambulance=50.0,
            data_visibility=50.0,
            governance=50.0,
            equity_protection=50.0,
            copayment_burden=50.0,
            budget_tightness=50.0,
            hospital_salience=50.0,
            complexity=50.0,
            source="test",
            claim_boundary="test",
        )


def test_reference_result_validation_rejects_out_of_range_scores():
    df = _minimal_results_frame()
    df.loc[0, "hybrid_viability_score"] = 120

    issues = validate_scenario_results(df)

    assert any("outside 0-100" in issue for issue in issues)


def test_registry_json_schemas_are_exportable():
    schemas = export_registry_json_schemas()

    assert "toy_lever" in schemas
    assert "runtime_scenario" in schemas
    assert schemas["runtime_scenario"]["title"] == "RuntimeScenarioDefinition"

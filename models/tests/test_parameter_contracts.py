import pytest
from pydantic import ValidationError

from models.primarycare_model.contracts.parameters import ParameterDefinition, ParameterValue, ParameterVector


def _definition(**overrides):
    data = {
        "parameter_id": "copay_level",
        "label": "Copayment level",
        "value_type": "number",
        "unit": "nzd",
        "default_value": 25.0,
        "lower_bound": 0.0,
        "upper_bound": 80.0,
        "description": "Illustrative copayment level.",
        "source": "test",
    }
    data.update(overrides)
    return ParameterDefinition(**data)


def test_parameter_definition_rejects_invalid_defaults():
    with pytest.raises(ValidationError, match="lower_bound cannot exceed upper_bound"):
        _definition(lower_bound=10.0, upper_bound=1.0)

    with pytest.raises(ValidationError, match="integer parameters require an integer default"):
        _definition(value_type="integer", default_value=1.2)

    with pytest.raises(ValidationError, match="number parameters require a numeric default"):
        _definition(value_type="number", default_value=True)

    with pytest.raises(ValidationError, match="boolean parameters require a boolean default"):
        _definition(value_type="boolean", default_value="yes")

    with pytest.raises(ValidationError, match="categorical default must be in category_values"):
        _definition(value_type="categorical", default_value="missing", category_values=("base", "high"))

    with pytest.raises(ValidationError, match="default_value is below lower_bound"):
        _definition(default_value=-1.0)

    with pytest.raises(ValidationError, match="default_value is above upper_bound"):
        _definition(default_value=100.0)


def test_parameter_value_validates_against_definition():
    definition = _definition()
    assert ParameterValue(parameter_id="copay_level", value=40.0, source="test").validate_against(definition)

    with pytest.raises(ValueError, match="parameter_id does not match definition"):
        ParameterValue(parameter_id="other", value=40.0, source="test").validate_against(definition)

    with pytest.raises(ValueError, match="requires a numeric value"):
        ParameterValue(parameter_id="copay_level", value=False, source="test").validate_against(definition)

    with pytest.raises(ValueError, match="below lower_bound"):
        ParameterValue(parameter_id="copay_level", value=-1.0, source="test").validate_against(definition)

    with pytest.raises(ValueError, match="above upper_bound"):
        ParameterValue(parameter_id="copay_level", value=100.0, source="test").validate_against(definition)


def test_parameter_value_type_specific_validation_and_vector_mapping():
    integer_def = _definition(parameter_id="visits", value_type="integer", default_value=1, upper_bound=10.0)
    boolean_def = _definition(
        parameter_id="enabled",
        value_type="boolean",
        unit="flag",
        default_value=True,
        lower_bound=None,
        upper_bound=None,
    )
    categorical_def = _definition(
        parameter_id="model",
        value_type="categorical",
        unit="category",
        default_value="base",
        lower_bound=None,
        upper_bound=None,
        category_values=("base", "high"),
    )

    with pytest.raises(ValueError, match="requires an integer value"):
        ParameterValue(parameter_id="visits", value=1.5, source="test").validate_against(integer_def)

    with pytest.raises(ValueError, match="requires a boolean value"):
        ParameterValue(parameter_id="enabled", value="true", source="test").validate_against(boolean_def)

    with pytest.raises(ValueError, match="must be one of"):
        ParameterValue(parameter_id="model", value="unknown", source="test").validate_against(categorical_def)

    vector = ParameterVector(
        vector_id="base",
        claim_boundary="synthetic contract fixture",
        values=(
            ParameterValue(parameter_id="visits", value=2, source="test"),
            ParameterValue(parameter_id="enabled", value=True, source="test"),
            ParameterValue(parameter_id="model", value="base", source="test"),
        ),
    )
    assert vector.as_dict() == {"visits": 2, "enabled": True, "model": "base"}

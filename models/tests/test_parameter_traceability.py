from __future__ import annotations

from models.primarycare_model.validation.public_parameter_loader import load_public_parameters


def test_public_parameters_have_required_traceability() -> None:
    params = load_public_parameters()
    assert params
    for param in params:
        assert param.source_id
        assert param.distribution_type
        assert param.distribution_parameters
        assert param.bounds["lower"] <= param.bounds["upper"]
        assert param.formula_refs

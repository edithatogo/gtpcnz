from __future__ import annotations

from models.primarycare_model.uncertainty.structural_ensemble import load_structural_models, run_structural_ensemble


def test_structural_ensemble_has_required_models() -> None:
    models = load_structural_models()
    assert len(models) >= 8
    ids = {model.structural_model_id for model in models}
    assert {"balanced", "supply_dominant", "weak_substitution"}.issubset(ids)


def test_structural_ensemble_reports_interval() -> None:
    result = run_structural_ensemble()
    assert result["uncertainty_status"] == "parameter_and_structural_uncertainty_reported"
    assert result["structural_uncertainty_interval"][0] < result["structural_uncertainty_interval"][1]

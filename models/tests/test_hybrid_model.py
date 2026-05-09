from primarycare_model.hybrid_model import hybrid_outcome, run_hybrid_model, hybrid_uncertainty, summarise_hybrid_uncertainty
from primarycare_model.demonstrative_games import SCENARIOS


def test_hybrid_model_returns_all_scenarios():
    df = run_hybrid_model()
    assert set(df["scenario_id"]) == {"S0", "S1", "S2", "S3", "S4"}
    assert "hybrid_viability_score" in df.columns


def test_full_architecture_outperforms_status_quo():
    df = run_hybrid_model().set_index("scenario_id")
    assert df.loc["S3", "hybrid_viability_score"] > df.loc["S0", "hybrid_viability_score"]
    assert df.loc["S3", "hospital_deflection_index"] > df.loc["S0", "hospital_deflection_index"]


def test_loose_benefits_have_higher_risk_than_full_architecture():
    df = run_hybrid_model().set_index("scenario_id")
    assert df.loc["S4", "fiscal_gaming_risk_index"] > df.loc["S3", "fiscal_gaming_risk_index"]


def test_hybrid_uncertainty_small_run():
    draws = hybrid_uncertainty(n_per_scenario=5, seed=42)
    assert len(draws) == 25
    summary = summarise_hybrid_uncertainty(draws)
    assert set(summary["scenario_id"]) == {"S0", "S1", "S2", "S3", "S4"}

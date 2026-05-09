from primarycare_model.mcda import CRITERIA, GAME_POSITIONS, POLICY_OPTIONS, WEIGHT_SETS, game_positions_frame, run_all_weight_sets, run_mcda, score_template_rows


def test_mcda_dimensions():
    assert len(CRITERIA) == 10
    assert len(POLICY_OPTIONS) == 10
    assert len(WEIGHT_SETS) == 6
    assert len(GAME_POSITIONS) == 14


def test_default_mcda_ranking_is_plausible():
    df = run_mcda()
    top = df.iloc[0]
    assert top["option_id"] == "O5"
    loose = df[df["option_id"] == "O6"].iloc[0]
    pcbs = df[df["option_id"] == "O3"].iloc[0]
    assert pcbs["risk_adjusted_score"] > loose["risk_adjusted_score"]


def test_all_weight_sets_have_rankings():
    df = run_all_weight_sets()
    assert set(df["weight_set_id"]) == {ws.weight_set_id for ws in WEIGHT_SETS}
    assert df.groupby("weight_set_id").size().min() == len(POLICY_OPTIONS)


def test_game_priority_scores_bounded():
    df = game_positions_frame()
    assert df["priority_score_0_to_100"].between(0, 100).all()
    assert df.sort_values("priority_score_0_to_100", ascending=False).iloc[0]["game_id"] in {"G1", "G11", "G14", "G3"}


def test_score_template_complete():
    df = score_template_rows()
    assert len(df) == len(CRITERIA) * len(POLICY_OPTIONS)

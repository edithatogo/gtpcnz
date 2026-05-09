from primarycare_model.nz_game_map import find_games_by_player, game_ids, get_nz_game_map, get_payoff_levers


def test_game_map_has_expected_number_of_games():
    games = get_nz_game_map()
    assert len(games) == 14
    assert len(set(game.game_id for game in games)) == len(games)


def test_core_players_are_present():
    all_players = " ".join(" ".join(game.players) for game in get_nz_game_map()).lower()
    for expected in ["health nz", "acc", "ambulance", "patients", "phos", "treasury"]:
        assert expected in all_players


def test_find_games_by_player_returns_relevant_games():
    acc_games = find_games_by_player("ACC")
    assert any(game.game_id == "G6" for game in acc_games)
    ambulance_games = find_games_by_player("Ambulance")
    assert any(game.game_id == "G7" for game in ambulance_games)


def test_payoff_levers_include_marginal_contact_benefit_and_target_salience():
    levers = {lever.symbol: lever for lever in get_payoff_levers()}
    assert "M" in levers
    assert "omega_p" in levers
    assert "p_h" in levers


def test_game_ids_are_ordered():
    assert game_ids()[0] == "G1"
    assert game_ids()[-1] == "G14"

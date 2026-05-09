from primarycare_model.uncapped_ffs_model_v131 import results

def test_uncapped_ffs_scenarios_present():
    rows = results()
    assert len(rows) == 9
    assert any(r['scenario'] == 'UC4' for r in rows)
    assert any(r['scenario'] == 'UC5' for r in rows)

def test_uncapped_with_place_beats_uncapped_weak_control():
    by = {r['scenario']: r for r in results()}
    assert by['UC4']['hybrid_score'] > by['UC5']['hybrid_score']
    assert by['UC4']['gaming_risk'] < by['UC5']['gaming_risk']

def test_full_hybrid_beats_current_reform():
    by = {r['scenario']: r for r in results()}
    assert by['UC8']['hybrid_score'] > by['UC1']['hybrid_score']
    assert by['UC8']['estimated_hospital_pressure'] < by['UC1']['estimated_hospital_pressure']

def test_capitation_only_has_lower_marginal_supply_than_uncapped_ffs():
    by = {r['scenario']: r for r in results()}
    assert by['UC7']['marginal_supply'] < by['UC4']['marginal_supply']

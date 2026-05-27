# Skill: Dashboard Claims and Units

Use this skill for Streamlit dashboard wording, units, claim boundaries, and public URL changes.

## Steps

1. Search the live dashboard surface and tests for the target wording.
2. Update implementation, claim tests, and public dashboard contract together.
3. Check that every slider, chart, metric, and index names its unit.
4. Preserve the public-data anchored benchmark caveat.
5. Run Streamlit app and claim tests.

## Standard Unit Labels

- Policy-strength controls: `0-100`.
- Model-generated indices: `0-100`, unitless index score.
- Months: integer months.
- Seeds: integer random seed.
- Population/agents/patients: counts.
- Activity: eligible activity units or appointments per representative period.
- Budget/payment: illustrative NZD when not real observed finance data.
- Access mix: percent share of need met.

## Required Checks

```powershell
python -m pytest -q models/tests/test_app.py models/tests/test_dashboard_claims.py models/tests/test_scenario_service.py
rg -n "toy|primary-care-funding-architecture.streamlit.app" models/primarycare_model/app.py models/primarycare_model/scenario_service.py models/tests/test_dashboard_claims.py
```

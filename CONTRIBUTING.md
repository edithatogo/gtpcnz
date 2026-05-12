# Contributing

GTPCNZ is currently maintained as a public research and translation repository.

## Ground Rules

- Keep claims source-bounded.
- Preserve the distinction between parameterised scaffold and calibrated forecast.
- Do not add precise fiscal, workforce, or hospital-demand claims without real data and validation notes.
- Keep equity, rurality, disability, and Te Tiriti implications visible when proposing policy interpretation changes.

## Development Workflow

1. Create a branch.
2. Run `pytest -q`.
3. Run `quarto render --to html`.
4. If changing the dashboard, run `streamlit run streamlit_app.py` and check the app locally.
5. Open a pull request.

## Pull Request Checklist

- Tests pass.
- Quarto website renders.
- Public claims are caveated.
- New dependencies are added to `requirements.txt`.
- Streamlit changes include `AppTest` coverage where practical.

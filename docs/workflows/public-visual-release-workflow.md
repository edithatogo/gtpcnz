# Public visual release workflow

Use this workflow when updating Quarto, GitHub Pages or the Streamlit dashboard with public visuals.

## Steps

1. Check the visual against Track 029.
2. Check recurring production requirements against Track 030.
3. Add static visuals to Quarto/GitHub Pages.
4. Add dynamic visuals to Streamlit only where interaction teaches something.
5. Add static fallbacks for any Quarto HTML dynamic visual.
6. Add or update tests for required labels, caveats and visual inventory entries.
7. Run local validation:

```bash
python -m compileall models
pytest -q
quarto render --to html
python -m py_compile streamlit_app.py models/primarycare_model/app.py models/primarycare_model/scenario_service.py
```

8. Push public repo changes.
9. Verify GitHub Actions and live URLs.
10. Commit the parent submodule pointer.

## Quality gate

Do not release if:

- model-generated visuals lack index wording;
- conceptual diagrams imply estimated effects;
- images lack alt text or captions;
- tables were flattened without rationale;
- hyperlinks only appear at the end when they support body claims.

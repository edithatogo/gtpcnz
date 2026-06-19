# Work Packages

| Package | Scope | Files | Gate |
|---|---|---|---|
| WP-075-A | Service layer | `models/primarycare_model/dashboard_service.py`, service tests | `python -m pytest -q models/tests/test_dashboard_service.py` |
| WP-075-B | Dash app | `dash_app/**`, Dash tests | `python -m pytest -q models/tests/test_dash_app.py` |
| WP-075-C | HF deployment | `dash_app/Dockerfile`, `.github/workflows/huggingface-space.yml` | Space bundle import check |
| WP-075-D | Public docs | README, Quarto, dashboard contract docs | dashboard claim tests |


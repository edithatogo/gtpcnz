# Workflow: Repo Hygiene Pass

## When To Run

- Before committing broad work.
- After repeated `proceed` turns where local state may have drifted.
- Before pushing to GitHub.
- Before cleaning untracked files or nested repos.

## Procedure

```powershell
git status -sb
git remote -v
git branch -vv
git stash list
git submodule status --recursive
```

Classify files:

| Class | Action |
|---|---|
| In-scope tracked files | Stage explicitly by path. |
| Unrelated tracked files | Leave alone or stash by explicit path if branch movement is blocked. |
| Untracked generated files | Leave alone unless a cleanup track includes them. |
| Nested repo changes | Inspect with `git -C <path> status -sb`; do not stage as parent content. |
| Stale lock files | Remove only exact `.git/index.lock` after confirming no active git process. |

## Verification

Run the smallest meaningful test set first, then the health gate:

```powershell
python -m pytest -q models/tests/test_app.py models/tests/test_dashboard_claims.py
python scripts/check_repo_health.py
```

If the health gate fails for an environmental or missing-support reason, record the exact reason and do not present it as a product failure.

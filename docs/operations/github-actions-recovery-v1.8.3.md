# GitHub Actions Recovery Runbook

Version: v1.8.3
Status: active operations runbook
Scope: `edithatogo/primary-care-funding-architecture`

## Current External Blocker

GitHub Actions runner jobs can fail before execution if the account or organisation cannot allocate hosted runners. The observed failure mode on 2026-05-24 was:

```text
The job was not started because recent account payments have failed or your spending limit needs to be increased.
```

This is not a repository test failure. It blocks CI and Pages jobs before checkout, dependency install, tests, or Quarto render can begin.

## Recovery Steps

1. Open GitHub account settings for the account that owns the repository.
2. Check `Billing & plans`.
3. Resolve failed payments or increase the Actions spending limit.
4. Return to the repository Actions tab.
5. Rerun these workflows:
   - `CI`
   - `Publish Quarto site`
   - `Latest dependency canary`
6. Confirm the repository health gate reports `15/15`.
7. Confirm `pytest -q`, `quarto render --to html`, and the Streamlit compile check pass on GitHub.

## Local Verification While Hosted Runners Are Blocked

Use these commands from the repository root:

```bash
python scripts/check_repo_health.py
pytest -q
quarto render --to html
python -m py_compile streamlit_app.py models/primarycare_model/app.py
```

On OneDrive-backed Windows checkouts, Quarto can encounter local file-lock, Python-kernel or hydration issues. If direct rendering fails for filesystem reasons, render from a clean temporary copy outside OneDrive and set `QUARTO_PYTHON` to a Python interpreter with the Jupyter notebook stack installed.

Verified local recovery pattern on 2026-05-26:

```powershell
py -3.12 -m pip install nbformat nbclient ipykernel jupyter-core
$dest = "C:\tmp\pcf-render-work-20260526"
New-Item -ItemType Directory -Force -Path $dest | Out-Null
robocopy . $dest /E /XD .git .quarto .serena .tmp _site archive codex-tmp public __pycache__ /XF *-IASN2001657* *.pyc *.quarto_ipynb*
$env:QUARTO_PYTHON = "C:\Users\60217257\AppData\Local\Programs\Python\Python312\python.exe"
quarto render --to html
```

`robocopy` returns `1` when files are copied successfully; treat that as success, not failure.

## Public Submodule Recovery

The public `gtpcnz` repository is mounted as `public/gtpcnz`. On OneDrive-backed checkouts, avoid in-place branch switching or broad cleanup if Git reports unlink or lock-file errors. Validate the intended public branch from a clean temporary clone instead:

```powershell
git clone --no-hardlinks --branch main-IASN2001657 --single-branch "public/gtpcnz" "C:\tmp\gtpcnz-main-IASN2001657-audit-20260526"
Set-Location "C:\tmp\gtpcnz-main-IASN2001657-audit-20260526"
git status --short --branch
git rev-list --left-right --count main...main-IASN2001657
python -m pytest models/tests
```

Only update the parent submodule pointer after the public branch has been validated outside OneDrive and the intended public commit is clear. Treat `*-IASN2001657*`, `.tmp/`, `codex-tmp/`, `.quarto/`, `_site/`, `__pycache__/` and `reports/*.quarto_ipynb*` as cleanup candidates, not release inputs.

## Guardrail

Do not weaken CI, remove tests, remove Pages deployment, or downgrade dependency checks to work around runner allocation failures. Hosted runner availability is an account setting issue, not a code quality issue.

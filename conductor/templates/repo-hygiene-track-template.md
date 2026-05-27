# Track Template: Repo Hygiene and Release Readiness

## Metadata

- Track ID: `<next-id>-repo-hygiene-<date>`
- Owner: `repo-hygiene-agent`
- Status: `pending`
- Scope: local repo state, branch state, tests, CI configuration, public deployment references, nested repo boundaries.

## Problem

The repo needs a repeatable hygiene pass that separates real product changes from local workspace noise, verifies the health gates, and prevents accidental publication of stale URLs, private artifacts, generated scratch files, or detached-HEAD commits.

## Goals

- Identify current branch, upstream, remote, and divergence.
- Inventory dirty tracked files, untracked files, nested repos, submodules, stashes, and ignored local noise.
- Verify canonical public URLs and deployment entrypoints.
- Run focused tests and repo-health checks relevant to the change.
- Produce a clean commit or an explicit non-commit status report.

## Non-Goals

- Do not delete untracked files unless the user explicitly asks.
- Do not reset, checkout, or rewrite unrelated changes.
- Do not change public claim strength.
- Do not push broad workspace state as part of hygiene.

## Required Checks

```powershell
git status -sb
git remote -v
git branch -vv
git stash list
git submodule status --recursive
python -m pytest -q -p no:cacheprovider models/tests
python scripts/check_repo_health.py
rg -n "primary-care-funding-architecture.streamlit.app|edithatogo/gtpcnz|edithatogo.github.io/gtpcnz" README.md index.qmd docs models scripts
```

If `scripts/check_repo_health.py` fails because of missing local support modules, record the exact missing module and run the closest focused tests instead.

## Acceptance Criteria

- Branch is not detached, unless the track explicitly says it is preserving a detached commit.
- Intended commit files are listed before commit.
- Unrelated local files are left untouched or stashed with a clear message.
- Focused tests pass.
- Repo-health passes, or the blocker is documented with exact command output.
- Remote push target is confirmed before pushing.

## Plan

- [ ] Read current branch, remote, and dirty state.
- [ ] Inventory nested repo/submodule state.
- [ ] Classify dirty files as in-scope, out-of-scope, generated, or unknown.
- [ ] Run focused tests for changed surfaces.
- [ ] Run repo-health gate.
- [ ] Commit only in-scope files.
- [ ] Push to the intended branch or record why no push occurred.

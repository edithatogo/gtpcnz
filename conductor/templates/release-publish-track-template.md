# Track Template: Branch, PR, and Publish Hygiene

## Metadata

- Track ID: `<next-id>-release-publish-<date>`
- Owner: `github-release-agent`
- Status: `pending`
- Scope: branch state, PR creation, CI status, Pages/Streamlit publication checks, branch pruning.

## Problem

Publication work can fail silently when branch state, nested repos, or deployment URLs drift.

## Goals

- Confirm the intended remote and branch before push.
- Prefer PR branches over force-pushing divergent local `main`.
- Confirm CI, Pages, and Streamlit deployment state after merge.
- Prune merged branches after verifying they have no unique commits.

## Required Checks

```powershell
git status -sb
git remote -v
git branch -vv
git log --oneline --decorate -5
gh pr status
gh run list --limit 10
```

## Acceptance Criteria

- Push target is `https://github.com/edithatogo/gtpcnz.git` unless the track explicitly says otherwise.
- `main` is not force-updated.
- PR or merge target is documented.
- Failed Actions are classified as repo failure or external account/platform blocker.
- Merged feature branches are deleted only after `ahead_by = 0` or equivalent verification.

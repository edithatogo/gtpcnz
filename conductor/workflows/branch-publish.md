# Workflow: Branch and Publish

## Goal

Publish completed work without mixing unrelated local history or workspace noise.

## Procedure

1. Confirm remote:

```powershell
git remote -v
```

2. Confirm branch and divergence:

```powershell
git status -sb
git branch -vv
```

3. If local `main` diverges from `origin/main`, create a branch from `origin/main` and copy/cherry-pick only the intended commit.

4. Run focused tests.

5. Commit only named files.

6. Push the branch:

```powershell
git push -u origin <branch>
```

7. Create or update PR.

8. After merge, verify:

```powershell
gh run list --limit 10
git ls-remote --heads origin <branch>
```

9. Delete the branch only after confirming it has no unique commits relative to `main`.

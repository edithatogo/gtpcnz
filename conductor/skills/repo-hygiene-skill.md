# Skill: Repo Hygiene

Use this skill before broad edits, branch repair, publish operations, or workspace cleanup.

## Steps

1. Read branch, upstream, and remote.
2. Group dirty state into in-scope, unrelated tracked, untracked generated, nested repo, and unknown.
3. If branch movement is needed, stash only the blocking unrelated tracked files with a descriptive message.
4. Run focused tests for the changed surface.
5. Run repo-health when available.
6. Stage only named in-scope files.
7. Commit with a scoped message.
8. Push only after confirming the remote URL and branch.

## Required Evidence

- `git status -sb`
- focused test command and result
- repo-health command and result or explicit blocker
- pushed branch or reason not pushed

## Failure Handling

- Missing support module in repo-health: report exact module and run focused tests.
- Detached HEAD: create a branch before push.
- Divergent local `main`: create a PR branch from `origin/main`.
- Nested repo dirty state: handle separately unless the track includes it.

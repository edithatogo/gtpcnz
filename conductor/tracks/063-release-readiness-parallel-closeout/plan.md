# Plan

Execution wave: `5`.

Depends on:

- Tracks `050` through `062`.

Blocks:

- None.

Safe parallelism:

- Use shallow Cline/DeepSeek v4 Flash delegation: coordinator -> work-package subagent.
- Do not exceed `max_agent_depth=2`.
- Subagents may run concurrently only when their allowed file surfaces do not overlap.
- Any subagent that discovers a need to edit model runtime files must stop and hand back to the coordinator.

## Work Packages

| Work package | Subagent role | Task | Allowed file surface | Required gate/evidence |
|---|---|---|---|---|
| WP-063-A | `diff-auditor` | Classify the large working tree into intended implementation, public mirror sync, generated/transient artifacts, and suspicious unrelated edits. | read-only by default; write only `conductor/tracks/063-release-readiness-parallel-closeout/implementation-log.md` | `git status -sb`, `git diff --stat`, submodule status where available |
| WP-063-B | `environment-blocker` | Reproduce and isolate Windows/OneDrive blockers for pytest temp cleanup, py_compile cache writes, Quarto `_site`, and Git shell/submodule calls. | `docs/testing/**`, track log | command transcripts and blocker classification |
| WP-063-C | `gate-runner` | Rerun deterministic public-only and release gates; record pass/fail with exact command and reason. | track log, `docs/release/**` | required gates in `acceptance.md` |
| WP-063-D | `commit-packager` | Propose reviewable commit groups and files to exclude, split, or inspect manually. | track log, `docs/release/**` | grouping plan with no destructive git actions |
| WP-063-E | `public-source-readiness` | Define the next public-source tasks needed to move Track 053 beyond readiness-only. | `docs/model/public-source-readiness-closeout-v1.md`, track log | readiness note preserving `calibration_readiness_only` |

## Cline Execution Waves

Wave 5A can run concurrently:

- WP-063-A `diff-auditor`
- WP-063-B `environment-blocker`
- WP-063-E `public-source-readiness`

Wave 5B runs after 5A:

- WP-063-C `gate-runner`

Wave 5C runs after 5B:

- WP-063-D `commit-packager`

## Completion Sequence

1. Run `python scripts/check_conductor_parallel_tracks.py`.
2. Assign Wave 5A work packages with non-overlapping write surfaces.
3. Run Wave 5B gate sweep and capture blocker details.
4. Run Wave 5C commit grouping.
5. Update `implementation-log.md` with changed files, gates run, residual blockers, and claim-boundary status.
6. Re-run `python scripts/check_conductor_parallel_tracks.py`.

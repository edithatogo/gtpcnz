# Substack schedule source of truth v1.8.1

Date: 2026-06-15

## Decision

`launch-schedule-v1.7.2.json` is the original primary-care launch plan. It is retained as historical publication-planning evidence and as a local content contract for post ordering, titles, source paths, and public-readiness checks. It is not the authoritative source for the current live Substack schedule after drafts have been rescheduled in Substack.

## Current live-state inputs

Current live scheduled state is represented by the parent publication catalogue and the cached live-draft details used by `scripts/check_substack_publication_readiness.py`:

- scheduled snapshot: `../../catalogue/rareinsights-substack-scheduled.json`
- draft map: `../../catalogue/primary-care-v172-live-draft-map.json`
- local/live health report: `docs/substack-ready/scheduled-post-health-quality-v1.8.1.json`
- human-readable report: `docs/substack-ready/scheduled-post-health-quality-v1.8.1.md`

The health-quality verifier is the repo-side gate that aligns the local applied posts, the scheduled snapshot, and the cached live draft payloads. When `--scheduled-live` is used, the verifier selects only currently scheduled primary-care posts from the live scheduled snapshot, maps them to draft ids through the live draft map, and scores cached live content against the current local opening/title.

## Operating rule

Do not infer an online publication obligation from the `scheduledAt` values in `launch-schedule-v1.7.2.json`. Those dates are historical launch-plan dates. For current live publication timing, refresh `../../catalogue/rareinsights-substack-scheduled.json` from Substack after respecting the shared throttle rule, then regenerate the scheduled health-quality report.

If Substack returns `429 Too Many Requests`, stop live probing or mutation and leave the cached report marked as the last verified state rather than continuing requests.

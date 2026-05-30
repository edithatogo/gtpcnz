# Release notes — v1.2.1

This release adds a systematic contract-compliance audit and housekeeping remediation layer.

## Purpose

The v1.2.0 package had the substantive material, but the audit found that repository-level metadata and some local Markdown links needed clean-up. v1.2.1 verifies the package against the accumulated requirements and records the result in auditable form.

## New files

- `docs/audit/contract-compliance-audit-v1.2.1.md`
- `docs/audit/acceptance-criteria-matrix-v1.2.1.csv`
- `docs/audit/substack-post-qa-checklist-v1.2.1.csv`
- `docs/audit/local-link-audit-v1.2.1.csv`
- `docs/audit/package-counts-v1.2.1.csv`
- `docs/audit/remediation-log-v1.2.1.md`
- `conductor/tracks/017-substack-ready-publication/*`
- `conductor/tracks/018-contract-compliance-audit/*`

## Remediations

- Updated `README.md` from stale v0.7.0 wording to current v1.2.1 status.
- Updated `conductor/tracks.md` to include all tracks 001–018.
- Fixed local Markdown figure links in final report, MCDA report and complete Substack series.
- Added an explicit acceptance criteria matrix.
- Initialised git history for the packaged v1.2.1 repo.

## QA

- `pytest -q`: 42 passed.
- Local Markdown link audit: 0 broken local links.
- Substack post audit: 12/12 posts pass readability, figure and hyperlink thresholds.

## Status

The package is now suitable for stakeholder discussion, RACMA scoping, Substack final editing, policy brief use, and New Zealand Medical Journal Viewpoint/protocol development. It remains non-calibrated and should not be used for precise predictive claims.

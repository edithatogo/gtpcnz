# Implementation Log

- Track opened after PR #64 and PR #65 merged CAL-G-005 and refreshed the release manifest.
- Scope is release artefact regeneration and verification only.
- No new evidence, model parameter, or claim-boundary change is made by opening this track.
- Release generators were updated so direct `python scripts/generate_release_model_card.py` and `python scripts/generate_release_manifest.py` execution imports package code from the repo root.
- Release model card now reports `empirically_supported_if_gated` / `public_aggregate_validated`, lists CAL-G-001 through CAL-G-007, and preserves not-valid-for warnings.
- Release manifest now records claim level, calibration status, not-valid-for warnings, source snapshot hash, parameter hash, model hash, output hash, visual-regression status, and accessibility status.
- Quarto project source now includes the generated release model card and Track 071 evidence page in the render set.
- Homepage, public report source, and public site-map source now surface aggregate validation without expanding precision, implementation-impact, or causal claims.
- `quarto render --to html` was attempted from the OneDrive worktree and blocked by access-denied cleanup of existing `_site` generated files.
- `quarto render reports/primary_care_architecture.qmd --to html` was attempted from the OneDrive worktree and blocked by access-denied cleanup under `.quarto` / `site_libs` plus a Deno Sass cache disk I/O error.
- `quarto render --to html --no-clean --no-cache` was attempted from the OneDrive worktree and blocked by access-denied replacement of `_site/site_libs/quarto-diagram/mermaid-init.js`.
- A render probe copy was created under `$env:TEMP\gtpcnz-track071-render`; Quarto there was blocked by internal Sass compilation failing to spawn `C:\WINDOWS\system32\cmd.exe` with `Invalid handle`.
- Local render blockers are documented in `docs/release/track-071-release-regeneration-v1.md`; release source surfaces are verified by tests.

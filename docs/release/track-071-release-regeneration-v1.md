# Track 071 release regeneration evidence

Track 071 regenerates release-facing public artifacts after the aggregate validation lane passed. The release status is narrow: aggregate validation is visible, but precision, implementation-impact and causal claims remain excluded.

## Regenerated artifacts

| Artifact | Path | Status |
|---|---|---|
| Release model card | `docs/release/model-card-v1.8.1.md` | Regenerated from `scripts/generate_release_model_card.py` |
| Release manifest | `docs/release/release-manifest-v1.8.1.json` | Regenerated from `scripts/generate_release_manifest.py` |
| Public report source | `reports/primary_care_architecture.qmd` | Updated to surface aggregate validation and retain exclusions |
| Homepage source | `index.qmd` | Updated to link to the generated release model card |
| Site-map source | `docs/public-site/site-map-and-release-manifest-v1.8.4.md` | Updated to list release card, manifest and this evidence page |

## Generator checks

| Command | Result |
|---|---|
| `python scripts/generate_release_model_card.py --check-only` | Passed |
| `python scripts/generate_release_manifest.py --check-only` | Passed |
| `python scripts/generate_release_model_card.py` | Wrote `docs/release/model-card-v1.8.1.md` |
| `python scripts/generate_release_manifest.py` | Wrote `docs/release/release-manifest-v1.8.1.json` |

## Release manifest values

| Field | Value |
|---|---|
| `version` | `1.8.1` |
| `claim_level` | `empirically_supported_if_gated` |
| `calibration_status` | `public_aggregate_validated` |
| `source_snapshot_hash` | `e2c31eadd51e56f3ba9f799470e2fe6d26cfba8939ed7c737395f216854e8b4b` |
| `parameter_hash` | `fdb642505004dc8f52e60f3c9ce94e61e982f7a6ab00845e66cc3f2bf87bff8b` |
| `model_hash` | `b79e2dda08e7119166e0660b728feef36c38490452f9e892a33b944a0823edce` |
| `output_hash` | `f72ee1445434087580209adde3993d58fa6700e63aea3761c3a665233d0c092c` |
| `visual_regression_status` | `gate-present` |
| `accessibility_status` | `gate-present` |

## Claim boundary

The generated model card and manifest keep the not-valid-for list:

- precise fiscal savings;
- ED reductions;
- hospital-demand reductions;
- workforce effects;
- implementation impacts;
- causal effects.

## Quarto render evidence

Attempted commands:

| Command | Result |
|---|---|
| `quarto render --to html` from the OneDrive worktree | Blocked by Windows access-denied errors while Quarto tried to remove existing `_site` generated files |
| `quarto render reports/primary_care_architecture.qmd --to html` from the OneDrive worktree | Blocked by access-denied cleanup errors under `.quarto`, `site_libs`, and a Deno Sass cache disk I/O error |
| `quarto render --to html --no-clean --no-cache` from the OneDrive worktree | Blocked by access-denied replacement of `_site/site_libs/quarto-diagram/mermaid-init.js` |
| `robocopy . "$env:TEMP\gtpcnz-track071-render" /E /XD .git .venv _site .quarto site_libs __pycache__ .pytest_cache /XF *.pyc` | Copied source checkout to a temp render probe directory |
| `quarto render --to html` from the temp render probe | Blocked by Quarto internal Sass compilation failing to spawn `C:\WINDOWS\system32\cmd.exe` with `Invalid handle` |

The source-level release surfaces are verified by `models/tests/test_release_engineering.py`. The remaining local render blocker is environmental: locked generated OneDrive output directories in the main worktree and a Quarto Windows Sass compiler spawn failure in the temp probe.

## Verification scope

This evidence page verifies release regeneration and source-surface alignment after aggregate validation. It does not change model parameters, public evidence sources, calibration gates or claim-specific validation status.

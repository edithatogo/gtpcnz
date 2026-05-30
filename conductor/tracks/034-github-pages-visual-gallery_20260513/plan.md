# Plan: GitHub Pages Visual Gallery

Status: Complete.

## Phase 1: Homepage Contract Implementation

1. Add above-the-fold caveat and two primary actions.
2. Add visual reading path.
3. Add visual preview cards.

Review gate: run scoped checks, run `$conductor-review`, apply safe fixes, rerun checks.

## Phase 2: Post and Game-Theory Cards

1. Add first-six post cards.
2. Add game-theory extension card/section.
3. Link each card to Quarto and Streamlit destinations where available.

Review gate: run scoped checks, run `$conductor-review`, apply safe fixes, rerun checks.

## Phase 3: Site Safety and Render

1. Confirm no private Substack drafts are copied into the public repo.
2. Confirm no local filesystem references are rendered.
3. Render the site.

Review gate: run scoped checks, run `$conductor-review`, apply safe fixes, rerun checks.

## Validation

```powershell
quarto render --to html
rg -n "Read report|Open dashboard|Post 01|Post 04|Game theory|model-generated index|Evidence tracker|Calibration readiness" index.qmd public/gtpcnz/index.qmd
rg -n "OneDrive|C:\\\\Users|substack-ready|private draft" public/gtpcnz/index.qmd
```

## Review Evidence

- 2026-05-13 setup-phase review: track registered and cross-referenced to Track 029 and the post-surface crosswalk contract.
- Metadata validation passed with `python -m json.tool`.
- Findings: no high-severity setup findings. Implementation was pending at setup time; the later 2026-05-13 implementation pass below records the delivered GitHub Pages updates, while Track 036 release closeout remains pending.
- 2026-05-13 implementation pass: `public/gtpcnz/index.qmd` updated into a visual reading map/gallery with caveat, report/dashboard calls to action, first-six post cards, game-theory extension and status labels.
- Scoped validation passed: `pytest -q -p no:cacheprovider models/tests` in `public/gtpcnz` included `models/tests/test_public_site_visual_contract.py`.
- Public boundary check passed: `git -C public/gtpcnz ls-files | rg "substack-ready|posts-v|appendices-v|long-drafts|C:\\Users|OneDrive"` returned no tracked private Substack/local-path matches.
- Review result: no high-severity findings found in the scoped implementation review.

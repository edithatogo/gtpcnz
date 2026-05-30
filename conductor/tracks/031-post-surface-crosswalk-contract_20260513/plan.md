# Plan: Post-to-Surface Crosswalk Contract

Status: Complete.

## Phase 1: Contract Creation

1. Add `docs/public-site/post-surface-crosswalk-contract-v1.8.2.md`.
2. Map posts 01-06 to Quarto, Streamlit, GitHub Pages, static visuals and dynamic visuals.
3. Add the game-theory extension crosswalk.
4. Cross-reference implementation tracks 032-036.

Review gate:

1. Run scoped validation.
2. Run `$conductor-review` for Track 031.
3. Apply safe in-scope fixes.
4. Rerun failed or relevant validation.
5. Record review result before progressing.

## Phase 2: Contract Linkage

1. Link the crosswalk from Track 029.
2. Link the crosswalk from the Streamlit dashboard contract.
3. Link implementation tracks back to this contract.

Review gate:

1. Run scoped validation.
2. Run `$conductor-review` for Track 031.
3. Apply safe in-scope fixes.
4. Rerun failed or relevant validation.
5. Record review result before progressing to Track 032/033/034 implementation.

## Validation

```powershell
rg -n "Post-to-surface|post-surface-crosswalk|Post 04|Game theory lab|Microeconomics lab|032|033|034|035|036" docs/public-site conductor/tracks/029-visual-contract-public-visual-narrative_20260513 conductor/tracks/031-post-surface-crosswalk-contract_20260513
```

## Review Evidence

- 2026-05-13 setup-phase review: crosswalk contract created, linked from Track 029 and the Streamlit dashboard contract, and mirrored into the public `gtpcnz` contract docs.
- Scoped validation passed: required references for Post 04, Game theory lab, Microeconomics lab and Tracks 032-036 are present.
- Metadata validation passed with `python -m json.tool`.
- Findings: no high-severity findings. At setup time, the next dependencies were Track 035 simulation specification and then Tracks 032-034 surface implementation; those dependencies are now covered by the later implementation passes recorded in Tracks 032-035.

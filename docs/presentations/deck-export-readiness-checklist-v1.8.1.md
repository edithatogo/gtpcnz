# Deck export/readiness checklist v1.8.1

This checklist governs use of `primary-care-funding-architecture-policy-briefing-v1.8.1.qmd`.

## Source render

Render the revealjs source deck with Quarto cache and process temp redirected to a local scratch path outside the OneDrive-backed working tree:

```powershell
$scratch = "C:\tmp\pcf-quarto-v1.8.1"
New-Item -ItemType Directory -Force -Path "$scratch\cache", "$scratch\tmp" | Out-Null
$env:QUARTO_CACHE_DIR = (Resolve-Path "$scratch\cache").Path
$env:TEMP = (Resolve-Path "$scratch\tmp").Path
$env:TMP = $env:TEMP
quarto render docs/presentations/primary-care-funding-architecture-policy-briefing-v1.8.1.qmd --to revealjs
```

Expected source-render output:

- `docs/presentations/primary-care-funding-architecture-policy-briefing-v1.8.1.html`
- supporting revealjs files beside the rendered deck, if Quarto creates them

Generated render output is a local handoff artefact. Do not commit it unless the output is deliberately reviewed and treated as a small source-like fixture. The tracked release source remains the `.qmd` file plus this checklist.

## Optional export operations

PDF export is optional and should be produced only for a specific handoff:

```powershell
quarto render docs/presentations/primary-care-funding-architecture-policy-briefing-v1.8.1.qmd --to revealjs
quarto render docs/presentations/primary-care-funding-architecture-policy-briefing-v1.8.1.qmd --to pdf
```

PPTX export is optional and may require a separate format target or a conversion step from rendered HTML/PDF, depending on the local Quarto/Pandoc toolchain. If produced, record the exact command used in the handoff notes before distribution.

Do not treat exported PDF or PPTX files as canonical. They are distribution derivatives of the `.qmd` source.

## Readiness checks

- [ ] Revealjs deck renders from the tracked `.qmd` source using redirected cache/temp paths.
- [ ] Slide title, subtitle, date, and author match the intended briefing context.
- [ ] The validation status slide retains `empirically_supported_if_gated` and `public_aggregate_validated`.
- [ ] The excluded-claims slide still prohibits precise fiscal, ED, hospital-demand, workforce, implementation, and causal claims.
- [ ] Any presenter notes or spoken handoff preserve the public aggregate validation boundary.
- [ ] Any PDF/PPTX derivative is labelled as an export derivative, not a source of truth.
- [ ] Generated render files are left untracked unless deliberately approved as small source-like fixtures.

## Claim boundary

The deck supports a bounded public aggregate validation briefing. It does not support claims of precise fiscal savings, ED reductions, hospital-demand reductions, workforce effects, implementation impacts, patient-level forecasts, linked-data calibration, or causal effects.

# Presentation Pack v1.8.1

`primary-care-funding-architecture-policy-briefing-v1.8.1.qmd` is a Quarto revealjs slide deck for presenting the current GTPCNZ public aggregate validation results.

Render command:

```powershell
$scratch = "C:\tmp\pcf-quarto-v1.8.1"
New-Item -ItemType Directory -Force -Path "$scratch\cache", "$scratch\tmp" | Out-Null
$env:QUARTO_CACHE_DIR = (Resolve-Path "$scratch\cache").Path
$env:TEMP = (Resolve-Path "$scratch\tmp").Path
$env:TMP = $env:TEMP
quarto render docs/presentations/primary-care-funding-architecture-policy-briefing-v1.8.1.qmd --to revealjs
```

Export/readiness checklist: `deck-export-readiness-checklist-v1.8.1.md`.

Generated HTML, PDF and PPTX outputs are distribution derivatives. Do not commit them unless a specific review decides they are intentionally small/source-like artefacts.

The deck is claim-gated: it presents aggregate validation status while preserving not-valid-for warnings around precise fiscal, ED, hospital-demand, workforce, implementation and causal claims.

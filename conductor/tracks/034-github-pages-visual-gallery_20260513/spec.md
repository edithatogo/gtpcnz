# Spec: GitHub Pages Visual Gallery

## Problem

The GitHub Pages site must be more than a directory of links. It needs to surface the reading map, the main visuals and clear entry points into the Quarto report and Streamlit dashboard.

## Goal

Create a public landing/gallery experience that lets a general reader understand the argument and choose the right next surface.

## Owned Files

Primary:

- `index.qmd`
- `_quarto.yml`
- public repo equivalents under `public/gtpcnz/`
- public-site docs only where homepage links need explanation

Tests:

- Quarto render checks
- site content/link checks
- deployed Pages screenshot audit in Track 036

## Requirements

1. Add visual preview cards for the argument map, current reform pathway, scenario rank chart, evidence tracker and calibration readiness.
2. Add post-aligned cards for posts 01-06.
3. Add a game-theory extension card or section.
4. Each card must identify whether the content is conceptual, toy, model-generated index, evidence readiness or calibration readiness.
5. Each card must link to the relevant Quarto section and, where possible, Streamlit module.
6. The top screen must include the caveat and two primary actions: read report and open dashboard.
7. The site must not contain private Substack drafts or local filesystem references.

## Parallelisation

This track can run in parallel with Track 032 and 033 after Track 031 is stable.

Suggested subagent split:

- Worker A owns homepage layout and cards.
- Worker B owns gallery/read-in-order rail and links.
- Worker C owns site render/link tests.

Workers must not edit Streamlit app internals or Quarto report body sections.

## Acceptance Criteria

1. GitHub Pages homepage embeds or previews at least four visual cards.
2. Homepage includes a post-aligned reading path for posts 01-06.
3. Homepage includes a game-theory entry point.
4. Homepage links to rendered Quarto report, Streamlit app, model card, evidence tracker and calibration readiness page.
5. `quarto render --to html` passes.
6. `$conductor-review` has been run and high-severity findings have been fixed or explicitly blocked.

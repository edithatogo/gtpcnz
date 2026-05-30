# Spec: Quarto Post-Aligned Visual Report

**Status:** Complete

## Problem

The Quarto report has useful static visuals, but it does not yet function as the canonical visual companion to each public post. Game-theory and microeconomics explanations need clearer section anchors, diagrams and reader guidance.

## Goal

Turn the Quarto report into a guided visual essay that implements the post-to-surface crosswalk.

## Owned Files

Primary:

- `reports/primary_care_architecture.qmd`
- `_quarto.yml`
- `index.qmd` only where report links need to surface
- public repo equivalents under `public/gtpcnz/` when implementing in the public submodule

Tests:

- Quarto render checks
- report content tests under `models/tests/` or an equivalent test location

## Requirements

1. Add a near-top section: "How the posts map to this report and dashboard".
2. Add stable anchors or clear headings for posts 01-06.
3. Add a dedicated game-theory section for "Why formulas do not solve games".
4. Add static game-theory diagrams: at minimum a payoff matrix and a controls/best-response diagram.
5. Add static microeconomic diagrams: at minimum marginal payment gap and co-payment/access barrier or capitation budget constraint.
6. Retain the current reform pathway as the comparator and label F0 accordingly.
7. Use "model-generated index" wording for all scenario plots.
8. Add captions and alt text/equivalent accessible descriptions for every static visual.
9. If any dynamic Quarto visual is used, provide a static fallback.

## Parallelisation

This track can run in parallel with Track 033 and Track 034 after Tracks 031 and 035 define the visual names and destinations.

Suggested subagent split:

- Worker A owns Quarto reading-map and anchors.
- Worker B owns static conceptual/game/microeconomics diagrams.
- Worker C owns static scenario plots and caption/status labels.

Workers must not edit Streamlit app files or GitHub Pages homepage files.

## Acceptance Criteria

1. Quarto report contains the post-to-report/dashboard reading map.
2. Posts 01-06 have named report destinations.
3. Post 04 has an explicit game-theory section.
4. At least two static game-theory diagrams are present.
5. At least two static microeconomics diagrams are present.
6. At least two model-generated scenario plots remain present.
7. `quarto render --to html` passes.
8. `$conductor-review` has been run and high-severity findings have been fixed or explicitly blocked.
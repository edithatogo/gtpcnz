# Track 051 — Dashboard UI Methodology Completion

## Problem

Track 049 implemented all analytical backend functions but several UI wiring items remain:
1. Methodology & evidence tab not rendered in Streamlit
2. Animated parameter-sweep plots not displayed
3. Outcome clustering table not rendered
4. Composite meta-plot not displayed
5. Canonical definitions not linked from metrics
6. Evidence table with download buttons not wired
7. Substack cross-references not displayed as badges

## Goal

Wire all remaining backend functions into the Streamlit UI, creating a comprehensive methodology tab, animated visualisations, and cross-referencing infrastructure.

## Deliverables

1. New "📚 Methodology & evidence" tab with:
   - Canonical definitions table (CANONICAL_DEFS) with hyperlinks to formula appendix
   - Evidence/references table from build_evidence_table()
   - Download buttons for CSL-JSON, RIS, BibLaTeX, XML (Endnote), CFF, YAML
   - Table of figures, table of tables, abbreviation index

2. Animated parameter-sweep plots using create_animation_frames() + Plotly frames
3. Outcome clustering display from run_outcome_clustering()
4. Composite meta-analysis plot from run_composite_meta_analysis()
5. Cross-reference badges linking to SUBSTACK_POSTS from each relevant tab
6. Metric-to-definition hyperlinks in all dataframes

## Acceptance Criteria

- Methodology tab renders all sections without error
- Animated plots play/pause/slider work correctly
- Clustering results display with interpretable labels
- Evidence table has working download buttons for all formats
- Each Streamlit tab has "Related Substack post" badge where applicable
- All 134+ tests pass

## Files Changed

- `models/primarycare_model/app.py` — new tab, animated renderers, clustering display, cross-ref badges

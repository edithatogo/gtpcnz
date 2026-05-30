# Track 052 — Dashboard Lab Enhancements: Deep Dive Clarifications

**Status:** Complete

## Problem

The microeconomics and game theory labs need:
1. Clear documentation of inputs, assumptions, calculations, and output meanings
2. Combined/hybrid model at end of each page showing interaction effects
3. Filters and highlighting on tables
4. Clustering of outcomes into effect categories
5. Cross-links between labs and dashboard tabs

## Deliverables

1. Each microeconomics lab (4 labs) gets a "How this works" expander documenting:
   - Input sliders and their real-world meaning
   - Assumptions behind the calculation
   - The formula/calculation steps
   - What the output means and how to interpret it

2. Each game theory lab (3 labs) gets the same treatment

3. Combined/hybrid model at end of each page that integrates the individual
   simulations into a single interactive plot showing interaction effects

4. Outcome clustering (unsupervised KMeans + supervised logistic regression)
   applied to each lab's output space

5. Table enhancements: filters, clickable row highlighting, column sorting

6. Cross-reference hyperlinks between related labs and dashboard tabs

## Files Changed

- `models/primarycare_model/app.py` — lab documentation expanders, combined models, clustering

## Acceptance Criteria

- Every lab has a "How this works" expander with input/assumption/calculation/output sections
- Combined model at end of each lab page renders without error
- Clustering applied to lab outputs with interpretable category labels
- Tables support filtering and sorting
- Cross-references link correctly
- All 134+ tests pass
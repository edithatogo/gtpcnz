# GTPCNZ Requirements MoSCoW v1.8.3

This control file records the public Streamlit, GitHub Pages and strict-validation requirements for the v1.8.3 surface.

## Must

- REQ-001: Keep the canonical public claim boundary visible on public surfaces.
- REQ-002: Keep Streamlit deployable from `streamlit_app.py`.
- REQ-003: Keep reference scenarios distinct from educational explainer controls.
- REQ-004: Load educational lever metadata from typed registries.
- REQ-005: Load runtime reference scenario defaults from typed registries.
- REQ-006: Validate shipped scenario outputs before dashboard display.
- REQ-007: Keep calculation engines and runtime helpers free of Streamlit imports.
- REQ-008: Keep public and root package dependency manifests aligned for runtime dependencies.
- REQ-009: Keep test collection scoped to root model tests unless explicitly testing the public mirror.
- REQ-010: Preserve seeded stochastic replay behaviour.

## Should

- REQ-011: Use Pydantic v2 contracts for object and registry validation.
- REQ-012: Use optional Pandera-compatible validation when Pandera is installed.
- REQ-013: Provide local fallback validation where optional schema packages are absent.
- REQ-014: Expose calculation traces for public model-generated indices.
- REQ-015: Preserve backward-compatible public aliases where older deployed tests require them.
- REQ-016: Mirror deployment-critical model files into `public/gtpcnz`.
- REQ-017: Keep result labels clear about live, cached, precomputed and stochastic calculations.
- REQ-018: Keep patient-level and linked-data forecast disclaimers attached to outputs.
- REQ-019: Keep concern-boundary checks executable in CI.
- REQ-020: Keep homepage visual-contract strings stable.

## Could

- REQ-021: Add full Pandera as a hard dependency after deployment compatibility is reviewed.
- REQ-022: Add PyArrow schemas for columnar output interchange.
- REQ-023: Add Hypothesis strategies generated from the contracts.
- REQ-024: Add static typing with Pyright or `mypy --strict`.
- REQ-025: Add a public registry browser to the Streamlit app.
- REQ-026: Add JSON Schema export pages for public review.
- REQ-027: Add richer result manifests for every chart.
- REQ-028: Add explicit stochastic replay provenance badges.
- REQ-029: Add public scenario-diff visualisations.
- REQ-030: Add source-level traceability for every educational lever.

## Won't

- REQ-031: Do not claim linked-data calibration.
- REQ-032: Do not claim patient-level forecasting.
- REQ-033: Do not convert index deltas into fiscal savings.
- REQ-034: Do not convert index deltas into hospital-demand reductions.
- REQ-035: Do not convert index deltas into workforce effects.
- REQ-036: Do not convert index deltas into implementation impacts.
- REQ-037: Do not add patient-level sample data.
- REQ-038: Do not move Streamlit dependencies into contracts or validation layers.
- REQ-039: Do not strengthen empirical claims through architecture refactoring.
- REQ-040: Do not remove public compatibility aliases until public tests are migrated.
- REQ-041: Do not treat optional Pandera absence as a production failure.
- REQ-042: Do not reopen model expansion without evidence-base change.

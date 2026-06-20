# Plan

1. Rank proposed visuals by public value, runtime cost, and claim-boundary risk.
2. Implement service-layer chart bundles for the highest-value visuals first: VOI evidence priority, structural ensemble uncertainty, scenario morph, equity-complexity heatmap, and causal architecture graph.
3. Add heavier visuals behind bounded controls or static precomputed payloads: 3D payoff surface, animated regime sweep, Bass adoption/budget surface.
4. Add responsive UI, table fallbacks, downloads, and accessible headings.
5. Add visual contract tests and browser smoke checks for desktop/mobile.
6. Document any visuals deferred for runtime, readability, or claim-boundary reasons.

## Implementation Notes

- Precompute where possible.
- Prefer Plotly WebGL only where point counts justify it.
- Keep all visual text in plain-English units and model-index wording.
- Avoid visual clutter; each visual must answer a specific reader question.

# Plan

1. Define a typed URL-state contract for Dash route, scenario selection, simulation kind, seed, draws, months, population, and educational sliders.
2. Add pure parse/serialize helpers with round-trip tests and strict caps.
3. Add guided reader mode as a visible route or top-level mode with a fixed sequence of sections.
4. Add custom scenario builder service helpers and Dash controls.
5. Add JSON/CSV exports for custom scenario comparisons.
6. Add copy-link and reset controls.
7. Run Dash, runtime, scenario, public-only, and concern-boundary gates.

## Implementation Notes

- Use URL query parameters, not server-side persistence.
- Keep defaults stable for Substack and GitHub Pages deep links.
- Reject or clamp invalid URL parameters.
- Keep custom scenario language explicitly educational/model-index only.

# Plan

1. Identify the current browser test harness and decide whether to reuse existing accessibility/screenshot scripts or add Dash-specific Playwright specs.
2. Add local Dash server fixture or documented manual server startup for browser tests.
3. Add route smoke tests for desktop and mobile.
4. Add interaction tests for scenario comparison, simulation run, table fallback, and CSV download.
5. Add nonblank/render checks for heatmaps and future 3D/animated visuals.
6. Add CI wiring or documented optional browser gate, depending on dependency/runtime constraints.

## Implementation Notes

- Prefer deterministic seeded states.
- Keep browser tests read-only and public-surface only.
- Use tolerant assertions for visual tests to avoid brittle pixel drift.

# Plan

1. Inventory calibration and validation modules and their current pass/readiness statuses.
2. Add a calibration diagnostics service layer that returns typed tables, chart bundles, and source/provenance metadata.
3. Expand Dash calibration/evidence routes with public aggregate calibration, PPC, holdout, temporal, shock, readiness, and freshness panels.
4. Add a missing-evidence queue table that links each blocked claim to the required public source/gate.
5. Add tests that verify diagnostics wording stays within readiness/public aggregate validation claims.
6. Run calibration, Dash, public-only, and concern-boundary gates.

## Implementation Notes

- Prefer existing modules under `models/primarycare_model/calibration/`.
- Use `docs/model/public-source-calibration-evidence-v1.md` as the current evidence ledger where applicable.
- If a gate is blocked, show the blocker plainly rather than hiding it.

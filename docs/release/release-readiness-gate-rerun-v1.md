# Release Readiness Gate Rerun Report - WP-063-C

**Track:** 063-release-readiness-parallel-closeout
**Subagent role:** gate-runner
**Run date:** 2026-06-04

---

## Gate Results Summary

| # | Gate Command | Exit Code | Pass/Fail | Blocker Notes | Claim-Boundary Implications |
|---|-------------|-----------|-----------|---------------|-----------------------------|
| 1 | `python scripts/check_conductor_parallel_tracks.py` | 0 | PASS | None | No change; parallel track contracts intact |
| 2 | `python scripts/check_public_only_boundary.py` | 0 | PASS | None | Public-only boundary preserved |
| 3 | `python scripts/check_parameter_traceability.py` | 0 | PASS | None | Parameter traceability verified |
| 4 | `python scripts/check_public_source_snapshot.py` | 0 | PASS | None | Public source snapshot contract valid |
| 5 | `python scripts/check_dependency_lock.py` | 0 | PASS | None | Dependency lock surface unchanged |
| 6 | `python scripts/check_concern_boundaries.py` | 0 | PASS | None | All 5 concern-boundary rules respected |
| 7 | `python scripts/run_public_aggregate_calibration.py --check-only` | 0 | PASS (readiness) | Source_ready=false for all 3 targets | calibration_readiness_only confirmed |
| 8 | `python scripts/run_voi.py --check-only` | 0 | PASS (readiness) | Decision-uncertainty analysis, not a forecast | VOI is exploratory; no causal claims |
| 9 | `python scripts/run_accessibility_audit.py --check-only` | 0 | PASS | None | Accessibility contract verified |
| 10 | `python scripts/generate_release_model_card.py --check-only` | 0 | PASS | None | Model card confirms claim level |
| 11 | `python scripts/generate_release_manifest.py --check-only` | 0 | PASS | None | All hashes present |
| 12 | `python scripts/sync_public_mirror.py --check` | 0 | PASS | None | 0 drift items; 60 files synced |
| 13 | `python -m pytest -q <13 test files>` | 0 | PASS | None | 15 passed in 3.57s |

---

## Detailed Gate Results

### Gate 1: check_conductor_parallel_tracks.py
- **Exit code:** 0
- **Stdout:** `conductor parallel track contracts passed`
- **Classification:** PASS - Readiness-only
- **Claim-boundary:** No change. Parallel track contracts for tracks 050-062 are intact.

### Gate 2: check_public_only_boundary.py
- **Exit code:** 0
- **Stdout:** `public-only boundary passed`
- **Classification:** PASS - Readiness-only
- **Claim-boundary:** Public-only boundary preserved. No private, patient-level, or confidential data detected.

### Gate 3: check_parameter_traceability.py
- **Exit code:** 0
- **Stdout:** `parameter traceability passed`
- **Classification:** PASS - Readiness-only
- **Claim-boundary:** All parameters traceable to their public registries.

### Gate 4: check_public_source_snapshot.py
- **Exit code:** 0
- **Stdout:** `public source snapshot contract passed`
- **Classification:** PASS - Readiness-only
- **Claim-boundary:** Source snapshot contract valid. Actual source data retrieval remains pending-download.

### Gate 5: check_dependency_lock.py
- **Exit code:** 0
- **Stdout:** `dependency lock surface passed`
- **Classification:** PASS - Readiness-only
- **Claim-boundary:** Dependency lock (uv.lock) surface unchanged.

### Gate 6: check_concern_boundaries.py
- **Exit code:** 0
- **Stdout:** [PASS] no-streamlit-in-strict-layers, [PASS] no-inline-scenario-defaults, [PASS] no-streamlit-in-engines, [PASS] no-inline-production-defaults-in-engines, [PASS] no-patient-level-data-references. Result: PASSED - all concern boundaries respected.
- **Classification:** PASS - Readiness-only
- **Claim-boundary:** All 5 concern-boundary rules respected. No patient-level data references.

### Gate 7: run_public_aggregate_calibration.py --check-only
- **Exit code:** 0
- **Stdout:** JSON output showing 3 calibration targets, all with source_ready: false, passed: false. Claim level: public_benchmark.
- **Classification:** PASS (calibration readiness - intentional fail on source_ready)
- **Claim-boundary:** Calibration remains at calibration_readiness_only. The 3 targets show expected readiness failures because sources are not yet retrieved. not_valid_for list preserved.

### Gate 8: run_voi.py --check-only
- **Exit code:** 0
- **Stdout:** JSON with EVPI=0.237, ENBS rankings, evidence priority [access, supply, fiscal_risk, gaming_risk, implementation_complexity]. Label: decision-uncertainty analysis, not a forecast.
- **Classification:** PASS - Readiness-only
- **Claim-boundary:** VOI is explicitly labeled as decision-uncertainty analysis, not a forecast. No causal or fiscal precision claims.

### Gate 9: run_accessibility_audit.py --check-only
- **Exit code:** 0
- **Stdout:** `accessibility/chart fallback contract passed`
- **Classification:** PASS - Readiness-only
- **Claim-boundary:** Accessibility contract verified; chart fallback mechanisms present.

### Gate 10: generate_release_model_card.py --check-only
- **Exit code:** 0
- **Stdout:** Claim level: public-data anchored benchmark. Calibration status: calibration readiness unless public aggregate gates pass. Not valid for: precise fiscal savings, ED reductions, hospital-demand reductions, workforce effects, implementation impacts, or causal effects. Inputs: public or published aggregate sources only.
- **Classification:** PASS - Readiness-only
- **Claim-boundary:** Model card explicitly restores claim boundary limitations.

### Gate 11: generate_release_manifest.py --check-only
- **Exit code:** 0
- **Stdout:** JSON with 5 content hashes (model, output, parameter, source_snapshot, visual_regression_status). Version: 1.8.1.
- **Classification:** PASS - Readiness-only
- **Claim-boundary:** All content hashes present; manifest generation successful.

### Gate 12: sync_public_mirror.py --check
- **Exit code:** 0
- **Stdout:** OK for all 60 files across 9 directories. Result: PASSED (0 drift items).
- **Classification:** PASS - Readiness-only
- **Claim-boundary:** Public mirror synced; no drift between working tree and mirror target.

### Gate 13: python -m pytest -q (13 test files)
- **Exit code:** 0
- **Stdout:** `15 passed in 3.57s`
- **Stderr:** (none)
- **Classification:** PASS - Readiness-only
- **Claim-boundary:** All 15 tests across 13 test files pass. No environment blockers.


---

## Environment Notes

- **Platform:** Windows, running under OneDrive sync
- **Python:** (as configured in .venv)
- **Runner timeout:** Not triggered (all gates completed within limits)
- **Temp pollution:** 12 orphaned pytest-cache directories exist but did not affect gate execution
- **Coordinator rerun note:** `python -m py_compile streamlit_app.py models/primarycare_model/app.py` later reproduced the known OneDrive bytecode-cache rename blocker (`WinError 5`). In-memory syntax compilation passed, so this is not a syntax failure.

## Claim-Boundary Status

**Current level:** public_benchmark / calibration_readiness_only
**Not valid for:** precise fiscal savings, ED reductions, hospital-demand reductions, workforce effects, implementation impacts, causal effects
**All gates:** Readiness-only passes (no calibrated-model passes). Public aggregate calibration targets remain source_ready: false.

## Conclusion

**13/13 deterministic readiness gates passed.** All are readiness-only passes. No calibrated-model passes attempted. The later `py_compile` bytecode-write check is environment-blocked on this OneDrive checkout, while in-memory syntax compilation passed. Claim boundaries unchanged.

# Repo, GitHub Pages and Streamlit Contracts v1.8.3

| Contract | Requirement | Surface | Obligation |
|---|---|---|---|
| CON-001 | REQ-001 | Public copy | Canonical public-data anchored caveat remains visible. |
| CON-002 | REQ-004 | Registries | Educational lever labels, bounds and defaults load from typed YAML. |
| CON-003 | REQ-005 | Registries | Runtime scenario defaults load from typed YAML. |
| CON-004 | REQ-006 | Validation | Reference scenario outputs are checked before display. |
| CON-005 | REQ-007 | Runtime | Contract, validation, registry and runtime calculation modules do not import Streamlit. |
| CON-006 | REQ-008 | Dependencies | Root and public package declare Pydantic v2. |
| CON-007 | REQ-009 | Tests | Root pytest collection excludes public mirror by default. |
| CON-008 | REQ-010 | Runtime | Seeded stochastic runs remain deterministic for fixed seed. |
| CON-009 | REQ-013 | Validation | Local validation works when Pandera is not installed. |
| CON-010 | REQ-031 | Claims | No linked-data calibration claim is introduced. |
| CON-011 | REQ-032 | Claims | No patient-level forecast claim is introduced. |
| CON-012 | REQ-040 | Public mirror | Backward-compatible aliases remain available for older public tests. |

## Traceability Summary

REQ-001 through REQ-042 are governed by this public-surface contract, the MoSCoW register, the design document, and the Track 043 Conductor plan.


## Public Calibrated Model Contracts

- `CON-PUBLIC-001` Public source admissibility: every runtime source used by the public model must be public or published. Gate: `python scripts/check_public_only_boundary.py`.
- `CON-PARAM-001` Parameter completeness: every coefficient, default, threshold, bound, distribution and scaling factor must resolve to a public parameter entry. Gate: `python scripts/check_parameter_traceability.py`.
- `CON-CAL-001` Public aggregate calibration: empirical calibration may only use public or published aggregate sources. Gate: `python scripts/run_public_aggregate_calibration.py --check-only`.
- `CON-UNC-001` Uncertainty completeness: headline results must include parameter and structural uncertainty metadata. Gate: `models/tests/test_structural_ensemble.py`.
- `CON-VOI-001` VOI completeness: VOI includes EVPI, EVPPI, EVSI, ENBS, decision-error probability and evidence ranking. Gate: `models/tests/test_full_voi.py`.
- `CON-VIS-001` Chart claim grammar: every public chart includes claim, calibration, uncertainty, source, interpretation, warning, download and table fallback metadata. Gate: `models/tests/test_streamlit_cockpit_contracts.py`.
- `CON-REL-001` Version consistency: VERSION, pyproject, app version, output manifests and model cards must agree. Gate: `python scripts/check_version_consistency.py`.
- `CON-SELF-001` No automatic self-learning release: evidence monitoring creates review candidates only. Gate: `models/tests/test_public_evidence_monitor.py`.

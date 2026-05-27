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

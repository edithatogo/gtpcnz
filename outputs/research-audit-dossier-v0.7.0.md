# Research audit dossier v0.7.0

## Purpose

This dossier records the audit status after adding uncertainty analysis and calibration-readiness artefacts.

## New artefacts

| Artefact | Purpose |
|---|---|
| `models/primarycare_model/uncertainty.py` | Executable uncertainty and sensitivity utilities |
| `docs/modelling/parameter-prior-register-v0.7.0.csv` | Parameter meanings, demonstrative ranges and evidence needs |
| `docs/modelling/monte-carlo-scenario-summary-v0.7.0.csv` | Scenario-level uncertainty summary |
| `docs/modelling/sensitivity-driver-ranking-welfare-v0.7.0.csv` | Game-level welfare sensitivity ranking |
| `docs/modelling/sensitivity-driver-ranking-hospital-pressure-v0.7.0.csv` | Game-level hospital-pressure sensitivity ranking |
| `docs/modelling/scenario-probability-comparisons-v0.7.0.csv` | Demonstrative comparison with S0 |
| `docs/audit/validation-backlog-v0.7.0.csv` | Game-by-game validation tasks |
| `docs/audit/evidence-priority-register-v0.7.0.csv` | Parameter-by-parameter evidence priorities |
| `docs/modelling/calibration-protocol-v0.7.0.md` | Protocol for moving from demonstrative to calibrated modelling |
| `docs/modelling/uncertainty-analysis-report-v0.7.0.md` | Narrative report of the uncertainty analysis |

## Quality-gate update

| Gate | v0.7.0 status |
|---|---|
| Conceptual game mapping | Passed |
| Demonstrative model for each game | Passed |
| Uncertainty stress test | Passed at demonstrative stage |
| Parameter register | Passed at demonstrative stage |
| Sensitivity ranking | Passed at demonstrative stage |
| Calibration protocol | Passed |
| Empirical calibration | Not yet passed |
| Stakeholder validation | Not yet passed |
| Equity/Te Tiriti validation | Not yet passed |
| Fiscal validation | Not yet passed |

## Research integrity statement

The v0.7.0 artefacts should be described as a **demonstrative and calibration-readiness package**. They should not be described as calibrated empirical evidence.

Permitted wording:

> The policy game has been mapped, converted into executable demonstrative models, stress-tested under uncertainty and prepared for empirical calibration.

Avoid:

> The model proves that a Primary Care Benefits Schedule will reduce hospital demand.

## Main audit risk

The main audit risk is that the model could be mistaken for evidence rather than a transparent hypothesis-testing framework. This is managed by:

- explicit labelling of all outputs as demonstrative;
- parameter-prior register;
- validation backlog;
- falsification criteria;
- calibration protocol;
- scenario S4 showing the risk of weak controls.

"""Generate v1.7.0 full-parameterisation outputs."""
from __future__ import annotations

from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "models"))

import matplotlib.pyplot as plt
import pandas as pd

from primarycare_model.full_parameterised_model_v170 import (
    parameter_register,
    data_input_contract,
    scenario_matrix,
    run_all_scenarios,
    sensitivity_analysis,
    calibration_target_matrix,
)

OUT = ROOT / "outputs"
FIG = OUT / "figures"
DOC = ROOT / "docs" / "calibration"
OUT.mkdir(exist_ok=True)
FIG.mkdir(exist_ok=True)
DOC.mkdir(exist_ok=True)

reg = parameter_register()
data = data_input_contract()
scen = scenario_matrix()
monthly, summary = run_all_scenarios(months=60)
sens = sensitivity_analysis("F4")
targets = calibration_target_matrix()

# Write CSVs to outputs and docs/calibration.
for path in [OUT, DOC]:
    reg.to_csv(path / "full-parameter-register-v1.7.0.csv", index=False)
    data.to_csv(path / "data-input-contract-v1.7.0.csv", index=False)
    scen.to_csv(path / "scenario-parameter-matrix-v1.7.0.csv", index=False)
    monthly.to_csv(path / "full-parameterised-monthly-results-v1.7.0.csv", index=False)
    summary.to_csv(path / "full-parameterised-summary-results-v1.7.0.csv", index=False)
    sens.to_csv(path / "full-parameterised-sensitivity-v1.7.0.csv", index=False)
    targets.to_csv(path / "calibration-target-matrix-v1.7.0.csv", index=False)

# Compact summary tables for reporting.
summary_short = summary[[
    "rank_by_hybrid_viability", "scenario_id", "scenario_name", "hybrid_viability_score",
    "access_score", "supply_generation_score", "hospital_pressure_score", "fiscal_risk_score", "gaming_risk_score",
    "mean_last12_primary_contacts_per_1000", "mean_last12_ed_events_per_100k", "mean_last12_public_cost_index",
]].sort_values("rank_by_hybrid_viability")
summary_short.to_csv(OUT / "full-parameterised-dashboard-table-v1.7.0.csv", index=False)

# Figure 1: scenario viability and pressure.
plot_df = summary.sort_values("hybrid_viability_score", ascending=True)
fig, ax = plt.subplots(figsize=(10, 6))
ax.barh(plot_df["scenario_name"], plot_df["hybrid_viability_score"], label="Hybrid viability")
ax.scatter(plot_df["hospital_pressure_score"], plot_df["scenario_name"], marker="o", label="Hospital pressure")
ax.set_xlabel("Score (0-100)")
ax.set_title("Full parameterised model: scenario viability and hospital pressure")
ax.legend(loc="lower right")
fig.tight_layout()
fig.savefig(FIG / "full-parameterised-scenario-viability-pressure-v1.7.0.png", dpi=180)
plt.close(fig)

# Figure 2: monthly hospital pressure trajectories.
fig, ax = plt.subplots(figsize=(10, 6))
for scenario_id in ["F0", "F3", "F4", "F5", "F6"]:
    df = monthly[monthly["scenario_id"] == scenario_id]
    label = df["scenario_name"].iloc[0]
    ax.plot(df["month"], df["hospital_pressure_index"], label=label)
ax.set_xlabel("Month")
ax.set_ylabel("Hospital pressure index")
ax.set_title("Hospital pressure trajectories under selected scenarios")
ax.legend(fontsize=8)
fig.tight_layout()
fig.savefig(FIG / "full-parameterised-hospital-pressure-trajectories-v1.7.0.png", dpi=180)
plt.close(fig)

# Figure 3: access vs fiscal risk.
fig, ax = plt.subplots(figsize=(8, 6))
ax.scatter(summary["fiscal_risk_score"], summary["access_score"])
for _, row in summary.iterrows():
    ax.annotate(row["scenario_id"], (row["fiscal_risk_score"], row["access_score"]), xytext=(4, 3), textcoords="offset points")
ax.set_xlabel("Fiscal risk score")
ax.set_ylabel("Access score")
ax.set_title("Access versus fiscal risk: controlled versus weak-control options")
fig.tight_layout()
fig.savefig(FIG / "full-parameterised-access-vs-fiscal-risk-v1.7.0.png", dpi=180)
plt.close(fig)

# Figure 4: top sensitivity drivers. Aggregate by max absolute viability change.
top = sens.groupby(["parameter", "domain"], as_index=False)["abs_viability_change"].max().sort_values("abs_viability_change", ascending=False).head(15).sort_values("abs_viability_change", ascending=True)
fig, ax = plt.subplots(figsize=(9, 7))
ax.barh(top["parameter"], top["abs_viability_change"])
ax.set_xlabel("Absolute change in hybrid viability score after ±0.08 perturbation")
ax.set_title("Top sensitivity drivers for the full hybrid scenario")
fig.tight_layout()
fig.savefig(FIG / "full-parameterised-top-sensitivity-drivers-v1.7.0.png", dpi=180)
plt.close(fig)

# Figure 5: parameter domain counts.
domain_counts = reg.groupby("domain").size().sort_values(ascending=True)
fig, ax = plt.subplots(figsize=(9, 7))
ax.barh(domain_counts.index, domain_counts.values)
ax.set_xlabel("Number of parameters")
ax.set_title("Parameter coverage by domain")
fig.tight_layout()
fig.savefig(FIG / "full-parameterised-parameter-domain-coverage-v1.7.0.png", dpi=180)
plt.close(fig)

# Markdown report.
report = f"""# Full parameterised model build report v1.7.0

## Status

This release continues the fully parameterised model build. It does **not** claim to be a real-data calibrated predictive model. It now provides a complete parameterisation scaffold: every major modelling mechanism has an explicit parameter, bounds, source status, real-data requirement and estimation strategy.

## What changed

- Expanded the parameter register from the earlier compact source-informed layer to **{len(reg)} explicit parameters** across demand, supply, funding, governance, ambulance, hospital, equity, risk and implementation domains.
- Added a **data-input contract** with **{len(data)} required input tables** for future empirical calibration.
- Added **{len(scen)} policy scenarios**, including current reform, uncapped scheduled medical fee-for-service, controlled full hybrid architecture, weak-control uncapping, ACC constraint shock, urgent/ambulance-only, scope-only and place-only scenarios.
- Added a 60-month dynamic simulation linking supply generation, access, unmet need, ambulance conveyance, emergency department events, admissions, hospital pressure and public cost.
- Added one-at-a-time sensitivity analysis and a calibration-target matrix.

## Scenario results

{summary_short.to_markdown(index=False)}

## Interpretation

The full hybrid upstream architecture continues to rank highest in this parameterised scaffold. The model distinguishes this from an uncontrolled uncapped model. The weak-control scenario improves the marginal activity signal but scores poorly on gaming, fiscal leakage and place/equity safeguards.

The result should be read as a structured modelling hypothesis, not as a forecast. The model is ready to accept real data, but the values remain priors/placeholders until linked data and stakeholder validation are available.

## Top sensitivity drivers

{top.sort_values('abs_viability_change', ascending=False).to_markdown(index=False)}

## Output tables

- `full-parameter-register-v1.7.0.csv`
- `data-input-contract-v1.7.0.csv`
- `scenario-parameter-matrix-v1.7.0.csv`
- `full-parameterised-monthly-results-v1.7.0.csv`
- `full-parameterised-summary-results-v1.7.0.csv`
- `full-parameterised-sensitivity-v1.7.0.csv`
- `calibration-target-matrix-v1.7.0.csv`

## Figures

- `outputs/figures/full-parameterised-scenario-viability-pressure-v1.7.0.png`
- `outputs/figures/full-parameterised-hospital-pressure-trajectories-v1.7.0.png`
- `outputs/figures/full-parameterised-access-vs-fiscal-risk-v1.7.0.png`
- `outputs/figures/full-parameterised-top-sensitivity-drivers-v1.7.0.png`
- `outputs/figures/full-parameterised-parameter-domain-coverage-v1.7.0.png`

## What this enables next

1. Replace placeholder priors with actual values from capitation, PHO, ACC, ambulance, NPCD, ED, hospital and workforce data.
2. Fit the transition parameters for marginal supply, price response, unmet-need conversion, ambulance deflection and ACC stabilisation.
3. Use temporal and geographic validation before making any predictive claims.
4. Feed the updated scenario outputs into the existing MCDA layer.

## Caveat

This is a fully specified parameterisation framework, not a completed empirical calibration. It makes the model auditable and data-ready, but does not yet estimate real-world effect sizes.
"""
(DOC / "full-parameterised-model-build-report-v1.7.0.md").write_text(report, encoding="utf-8")
(OUT / "full-parameterised-model-build-report-v1.7.0.md").write_text(report, encoding="utf-8")

# Equation/logic map.
equation_map = pd.DataFrame([
    {"model_layer": "demand burden", "inputs": "chronic need, rurality, deprivation, multimorbidity", "output": "demand_burden", "real_data_needed": "NPCD/NES/NZDep/rurality/multimorbidity"},
    {"model_layer": "marginal payment", "inputs": "scheduled benefit strength, price adequacy, activity signal, ACC activity, global cap", "output": "marginal_payment_signal", "real_data_needed": "item prices, marginal costs, ACC payments, capitation rules"},
    {"model_layer": "supply generation", "inputs": "marginal payment, scope capacity, direct claiming, rural loading, market entry, local in-person constraint", "output": "supply_generation", "real_data_needed": "workforce, open books, claim volume, practice entry/exit"},
    {"model_layer": "access", "inputs": "supply generation, urgent/ambulance alternatives, telehealth, co-payment burden, demand burden", "output": "access_index", "real_data_needed": "appointment/wait data, fees, mode, urgency"},
    {"model_layer": "hospital deflection", "inputs": "access, urgent/ambulance alternatives, data/KPIs, place accountability, scope capacity, demand burden", "output": "hospital_deflection", "real_data_needed": "linked primary/ambulance/ED/admission data"},
    {"model_layer": "risk", "inputs": "low-value activity, moral hazard, fiscal leakage, cherry-picking, governance, item rules", "output": "gaming_risk and fiscal_risk", "real_data_needed": "claims, audit, outliers, re-presentations, equity monitoring"},
    {"model_layer": "monthly dynamics", "inputs": "access, supply generation, unmet need persistence, ED conversion, ambulance conveyance, admissions, costs", "output": "monthly outcomes", "real_data_needed": "monthly panels and event linkages"},
])
equation_map.to_csv(OUT / "model-logic-map-v1.7.0.csv", index=False)
equation_map.to_csv(DOC / "model-logic-map-v1.7.0.csv", index=False)

print("Wrote v1.7.0 outputs")

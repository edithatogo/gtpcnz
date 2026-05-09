from pathlib import Path
import pandas as pd
import matplotlib.pyplot as plt

from primarycare_model.uncertainty import (
    parameter_prior_rows,
    run_monte_carlo,
    summarise_uncertainty,
    rank_sensitivity,
    scenario_pairwise_probabilities,
)

ROOT = Path(__file__).resolve().parents[1]
DOCS = ROOT / "docs"
MODELLING = DOCS / "modelling"
FIGURES = DOCS / "figures"
AUDIT = DOCS / "audit"
OUTPUTS = ROOT / "outputs"
for directory in [MODELLING, FIGURES, AUDIT, OUTPUTS]:
    directory.mkdir(parents=True, exist_ok=True)

# Use 1,000 draws per scenario for a stable but lightweight demonstrative stress test.
draws = run_monte_carlo(n_per_scenario=1000, sd=0.08, seed=20260507)
summary = summarise_uncertainty(draws)
sens_welfare = rank_sensitivity(draws, outcome_metric="system_welfare", top_n=8)
sens_hospital = rank_sensitivity(draws, outcome_metric="hospital_pressure", top_n=8)
sens_welfare_by_scenario = rank_sensitivity(
    draws,
    outcome_metric="system_welfare",
    by=("scenario_id", "scenario_name", "game_id", "game_name"),
    top_n=5,
)
sens_hospital_by_scenario = rank_sensitivity(
    draws,
    outcome_metric="hospital_pressure",
    by=("scenario_id", "scenario_name", "game_id", "game_name"),
    top_n=5,
)
prob = scenario_pairwise_probabilities(draws)
priors = pd.DataFrame(parameter_prior_rows()).round(3)

# Write core outputs.
draw_sample = draws.sample(n=min(5000, len(draws)), random_state=20260507).round(3)
priors.to_csv(MODELLING / "parameter-prior-register-v0.7.0.csv", index=False)
summary.to_csv(MODELLING / "monte-carlo-scenario-summary-v0.7.0.csv", index=False)
sens_welfare.to_csv(MODELLING / "sensitivity-driver-ranking-welfare-v0.7.0.csv", index=False)
sens_hospital.to_csv(MODELLING / "sensitivity-driver-ranking-hospital-pressure-v0.7.0.csv", index=False)
sens_welfare_by_scenario.to_csv(MODELLING / "sensitivity-driver-ranking-welfare-by-scenario-v0.7.0.csv", index=False)
sens_hospital_by_scenario.to_csv(MODELLING / "sensitivity-driver-ranking-hospital-pressure-by-scenario-v0.7.0.csv", index=False)
prob.to_csv(MODELLING / "scenario-probability-comparisons-v0.7.0.csv", index=False)
draw_sample.to_csv(MODELLING / "monte-carlo-draw-sample-v0.7.0.csv", index=False)

# Also copy key outputs to /outputs for download convenience.
for src in [
    MODELLING / "parameter-prior-register-v0.7.0.csv",
    MODELLING / "monte-carlo-scenario-summary-v0.7.0.csv",
    MODELLING / "sensitivity-driver-ranking-welfare-v0.7.0.csv",
    MODELLING / "sensitivity-driver-ranking-hospital-pressure-v0.7.0.csv",
    MODELLING / "scenario-probability-comparisons-v0.7.0.csv",
    MODELLING / "sensitivity-driver-ranking-welfare-by-scenario-v0.7.0.csv",
    MODELLING / "sensitivity-driver-ranking-hospital-pressure-by-scenario-v0.7.0.csv",
]:
    (OUTPUTS / src.name).write_text(src.read_text())

# Figure 1: boxplot of welfare by scenario.
scenario_order = ["S0", "S1", "S2", "S3", "S4"]
scenario_labels = [
    "S0\nStatus quo",
    "S1\nReweighting",
    "S2\nBenefits",
    "S3\nFull upstream",
    "S4\nWeak controls",
]
plot_data = [draws.loc[draws["scenario_id"] == sid, "system_welfare"].astype(float).values for sid in scenario_order]
plt.figure(figsize=(9, 5))
plt.boxplot(plot_data, labels=scenario_labels, showfliers=False)
plt.ylabel("Demonstrative system welfare score")
plt.title("Uncertainty stress test: welfare distribution by scenario")
plt.tight_layout()
plt.savefig(FIGURES / "uncertainty-welfare-by-scenario-v0.7.0.png", dpi=200)
plt.savefig(OUTPUTS / "uncertainty-welfare-by-scenario-v0.7.0.png", dpi=200)
plt.close()

# Figure 2: top welfare sensitivity drivers aggregated across games.
agg = (
    sens_welfare.groupby("parameter", as_index=False)["abs_correlation"]
    .mean()
    .sort_values("abs_correlation", ascending=False)
    .head(10)
    .sort_values("abs_correlation", ascending=True)
)
plt.figure(figsize=(8, 5))
plt.barh(agg["parameter"], agg["abs_correlation"])
plt.xlabel("Mean absolute correlation with welfare")
plt.title("Top demonstrative welfare sensitivity drivers")
plt.tight_layout()
plt.savefig(FIGURES / "sensitivity-top-welfare-drivers-v0.7.0.png", dpi=200)
plt.savefig(OUTPUTS / "sensitivity-top-welfare-drivers-v0.7.0.png", dpi=200)
plt.close()

# Figure 3: hospital pressure with 5-95% uncertainty intervals.
intervals = summary[[
    "scenario_id", "scenario_name", "hospital_pressure_mean", "hospital_pressure_p05", "hospital_pressure_p95"
]].copy()
intervals["scenario_label"] = intervals["scenario_id"]
intervals = intervals.set_index("scenario_id").loc[scenario_order].reset_index()
x = range(len(intervals))
y = intervals["hospital_pressure_mean"].astype(float)
yerr = [
    (y - intervals["hospital_pressure_p05"].astype(float)).values,
    (intervals["hospital_pressure_p95"].astype(float) - y).values,
]
plt.figure(figsize=(8, 5))
plt.errorbar(list(x), y, yerr=yerr, fmt="o", capsize=4)
plt.xticks(list(x), scenario_labels)
plt.ylabel("Demonstrative hospital pressure score")
plt.title("Hospital pressure uncertainty interval by scenario")
plt.tight_layout()
plt.savefig(FIGURES / "uncertainty-hospital-pressure-v0.7.0.png", dpi=200)
plt.savefig(OUTPUTS / "uncertainty-hospital-pressure-v0.7.0.png", dpi=200)
plt.close()

# Audit validation backlog.
backlog_rows = []
game_names = draws[["game_id", "game_name"]].drop_duplicates().sort_values("game_id")
for _, row in game_names.iterrows():
    game_id = row["game_id"]
    game_name = row["game_name"]
    top_w = sens_welfare[sens_welfare["game_id"] == game_id].head(3)["parameter"].tolist()
    top_h = sens_hospital[sens_hospital["game_id"] == game_id].head(3)["parameter"].tolist()
    backlog_rows.append(
        {
            "game_id": game_id,
            "game_name": game_name,
            "top_welfare_drivers": "; ".join(top_w),
            "top_hospital_pressure_drivers": "; ".join(top_h),
            "minimum_next_evidence": "empirical estimates for top drivers plus stakeholder validation of mechanism",
            "validation_status": "not empirically calibrated",
            "suggested_validation_method": "OIA/data extraction + stakeholder workshop + sensitivity recalibration",
        }
    )
backlog = pd.DataFrame(backlog_rows)
backlog.to_csv(AUDIT / "validation-backlog-v0.7.0.csv", index=False)
backlog.to_csv(OUTPUTS / "validation-backlog-v0.7.0.csv", index=False)

# Evidence priority register by parameter.
priority = priors.copy()
priority["minimum_viable_validation_question"] = priority["parameter"].map(
    lambda p: f"What empirical range and central tendency should be used for {p}, and does stakeholder evidence support its direction of effect?"
)
priority.to_csv(AUDIT / "evidence-priority-register-v0.7.0.csv", index=False)
priority.to_csv(OUTPUTS / "evidence-priority-register-v0.7.0.csv", index=False)

print("wrote v0.7.0 uncertainty outputs")

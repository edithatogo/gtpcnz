"""Run v0.6.0 demonstrative game models and write CSV/figure outputs."""

from __future__ import annotations

import csv
from dataclasses import replace
from pathlib import Path
import sys

import matplotlib.pyplot as plt

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "models"))

from primarycare_model.demonstrative_games import GAME_MODELS, SCENARIOS, Scenario, run_all, scenarios_as_rows, summarise_by_scenario  # noqa: E402

OUT_DIR = ROOT / "outputs"
FIG_DIR = ROOT / "docs" / "figures"
MODEL_DOC_DIR = ROOT / "docs" / "modelling"


def write_csv(path: Path, rows: list[dict[str, object]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if not rows:
        return
    with path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)


def make_summary_rows(summary: dict[str, dict[str, float]]) -> list[dict[str, object]]:
    scenario_names = {
        "S0": "Status quo tight control",
        "S1": "Capitation reweighting only",
        "S2": "Primary Care Benefits Schedule",
        "S3": "Full upstream access architecture",
        "S4": "Loose benefits, weak controls",
    }
    rows: list[dict[str, object]] = []
    for scenario_id, metrics in summary.items():
        row: dict[str, object] = {"scenario_id": scenario_id, "scenario_name": scenario_names[scenario_id]}
        row.update({key: round(value, 2) for key, value in metrics.items()})
        rows.append(row)
    return rows


def save_bar_chart(summary_rows: list[dict[str, object]]) -> None:
    FIG_DIR.mkdir(parents=True, exist_ok=True)
    labels = [str(r["scenario_id"]) for r in summary_rows]
    welfare = [float(r["mean_system_welfare"]) for r in summary_rows]
    pressure = [float(r["mean_hospital_pressure"]) for r in summary_rows]

    fig = plt.figure(figsize=(9, 5.2))
    ax = fig.add_subplot(111)
    x = list(range(len(labels)))
    width = 0.35
    ax.bar([i - width / 2 for i in x], welfare, width, label="Mean system welfare")
    ax.bar([i + width / 2 for i in x], [100 - p for p in pressure], width, label="Inverse hospital pressure")
    ax.set_xticks(x)
    ax.set_xticklabels(labels)
    ax.set_ylabel("Score (0-100)")
    ax.set_title("Demonstrative game model summary by scenario")
    ax.legend()
    ax.text(0, -18, "S0 status quo; S1 reweighting; S2 benefits; S3 full architecture; S4 weak controls", transform=ax.transData, fontsize=8)
    fig.tight_layout()
    fig.savefig(FIG_DIR / "demonstrative-game-summary-v0.6.0.png", dpi=180)
    plt.close(fig)


def save_game_pressure_chart(outcome_rows: list[dict[str, object]]) -> None:
    FIG_DIR.mkdir(parents=True, exist_ok=True)
    games = [f"G{i}" for i in range(1, 15)]
    scenarios = ["S0", "S1", "S2", "S3", "S4"]
    by_key = {(str(r["game_id"]), str(r["scenario_id"])): float(r["hospital_pressure"]) for r in outcome_rows}

    fig = plt.figure(figsize=(11, 6))
    ax = fig.add_subplot(111)
    x = list(range(len(games)))
    width = 0.16
    for idx, scenario_id in enumerate(scenarios):
        values = [by_key[(game, scenario_id)] for game in games]
        offsets = [i + (idx - 2) * width for i in x]
        ax.bar(offsets, values, width, label=scenario_id)
    ax.set_xticks(x)
    ax.set_xticklabels(games)
    ax.set_ylabel("Hospital pressure score (lower is better)")
    ax.set_title("Demonstrative hospital-pressure result by game")
    ax.legend()
    fig.tight_layout()
    fig.savefig(FIG_DIR / "demonstrative-hospital-pressure-by-game-v0.6.0.png", dpi=180)
    plt.close(fig)


def write_markdown_report(summary_rows: list[dict[str, object]], outcome_rows: list[dict[str, object]]) -> None:
    MODEL_DOC_DIR.mkdir(parents=True, exist_ok=True)
    lines: list[str] = []
    lines.append("# Demonstrative game modelling report v0.6.0\n")
    lines.append("Status: demonstrative, non-calibrated, hypothesis-testing scaffold.\n")
    lines.append("This report turns each of the 14 mapped New Zealand policy games into a small executable model. The outputs are not empirical estimates. They are structured demonstrations of how the hypothesised mechanisms behave under contrasting policy architectures.\n")
    lines.append("## Scenarios\n")
    lines.append("| Scenario | Description |\n|---|---|\n")
    lines.append("| S0 | Status quo tight control: dominant capitation/contracting, PHO intermediation, limited marginal benefit, high hospital salience. |\n")
    lines.append("| S1 | Capitation reweighting only: better allocation inside capitation, modest access target/data improvement, no material demand-driven benefit stream. |\n")
    lines.append("| S2 | Primary Care Benefits Schedule: contact-type benefits added to capitation, optional/direct claiming and moderate safeguards. |\n")
    lines.append("| S3 | Full upstream access architecture: benefits schedule plus strong KPIs, data, ambulance alternatives, scope flexibility and equity protections. |\n")
    lines.append("| S4 | Loose benefits, weak controls: high benefit activity with weak governance, weak equity protections and high gaming risk. |\n")
    lines.append("\n## Mean scenario results\n")
    lines.append("| Scenario | Access | Viability | Equity | Fiscal control | Hospital pressure | Gaming risk | Welfare |\n|---|---:|---:|---:|---:|---:|---:|---:|\n")
    for r in summary_rows:
        lines.append(
            f"| {r['scenario_id']} | {r['mean_access_score']} | {r['mean_provider_viability']} | {r['mean_equity_score']} | {r['mean_fiscal_control']} | {r['mean_hospital_pressure']} | {r['mean_gaming_risk']} | {r['mean_system_welfare']} |\n"
        )
    lines.append("\n## Interpretation\n")
    lines.append("Across the demonstrative parameterisation, S1 improves equity and information relative to S0 but does not fully reverse the marginal-supply problem. S2 and S3 improve access and reduce hospital pressure because eligible activity can expand. S4 is deliberately included as a caution: unrestricted demand-driven benefits without strong governance improve access but materially increase gaming, equity and safety risk.\n")
    lines.append("\n## Per-game model cards\n")
    for game_id in [f"G{i}" for i in range(1, 15)]:
        game_rows = [r for r in outcome_rows if r["game_id"] == game_id]
        game_name = game_rows[0]["game_name"]
        lines.append(f"\n### {game_id}: {game_name}\n")
        lines.append(f"Mechanism: {game_rows[0]['mechanism_summary']}\n\n")
        lines.append("| Scenario | Equilibrium label | Access | Hospital pressure | Gaming risk | Welfare |\n|---|---|---:|---:|---:|---:|\n")
        for r in game_rows:
            lines.append(
                f"| {r['scenario_id']} | {r['equilibrium_label']} | {r['access_score']} | {r['hospital_pressure']} | {r['gaming_risk']} | {r['system_welfare']} |\n"
            )
    lines.append("\n## Sensitivity analysis\n")
    lines.append("A one-at-a-time sensitivity table around S2 is available in `demonstrative-model-sensitivity-v0.6.0.csv`. It varies one key lever for each game by +/-0.20 on the normalised scale and records welfare and hospital-pressure changes.\n")
    lines.append("\n## Limitations\n")
    lines.append("These models use stylised normalised parameters and transparent formulae. They are intended to demonstrate mechanism plausibility and support stakeholder challenge. They should not be used as forecasts. Empirical calibration requires OIA material, administrative datasets, stakeholder validation and sensitivity analysis.\n")
    (MODEL_DOC_DIR / "demonstrative-modelling-report-v0.6.0.md").write_text("".join(lines), encoding="utf-8")


def write_model_cards(outcome_rows: list[dict[str, object]]) -> None:
    MODEL_DOC_DIR.mkdir(parents=True, exist_ok=True)
    lines = ["# Demonstrative model cards v0.6.0\n\n", "Each card records the demonstrative model status for one mapped game.\n"]
    for game_id in [f"G{i}" for i in range(1, 15)]:
        rows = [r for r in outcome_rows if r["game_id"] == game_id]
        lines.append(f"\n## {game_id}: {rows[0]['game_name']}\n")
        lines.append(f"- **Mechanism:** {rows[0]['mechanism_summary']}\n")
        best = max(rows, key=lambda r: float(r["system_welfare"]))
        worst_pressure = max(rows, key=lambda r: float(r["hospital_pressure"]))
        highest_risk = max(rows, key=lambda r: float(r["gaming_risk"]))
        lines.append(f"- **Highest welfare scenario:** {best['scenario_id']} ({best['scenario_name']}) with welfare {best['system_welfare']}.\n")
        lines.append(f"- **Highest hospital-pressure scenario:** {worst_pressure['scenario_id']} ({worst_pressure['scenario_name']}) with pressure {worst_pressure['hospital_pressure']}.\n")
        lines.append(f"- **Highest gaming-risk scenario:** {highest_risk['scenario_id']} ({highest_risk['scenario_name']}) with risk {highest_risk['gaming_risk']}.\n")
        lines.append("- **Audit status:** Demonstrative only; requires calibration and stakeholder validation.\n")
    (MODEL_DOC_DIR / "demonstrative-model-cards-v0.6.0.md").write_text("".join(lines), encoding="utf-8")


def make_sensitivity_rows() -> list[dict[str, object]]:
    """One-at-a-time sensitivity around S2 for the key lever in each game."""

    base = next(s for s in SCENARIOS if s.scenario_id == "S2")
    key_levers = {
        "G1": "primary_kpi_salience",
        "G2": "primary_kpi_salience",
        "G3": "marginal_contact_benefit",
        "G4": "copayment_protections",
        "G5": "direct_claiming",
        "G6": "acc_constraint",
        "G7": "ambulance_alternative_funding",
        "G8": "scope_flexibility",
        "G9": "telehealth_integration",
        "G10": "copayment_protections",
        "G11": "gaming_controls",
        "G12": "equity_program_strength",
        "G13": "narrative_coherence",
        "G14": "data_observability",
    }
    rows: list[dict[str, object]] = []
    for game_id, lever in key_levers.items():
        model = GAME_MODELS[game_id]
        base_outcome = model(base)
        base_value = getattr(base, lever)
        for direction, delta in [("low", -0.20), ("high", 0.20)]:
            new_value = max(0.0, min(1.0, base_value + delta))
            scenario = replace(base, scenario_id=f"S2_{game_id}_{direction}", name=f"S2 sensitivity {game_id} {direction}", **{lever: new_value})
            outcome = model(scenario)
            rows.append({
                "game_id": game_id,
                "game_name": outcome.game_name,
                "lever": lever,
                "direction": direction,
                "base_value": round(base_value, 3),
                "new_value": round(new_value, 3),
                "base_welfare": round(base_outcome.system_welfare, 2),
                "new_welfare": round(outcome.system_welfare, 2),
                "delta_welfare": round(outcome.system_welfare - base_outcome.system_welfare, 2),
                "base_hospital_pressure": round(base_outcome.hospital_pressure, 2),
                "new_hospital_pressure": round(outcome.hospital_pressure, 2),
                "delta_hospital_pressure": round(outcome.hospital_pressure - base_outcome.hospital_pressure, 2),
                "interpretation": "Positive welfare delta and negative pressure delta support the proposed lever direction." if direction == "high" else "Low lever setting tests fragility of the mechanism.",
            })
    return rows


def main() -> None:
    outcomes = run_all()
    outcome_rows = [outcome.as_row() for outcome in outcomes]
    summary_rows = make_summary_rows(summarise_by_scenario(outcomes))
    scenario_rows = scenarios_as_rows()
    sensitivity_rows = make_sensitivity_rows()

    write_csv(OUT_DIR / "demonstrative-model-results-v0.6.0.csv", outcome_rows)
    write_csv(OUT_DIR / "demonstrative-model-summary-v0.6.0.csv", summary_rows)
    write_csv(MODEL_DOC_DIR / "demonstrative-model-scenario-inputs-v0.6.0.csv", scenario_rows)
    write_csv(MODEL_DOC_DIR / "demonstrative-model-results-v0.6.0.csv", outcome_rows)
    write_csv(MODEL_DOC_DIR / "demonstrative-model-summary-v0.6.0.csv", summary_rows)
    write_csv(OUT_DIR / "demonstrative-model-sensitivity-v0.6.0.csv", sensitivity_rows)
    write_csv(MODEL_DOC_DIR / "demonstrative-model-sensitivity-v0.6.0.csv", sensitivity_rows)
    save_bar_chart(summary_rows)
    save_game_pressure_chart(outcome_rows)
    write_markdown_report(summary_rows, outcome_rows)
    write_model_cards(outcome_rows)


if __name__ == "__main__":
    main()

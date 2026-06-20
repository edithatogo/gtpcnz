from __future__ import annotations

import json
import shutil
from dataclasses import dataclass
from datetime import UTC, datetime
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
from PIL import Image

ROOT = Path(__file__).resolve().parents[1]
FIGURES = ROOT / "docs" / "substack-ready" / "figures"
REPORTS = ROOT / "reports"
FILENAMES = [
    "pcf-v172-sim-01-supply-pressure-plot.png",
    "pcf-v172-sim-02-funding-comparison-plot.png",
    "pcf-v172-sim-03-marginal-supply-plot.png",
    "pcf-v172-sim-04-gaming-risk-frontier-plot.png",
    "pcf-v172-sim-05-current-vs-hybrid-plot.png",
    "pcf-v172-sim-06-payment-control-plot.png",
]

COLORS = {
    "ink": "#1f2d2b",
    "muted": "#687879",
    "grid": "#d8e1de",
    "green": "#2f7668",
    "green2": "#72a77a",
    "gold": "#c88a2d",
    "red": "#b95a4a",
    "blue": "#2a5f9e",
    "slate": "#95a6aa",
    "sand": "#ead7b8",
}


@dataclass
class Score:
    filename: str
    width: int
    height: int
    score: float
    text_density_penalty: float
    whitespace_penalty: float
    aspect_penalty: float
    component_penalty: float


def main() -> None:
    REPORTS.mkdir(exist_ok=True)
    before = score_all()
    backup_dir = backup_existing()
    render_all()
    after = score_all()
    render_contact_sheet()
    stamp = datetime.now(UTC).isoformat().replace(":", "-").replace(".", "-")
    report = {
        "createdAt": datetime.now(UTC).isoformat(),
        "backupDir": str(backup_dir.relative_to(ROOT)),
        "scoringMethod": (
            "100 minus penalties for text-like dark pixel density, low whitespace, "
            "small canvas/aspect, and excessive connected components. This is a "
            "publication-readability heuristic, not an OCR model."
        ),
        "threshold": 95,
        "before": [score.__dict__ for score in before],
        "after": [score.__dict__ for score in after],
        "passed": all(score.score >= 95 for score in after),
    }
    report_path = REPORTS / f"substack-simulation-plot-polish-{stamp}.json"
    latest_path = REPORTS / "substack-simulation-plot-polish-latest.json"
    report_path.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    latest_path.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"report": str(report_path.relative_to(ROOT)), "passed": report["passed"], "after": report["after"]}, indent=2))
    if not report["passed"]:
        raise SystemExit("One or more polished plots scored below 95.")


def backup_existing() -> Path:
    stamp = datetime.now(UTC).strftime("%Y%m%dT%H%M%SZ")
    backup_dir = ROOT / ".tmp" / f"sim-plot-backup-{stamp}"
    backup_dir.mkdir(parents=True, exist_ok=True)
    for name in [*FILENAMES, "pcf-v172-sim-contact-sheet.png"]:
        source = FIGURES / name
        if source.exists():
            shutil.copy2(source, backup_dir / name)
    return backup_dir


def render_all() -> None:
    set_style()
    render_supply_pressure(FIGURES / FILENAMES[0])
    render_funding_comparison(FIGURES / FILENAMES[1])
    render_marginal_supply(FIGURES / FILENAMES[2])
    render_gaming_frontier(FIGURES / FILENAMES[3])
    render_current_vs_hybrid(FIGURES / FILENAMES[4])
    render_payment_control(FIGURES / FILENAMES[5])


def set_style() -> None:
    plt.rcParams.update(
        {
            "figure.dpi": 180,
            "savefig.dpi": 180,
            "font.family": "DejaVu Sans",
            "font.size": 13,
            "axes.titlesize": 22,
            "axes.labelsize": 14,
            "xtick.labelsize": 12,
            "ytick.labelsize": 12,
            "legend.fontsize": 12,
            "axes.edgecolor": "#aab8b4",
            "axes.labelcolor": COLORS["ink"],
            "xtick.color": COLORS["ink"],
            "ytick.color": COLORS["ink"],
            "text.color": COLORS["ink"],
        }
    )


def finish(fig: plt.Figure, ax: plt.Axes | None, path: Path, footer: str = "Illustrative indices; not a forecast.") -> None:
    if ax is not None:
        ax.grid(axis="y", color=COLORS["grid"], linewidth=0.8)
        ax.spines["top"].set_visible(False)
        ax.spines["right"].set_visible(False)
    fig.text(0.055, 0.035, footer, fontsize=9.5, color=COLORS["muted"])
    fig.savefig(path, bbox_inches="tight", pad_inches=0.22, facecolor="white")
    plt.close(fig)


def render_supply_pressure(path: Path) -> None:
    x = np.array([14.2, 13.8, 40.4, 40.1, 55.5, 37.2, 13.9, 14.3, 21.4, 15.0])
    y = np.array([78.4, 79.6, 75.9, 74.4, 61.8, 77.2, 80.1, 72.2, 78.3, 77.9])
    fig, ax = plt.subplots(figsize=(12.8, 7.2))
    ax.scatter(x, y, s=95, color=COLORS["slate"], alpha=0.95, edgecolor="white", linewidth=1.3)
    ax.scatter([55.5], [61.8], s=210, color=COLORS["green"], edgecolor=COLORS["ink"], linewidth=1.3, zorder=3)
    ax.annotate("Full hybrid", xy=(55.5, 61.8), xytext=(-88, -14), textcoords="offset points", fontsize=13, weight="bold")
    ax.annotate("Current cluster", xy=(14.2, 78.4), xytext=(16.8, 76.0), fontsize=12, color=COLORS["muted"], arrowprops={"arrowstyle": "-", "color": COLORS["muted"]})
    ax.set_title("Supply generation vs hospital pressure", loc="left", pad=14, weight="bold")
    ax.set_xlabel("Supply generation index")
    ax.set_ylabel("Hospital pressure index (lower is better)")
    ax.set_xlim(10, 60)
    ax.set_ylim(82, 58)
    ax.text(59, 80.4, "Lower pressure", ha="right", fontsize=11, color=COLORS["muted"])
    finish(fig, ax, path)


def render_funding_comparison(path: Path) -> None:
    categories = ["Access", "Supply", "Fiscal risk", "Gaming risk"]
    scenarios = ["Current", "Capitation", "Blend", "Hybrid", "Uncontrolled"]
    values = np.array(
        [
            [24, 15, 28, 34],
            [22, 14, 27, 35],
            [36, 40, 50, 39],
            [53, 56, 38, 27],
            [33, 37, 66, 70],
        ]
    )
    fig, ax = plt.subplots(figsize=(13.2, 7.4))
    x = np.arange(len(scenarios))
    width = 0.18
    palette = [COLORS["green"], COLORS["green2"], COLORS["gold"], COLORS["red"]]
    for i, category in enumerate(categories):
        ax.bar(x + (i - 1.5) * width, values[:, i], width, label=category, color=palette[i])
    ax.set_title("Funding design comparison", loc="left", pad=14, weight="bold")
    ax.set_ylabel("Model index score")
    ax.set_xticks(x)
    ax.set_xticklabels(scenarios)
    ax.set_ylim(0, 82)
    ax.legend(ncol=4, loc="upper center", bbox_to_anchor=(0.5, -0.11), frameon=False)
    finish(fig, ax, path)


def render_marginal_supply(path: Path) -> None:
    q = np.linspace(0, 100, 101)
    revenue = 72 - 0.34 * q
    cost = 22 + 0.26 * q
    crossing = q[np.argmin(np.abs(revenue - cost))]
    fig, ax = plt.subplots(figsize=(13.2, 7.4))
    ax.plot(q, revenue, color=COLORS["blue"], linewidth=3.2, label="Payment signal")
    ax.plot(q, cost, color=COLORS["red"], linewidth=3.2, label="Marginal cost")
    ax.fill_between(q, cost, revenue, where=revenue >= cost, color=COLORS["green2"], alpha=0.2, label="Viable band")
    ax.axvline(crossing, color=COLORS["muted"], linestyle="--", linewidth=1.8)
    ax.text(crossing + 2, 66, "Break-even", fontsize=11, color=COLORS["muted"])
    ax.set_title("Marginal revenue and marginal cost", loc="left", pad=14, weight="bold")
    ax.set_xlabel("Additional primary-care activity")
    ax.set_ylabel("Illustrative dollars / effort index")
    ax.set_xlim(0, 100)
    ax.set_ylim(18, 76)
    ax.legend(loc="upper center", bbox_to_anchor=(0.5, -0.11), ncol=3, frameon=False)
    finish(fig, ax, path)


def render_gaming_frontier(path: Path) -> None:
    control = np.linspace(0, 1, 44)
    access_gain = 20 + 55 * (control ** 0.88)
    residual_risk = 84 - 72 * (control ** 0.82)
    fig, ax = plt.subplots(figsize=(13.2, 7.4))
    scatter = ax.scatter(access_gain, residual_risk, c=control, cmap="viridis", s=72, edgecolor="white", linewidth=0.45)
    ax.set_title("Gaming-risk frontier", loc="left", pad=14, weight="bold")
    ax.set_xlabel("Access gain index")
    ax.set_ylabel("Residual gaming-risk index (lower is better)")
    ax.set_xlim(17, 78)
    ax.set_ylim(90, 5)
    ax.annotate("Weak controls", xy=(22, 82), xytext=(28, 72), fontsize=12, color=COLORS["muted"], arrowprops={"arrowstyle": "-", "color": COLORS["muted"]})
    ax.annotate("Strong controls", xy=(73, 14), xytext=(59, 20), fontsize=12, color=COLORS["muted"], arrowprops={"arrowstyle": "-", "color": COLORS["muted"]})
    colorbar = fig.colorbar(scatter, ax=ax, pad=0.018, fraction=0.045)
    colorbar.set_label("Control strength", fontsize=12)
    finish(fig, ax, path)


def render_current_vs_hybrid(path: Path) -> None:
    categories = ["Hybrid viability", "Access", "Supply", "Hospital deflection", "Governance"]
    current = np.array([52, 24, 15, 22, 56])
    hybrid = np.array([77, 53, 56, 50, 77])
    y = np.arange(len(categories))
    fig, ax = plt.subplots(figsize=(13.2, 7.4))
    ax.barh(y + 0.18, current, height=0.34, color=COLORS["slate"], label="Current reform")
    ax.barh(y - 0.18, hybrid, height=0.34, color=COLORS["green"], label="Full hybrid")
    ax.set_title("Current reform vs full hybrid", loc="left", pad=14, weight="bold")
    ax.set_xlabel("Model index score")
    ax.set_yticks(y)
    ax.set_yticklabels(categories)
    ax.set_xlim(0, 86)
    ax.invert_yaxis()
    ax.legend(loc="upper center", bbox_to_anchor=(0.5, -0.11), ncol=2, frameon=False)
    finish(fig, ax, path)


def render_payment_control(path: Path) -> None:
    q = np.linspace(0, 100, 101)
    gross = 18 + 1.05 * q
    control = np.where(q < 65, 0.22 * q, 14.3 + 1.18 * (q - 65))
    net = gross - control
    fig, ax = plt.subplots(figsize=(13.2, 7.4))
    ax.fill_between(q, net, gross, color=COLORS["sand"], alpha=0.75, label="Control adjustment")
    ax.plot(q, gross, color=COLORS["green2"], linewidth=3.0, label="Gross payment")
    ax.plot(q, net, color=COLORS["blue"], linewidth=3.2, label="Net incentive")
    ax.set_title("Activity payment with control adjustment", loc="left", pad=14, weight="bold")
    ax.set_xlabel("Eligible activity units")
    ax.set_ylabel("Illustrative payment / incentive index")
    ax.set_xlim(0, 100)
    ax.set_ylim(10, 130)
    ax.legend(loc="upper center", bbox_to_anchor=(0.5, -0.11), ncol=3, frameon=False)
    finish(fig, ax, path)


def score_all() -> list[Score]:
    return [score_image(FIGURES / name) for name in FILENAMES if (FIGURES / name).exists()]


def score_image(path: Path) -> Score:
    image = Image.open(path).convert("L")
    arr = np.array(image)
    height, width = arr.shape
    dark = arr < 95
    mid = arr < 145
    text_like = dark & (edge_proxy(arr) > 18)
    text_density = float(text_like.mean())
    white_fraction = float((arr > 245).mean())
    components = connected_component_count(mid[::3, ::3])
    text_density_penalty = max(0.0, (text_density - 0.022) * 900)
    whitespace_penalty = max(0.0, (0.50 - white_fraction) * 50)
    aspect = width / height
    aspect_penalty = 0.0 if 1.45 <= aspect <= 2.05 and width >= 1500 and height >= 850 else 6.0
    component_penalty = max(0.0, (components - 950) / 170)
    score = 100 - text_density_penalty - whitespace_penalty - aspect_penalty - component_penalty
    return Score(
        filename=path.name,
        width=width,
        height=height,
        score=round(max(0.0, min(100.0, score)), 1),
        text_density_penalty=round(text_density_penalty, 1),
        whitespace_penalty=round(whitespace_penalty, 1),
        aspect_penalty=round(aspect_penalty, 1),
        component_penalty=round(component_penalty, 1),
    )


def edge_proxy(arr: np.ndarray) -> np.ndarray:
    gx = np.abs(np.diff(arr.astype(float), axis=1, prepend=arr[:, :1]))
    gy = np.abs(np.diff(arr.astype(float), axis=0, prepend=arr[:1, :]))
    return gx + gy


def connected_component_count(mask: np.ndarray) -> int:
    seen = np.zeros(mask.shape, dtype=bool)
    count = 0
    rows, cols = mask.shape
    for row in range(rows):
        for col in range(cols):
            if not mask[row, col] or seen[row, col]:
                continue
            count += 1
            stack = [(row, col)]
            seen[row, col] = True
            while stack:
                r, c = stack.pop()
                for nr, nc in ((r - 1, c), (r + 1, c), (r, c - 1), (r, c + 1)):
                    if 0 <= nr < rows and 0 <= nc < cols and mask[nr, nc] and not seen[nr, nc]:
                        seen[nr, nc] = True
                        stack.append((nr, nc))
    return count


def render_contact_sheet() -> None:
    images = [Image.open(FIGURES / name).convert("RGB") for name in FILENAMES]
    thumb_width = 920
    thumbs = []
    for image in images:
        ratio = thumb_width / image.width
        thumbs.append(image.resize((thumb_width, int(image.height * ratio))))
    label_height = 44
    gap = 58
    width = thumb_width * 2 + gap * 3
    row_height = max(thumb.height for thumb in thumbs[:2]) + label_height + gap
    height = row_height * 3 + gap
    sheet = Image.new("RGB", (width, height), "white")
    for idx, thumb in enumerate(thumbs):
        row, col = divmod(idx, 2)
        x = gap + col * (thumb_width + gap)
        y = gap + row * row_height
        sheet.paste(thumb, (x, y))
    sheet.save(FIGURES / "pcf-v172-sim-contact-sheet.png")


if __name__ == "__main__":
    main()

from __future__ import annotations

import json
from datetime import UTC, datetime
from pathlib import Path

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


def main() -> None:
    backup_dir = original_backup_dir()
    before = [score_image(backup_dir / name) for name in FILENAMES]
    after = [score_image(FIGURES / name) for name in FILENAMES]
    report = {
        "createdAt": datetime.now(UTC).isoformat(),
        "scale": "0-100; target is >=95",
        "method": (
            "Publication readability heuristic. It penalises small canvases, long/tall layouts, "
            "dense title/footer bands, edge-heavy text-like regions, and busy connected components. "
            "It is deliberately stricter than the generation guard and should be read alongside visual inspection."
        ),
        "backupDir": str(backup_dir.relative_to(ROOT)),
        "before": before,
        "after": after,
        "passed": all(item["score"] >= 95 for item in after),
    }
    path = REPORTS / "substack-simulation-plot-readability-score-latest.json"
    path.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(report, indent=2))
    if not report["passed"]:
        raise SystemExit("One or more polished plots scored below 95.")


def original_backup_dir() -> Path:
    backup_root = ROOT / ".tmp"
    candidates = sorted(path for path in backup_root.glob("sim-plot-backup-*") if path.is_dir())
    if not candidates:
        latest_polish = json.loads((REPORTS / "substack-simulation-plot-polish-latest.json").read_text(encoding="utf-8"))
        return ROOT / latest_polish["backupDir"]
    return candidates[0]


def score_image(path: Path) -> dict[str, object]:
    image = Image.open(path).convert("L")
    arr = np.array(image)
    height, width = arr.shape
    edge = edge_proxy(arr)
    dark = arr < 150
    text_like = dark & (edge > 12)
    text_density = float(text_like.mean())
    top_band = arr[: int(height * 0.18), :]
    bottom_band = arr[int(height * 0.82) :, :]
    top_text_density = float(((top_band < 150) & (edge[: top_band.shape[0], :] > 12)).mean())
    bottom_text_density = float(((bottom_band < 150) & (edge[int(height * 0.82) :, :] > 12)).mean())
    component_count = connected_component_count((arr < 170)[::4, ::4])

    canvas_penalty = max(0.0, (1900 - width) / 35) + max(0.0, (1180 - height) / 30)
    text_penalty = max(0.0, (text_density - 0.010) * 1350)
    band_penalty = max(0.0, (top_text_density - 0.016) * 600) + max(0.0, (bottom_text_density - 0.012) * 520)
    component_penalty = max(0.0, (component_count - 420) / 35)
    aspect = width / height
    aspect_penalty = 0.0 if 1.45 <= aspect <= 1.95 else 3.0
    score = 100 - canvas_penalty - text_penalty - band_penalty - component_penalty - aspect_penalty
    return {
        "filename": path.name,
        "width": width,
        "height": height,
        "score": round(max(0.0, min(100.0, score)), 1),
        "penalties": {
            "canvas": round(canvas_penalty, 1),
            "textDensity": round(text_penalty, 1),
            "titleFooterBands": round(band_penalty, 1),
            "busyComponents": round(component_penalty, 1),
            "aspect": round(aspect_penalty, 1),
        },
    }


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


if __name__ == "__main__":
    main()

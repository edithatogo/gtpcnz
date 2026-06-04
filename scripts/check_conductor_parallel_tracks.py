from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MATRIX = ROOT / "conductor" / "parallel-execution-matrix.json"

REQUIRED_TRACK_FIELDS = {
    "wave",
    "depends_on",
    "blocks",
    "can_run_parallel_with",
    "allowed_files",
    "forbidden_files",
    "gates",
}
REQUIRED_FILES = {
    "metadata.json",
    "spec.md",
    "plan.md",
    "contracts.md",
    "acceptance.md",
    "implementation-log.md",
    "work-packages.md",
    "agent-prompts.md",
}


def _prefix(glob: str) -> str:
    return glob.replace("**", "").rstrip("*").rstrip("/")


def _overlap(left: str, right: str) -> bool:
    lp = _prefix(left)
    rp = _prefix(right)
    return bool(lp and rp and (lp.startswith(rp) or rp.startswith(lp)))


def main() -> int:
    issues: list[str] = []
    if not MATRIX.exists():
        issues.append("missing conductor/parallel-execution-matrix.json")
    else:
        matrix = json.loads(MATRIX.read_text(encoding="utf-8"))
        tracks = matrix.get("tracks", {})
        for track_id, cfg in tracks.items():
            missing_fields = sorted(REQUIRED_TRACK_FIELDS - set(cfg))
            if missing_fields:
                issues.append(f"{track_id} missing matrix fields {missing_fields}")
            track_dir = ROOT / "conductor" / "tracks" / track_id
            if not track_dir.exists():
                issues.append(f"{track_id} missing track directory")
                continue
            missing_files = sorted(name for name in REQUIRED_FILES if not (track_dir / name).exists())
            if missing_files:
                issues.append(f"{track_id} missing files {missing_files}")
            metadata = json.loads((track_dir / "metadata.json").read_text(encoding="utf-8"))
            if metadata.get("execution_wave") != cfg.get("wave"):
                issues.append(f"{track_id} metadata execution_wave differs from matrix")
            for dep in cfg.get("depends_on", []):
                if dep not in tracks:
                    issues.append(f"{track_id} depends on unknown track {dep}")
            for peer in cfg.get("can_run_parallel_with", []):
                if peer not in tracks:
                    issues.append(f"{track_id} can run with unknown track {peer}")
                    continue
                if track_id not in tracks[peer].get("can_run_parallel_with", []):
                    issues.append(f"{track_id} parallel relationship with {peer} is not symmetric")
                for left in cfg.get("allowed_files", []):
                    for right in tracks[peer].get("allowed_files", []):
                        if _overlap(left, right):
                            issues.append(f"{track_id} and {peer} have overlapping allowed files: {left} <> {right}")
            if not cfg.get("allowed_files"):
                issues.append(f"{track_id} has no allowed file ownership")
            if not cfg.get("gates"):
                issues.append(f"{track_id} has no gates")
            for doc in ["plan.md", "contracts.md", "acceptance.md", "work-packages.md", "agent-prompts.md"]:
                text = (track_dir / doc).read_text(encoding="utf-8")
                if "precise fiscal savings" not in text and doc in {"contracts.md", "agent-prompts.md"}:
                    issues.append(f"{track_id}/{doc} lacks claim-boundary forbidden moves")
    if issues:
        print("\n".join(issues))
        return 1
    print("conductor parallel track contracts passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

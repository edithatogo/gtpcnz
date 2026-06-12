"""Score Substack-ready posts against series, Substack, and image contracts."""
from __future__ import annotations

import argparse
import json
import re
from dataclasses import dataclass
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCHEDULE = ROOT / "launch-schedule-v1.7.2.json"
CURRENT_POST_DIR = "docs/substack-ready/posts-v1.8.1-applied/"
MODEL_TERMS = ("public_aggregate_validated", "empirically_supported_if_gated")
MIN_WORDS = 850
MAX_WORDS = 1_400


@dataclass(frozen=True)
class Score:
    series: int
    substack: int
    images: int
    live: int
    failures: tuple[str, ...]
    warnings: tuple[str, ...] = ()


@dataclass(frozen=True)
class LiveDraft:
    text: str
    image_count: int
    title: str


def local_post_path(post_path: str) -> Path:
    prefix = "rareinsights/primary-care-funding-architecture-v1.7.2/"
    return ROOT / post_path.removeprefix(prefix)


def words(markdown: str) -> list[str]:
    return re.findall(r"\b[\w'-]+\b", markdown)


def title_from_markdown(markdown: str) -> str:
    for line in markdown.splitlines():
        if line.startswith("# "):
            return line[2:].strip()
    return ""


def image_paths(markdown_path: Path, markdown: str) -> list[Path]:
    paths: list[Path] = []
    for match in re.finditer(r"!\[([^\]]*)\]\(([^)]+)\)", markdown):
        target = match.group(2).strip()
        if target.startswith(("http://", "https://")):
            continue
        paths.append((markdown_path.parent / target).resolve())
    return paths


def walk_doc_text(node: object) -> str:
    if isinstance(node, dict):
        parts = []
        text = node.get("text")
        if isinstance(text, str):
            parts.append(text)
        for child in node.get("content", []) or []:
            parts.append(walk_doc_text(child))
        return " ".join(part for part in parts if part)
    if isinstance(node, list):
        return " ".join(walk_doc_text(item) for item in node)
    return ""


def count_images(node: object) -> int:
    if isinstance(node, dict):
        count = 1 if node.get("type") in {"image2", "captionedImage"} else 0
        return count + sum(count_images(child) for child in node.get("content", []) or [])
    if isinstance(node, list):
        return sum(count_images(item) for item in node)
    return 0


def read_live_draft(cache_dir: Path, draft_id: object) -> LiveDraft | None:
    if not draft_id:
        return None
    path = cache_dir / f"draft-{draft_id}.json"
    if not path.exists():
        return None
    data = json.loads(path.read_text(encoding="utf-8"))
    body_raw = data.get("draft_body") or data.get("body")
    if not body_raw:
        return None
    body = json.loads(body_raw) if isinstance(body_raw, str) else body_raw
    return LiveDraft(
        text=walk_doc_text(body),
        image_count=count_images(body),
        title=str(data.get("draft_title") or data.get("title") or ""),
    )


def first_public_paragraph(markdown: str) -> str:
    for block in markdown.split("\n\n"):
        text_block = block.strip()
        if not text_block or text_block.startswith(("#", "!", "---")):
            continue
        if re.sub(r"[*_`]", "", text_block).lower().startswith("subtitle:"):
            continue
        return re.sub(r"\s+", " ", text_block)
    return ""


def score_row(row: dict[str, object], live_draft: LiveDraft | None = None) -> Score:
    failures: list[str] = []
    warnings: list[str] = []
    post_number = str(row.get("postNumber", "")).zfill(2)
    post_path = str(row.get("postPath", ""))
    title = str(row.get("title", "")).strip()
    subtitle = str(row.get("subtitle", "")).strip()
    hero_image = str(row.get("heroImage", "")).strip()
    scheduled_at = str(row.get("scheduledAt", "")).strip()
    markdown_path = local_post_path(post_path)
    markdown = markdown_path.read_text(encoding="utf-8")
    markdown_words = words(markdown)
    markdown_title = title_from_markdown(markdown)
    markdown_lower = markdown.lower()
    found_images = image_paths(markdown_path, markdown)

    series = 0
    if CURRENT_POST_DIR in post_path and "appendices-" not in post_path and markdown_path.exists():
        series += 10
    else:
        failures.append(f"post {post_number}: schedule must point at current main-post markdown")
    if markdown_title == title:
        series += 10
    else:
        failures.append(f"post {post_number}: markdown title does not match schedule title")
    if "appendix for this post" in markdown_lower and "deep dive appendix for post" not in markdown_lower[:400]:
        series += 10
    else:
        failures.append(f"post {post_number}: main post must link to appendix without becoming appendix text")
    if all(term in markdown for term in MODEL_TERMS) and "Claim boundary:" in markdown:
        series += 10
    else:
        failures.append(f"post {post_number}: missing v1.8.1 model terms or claim boundary")
    if "## What would change my mind?" in markdown and "## Useful links" in markdown:
        series += 10
    else:
        failures.append(f"post {post_number}: missing public falsifiability or useful-links section")

    substack = 0
    if 35 <= len(title) <= 95 and 45 <= len(subtitle) <= 150:
        substack += 10
    else:
        failures.append(f"post {post_number}: title/subtitle length is outside Substack range")
    if MIN_WORDS <= len(markdown_words) <= MAX_WORDS:
        substack += 10
    else:
        failures.append(f"post {post_number}: word count {len(markdown_words)} outside {MIN_WORDS}-{MAX_WORDS}")
    first_heading_at = markdown.find("\n## ")
    opening = markdown[: first_heading_at if first_heading_at != -1 else 700]
    opening_paragraphs = [p for p in opening.split("\n\n") if p.strip() and not p.startswith("#")]
    if len(opening_paragraphs) >= 4 and "deep dive" not in opening.lower():
        substack += 10
    else:
        failures.append(f"post {post_number}: opening needs a public hook before technical framing")
    if "\n## " in markdown and "\n### " not in markdown:
        substack += 10
    else:
        failures.append(f"post {post_number}: heading rhythm should use public-facing H2 sections only")
    if scheduled_at and "Australia/Sydney" in scheduled_at and str(row.get("publicationStatus", "")) == "ready":
        substack += 10
    else:
        failures.append(f"post {post_number}: schedule row must be ready and timezone-specific")

    images = 0
    if hero_image and local_post_path(hero_image).exists():
        images += 3
    else:
        failures.append(f"post {post_number}: missing schedule hero image")
    if found_images and all(path.exists() for path in found_images):
        images += 3
    else:
        failures.append(f"post {post_number}: missing in-post image file")
    if re.search(r"!\[[A-Z][^\]]{35,}\]\(", markdown):
        images += 2
    else:
        failures.append(f"post {post_number}: image alt text should be descriptive")
    if any("v1.7.2" in path.name or "pcf-v172" in path.name for path in [*found_images, local_post_path(hero_image)]):
        images += 2
    else:
        failures.append(f"post {post_number}: image package should use the current visual set")

    live = 0
    if live_draft is None:
        warnings.append(f"post {post_number}: live draft cache unavailable; online freshness not verified")
    else:
        live_text = live_draft.text
        compact_live = re.sub(r"\s+", " ", live_text)
        opening = first_public_paragraph(markdown)
        live += 5
        if title in live_draft.title or title in compact_live[:500]:
            live += 5
        else:
            failures.append(f"post {post_number}: live draft title/body does not match schedule title")
        if all(term in live_text for term in MODEL_TERMS):
            live += 8
        else:
            failures.append(f"post {post_number}: live draft missing exact v1.8.1 model terms")
        if "technical appendix" not in live_text[:800].lower():
            live += 5
        else:
            failures.append(f"post {post_number}: live draft still contains appendix-style lead text")
        if opening and opening[:80] in compact_live:
            live += 5
        else:
            failures.append(f"post {post_number}: live draft does not contain the current local opening")
        if not found_images or live_draft.image_count > 0:
            live += 2
        else:
            warnings.append(f"post {post_number}: live draft has no cached in-body image nodes")

    return Score(series=series, substack=substack, images=images, live=live, failures=tuple(failures), warnings=tuple(warnings))


def load_rows(post_numbers: set[str]) -> list[dict[str, object]]:
    rows = json.loads(SCHEDULE.read_text(encoding="utf-8"))
    selected = []
    for row in rows:
        post_number = str(row.get("postNumber", "")).zfill(2)
        if post_number in post_numbers:
            selected.append(row)
    return selected


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--post", action="append", help="Post number to score, e.g. 07")
    parser.add_argument("--scheduled-live", action="store_true", help="Score posts that are currently scheduled online")
    parser.add_argument("--live-map", default="../../catalogue/primary-care-v172-live-draft-map.json")
    parser.add_argument("--scheduled-snapshot", default="../../catalogue/rareinsights-substack-scheduled.json")
    parser.add_argument("--live-cache-dir", default="../../.tmp")
    parser.add_argument("--json-out")
    parser.add_argument("--markdown-out")
    parser.add_argument("--min-series", type=int, default=45)
    parser.add_argument("--min-substack", type=int, default=45)
    parser.add_argument("--min-images", type=int, default=9)
    parser.add_argument("--min-health-quality", type=int, default=95)
    args = parser.parse_args()

    live_map_by_sequence: dict[int, int] = {}
    selected_draft_by_post: dict[str, int] = {}
    if args.scheduled_live:
        live_map = json.loads((ROOT / args.live_map).resolve().read_text(encoding="utf-8"))
        scheduled = json.loads((ROOT / args.scheduled_snapshot).resolve().read_text(encoding="utf-8"))
        scheduled_ids = {int(item["id"]) for item in scheduled}
        live_map_by_sequence = {int(item["sequence"]): int(item["draftId"]) for item in live_map}
        schedule_rows = json.loads(SCHEDULE.read_text(encoding="utf-8"))
        post_numbers = set()
        for row in schedule_rows:
            draft_id = live_map_by_sequence.get(int(row.get("sequence", 0)))
            if draft_id in scheduled_ids:
                post_number = str(row.get("postNumber", "")).zfill(2)
                post_numbers.add(post_number)
                selected_draft_by_post[post_number] = draft_id
    else:
        if not args.post:
            parser.error("Pass --post or --scheduled-live")
        post_numbers = {str(post).zfill(2) for post in args.post}

    rows = load_rows(post_numbers)
    missing = post_numbers - {str(row.get("postNumber", "")).zfill(2) for row in rows}
    failures = [f"post {post}: not found in schedule" for post in sorted(missing)]
    results: dict[str, dict[str, object]] = {}
    total_health = 0

    for row in rows:
        post_number = str(row.get("postNumber", "")).zfill(2)
        live_draft = read_live_draft((ROOT / args.live_cache_dir).resolve(), selected_draft_by_post.get(post_number))
        score = score_row(row, live_draft=live_draft)
        local_total = score.series + score.substack + score.images
        local_quality = round((local_total / 110) * 70)
        health_quality = min(100, local_quality + score.live)
        total_health += health_quality
        results[post_number] = {
            "series": score.series,
            "substack": score.substack,
            "images": score.images,
            "live": score.live,
            "health.quality": health_quality,
            "warnings": list(score.warnings),
        }
        failures.extend(score.failures)
        if score.series < args.min_series:
            failures.append(f"post {post_number}: series score {score.series}/50 below {args.min_series}/50")
        if score.substack < args.min_substack:
            failures.append(f"post {post_number}: Substack score {score.substack}/50 below {args.min_substack}/50")
        if score.images < args.min_images:
            failures.append(f"post {post_number}: image score {score.images}/10 below {args.min_images}/10")
        if health_quality < args.min_health_quality:
            failures.append(f"post {post_number}: health.quality {health_quality}/100 below {args.min_health_quality}/100")

    average = round(total_health / len(rows), 1) if rows else 0
    payload = {"average_health.quality": average, "posts": results}
    print(json.dumps(payload, indent=2))
    if args.json_out:
        Path(args.json_out).write_text(f"{json.dumps(payload, indent=2)}\n", encoding="utf-8")
    if args.markdown_out:
        lines = [
            "# Primary care scheduled-post health.quality report",
            "",
            f"Average health.quality: {average} / 100",
            "",
            "| Post | health.quality | Series | Substack | Images | Live | Warnings |",
            "|---|---:|---:|---:|---:|---:|---|",
        ]
        for post_number, result in sorted(results.items()):
            warnings_text = "; ".join(result["warnings"]) if result["warnings"] else ""
            lines.append(
                f"| {post_number} | {result['health.quality']} | {result['series']} | "
                f"{result['substack']} | {result['images']} | {result['live']} | {warnings_text} |"
            )
        lines.append("")
        if failures:
            lines.append("## Blocking failures")
            lines.extend(f"- {failure}" for failure in failures)
        else:
            lines.append("No blocking failures.")
        Path(args.markdown_out).write_text("\n".join(lines) + "\n", encoding="utf-8")
    if failures:
        print("Publication readiness failed:")
        for failure in failures:
            print(f"- {failure}")
        return 1
    print("Publication readiness passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

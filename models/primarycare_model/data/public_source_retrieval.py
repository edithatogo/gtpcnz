"""Validate public-source retrieval plans without mutating model claims."""

from __future__ import annotations

from pathlib import Path
from typing import Any

import yaml
from pydantic import TypeAdapter

from models.primarycare_model.contracts.public_sources import PublicSourceRetrievalPlan
from models.primarycare_model.data.public_source_snapshot import PUBLIC_REGISTRY, ROOT, load_public_sources

RETRIEVAL_PLAN_PATH = PUBLIC_REGISTRY / "source_retrieval.public.v1.yaml"


def _lists_to_tuples(obj: Any) -> Any:
    if isinstance(obj, list):
        return tuple(_lists_to_tuples(item) for item in obj)
    if isinstance(obj, dict):
        return {key: _lists_to_tuples(value) for key, value in obj.items()}
    return obj


def load_public_source_retrieval_plans() -> tuple[PublicSourceRetrievalPlan, ...]:
    payload = yaml.safe_load(RETRIEVAL_PLAN_PATH.read_text(encoding="utf-8"))
    return TypeAdapter(tuple[PublicSourceRetrievalPlan, ...]).validate_python(
        _lists_to_tuples(payload["retrieval_plans"])
    )


def _is_repo_relative(path: str) -> bool:
    candidate = Path(path)
    return not candidate.is_absolute() and ".." not in candidate.parts


def verify_public_source_retrieval_plan() -> tuple[str, ...]:
    sources = {source.source_id: source for source in load_public_sources()}
    plans = {plan.source_id: plan for plan in load_public_source_retrieval_plans()}
    issues: list[str] = []

    missing = sorted(set(sources) - set(plans))
    extra = sorted(set(plans) - set(sources))
    issues.extend(f"{source_id}: missing retrieval plan" for source_id in missing)
    issues.extend(f"{source_id}: retrieval plan has no matching public source" for source_id in extra)

    for source_id, plan in sorted(plans.items()):
        source = sources.get(source_id)
        if source is None:
            continue
        if plan.landing_page_url != source.url_or_reference and plan.download_url != source.url_or_reference:
            issues.append(f"{source_id}: retrieval plan URL does not match public source registry URL")
        if plan.public_access_status != source.public_access_status:
            issues.append(f"{source_id}: retrieval plan public_access_status differs from source registry")
        if plan.licence_basis != source.licence_status:
            issues.append(f"{source_id}: retrieval plan licence_basis differs from source registry")
        if plan.expected_raw_dir != f"data/public_raw/{source_id}":
            issues.append(f"{source_id}: expected_raw_dir must be data/public_raw/{source_id}")
        if not plan.expected_processed_artifact.startswith(f"data/public_processed/{source_id}/"):
            issues.append(f"{source_id}: expected_processed_artifact must be under data/public_processed/{source_id}/")
        for field_name in ("expected_raw_dir", "expected_processed_artifact", "fetch_script", "transform_script"):
            value = getattr(plan, field_name)
            if not _is_repo_relative(value):
                issues.append(f"{source_id}: {field_name} must be a repository-relative path")
        if not plan.fetch_script.startswith("scripts/fetch_"):
            issues.append(f"{source_id}: fetch_script must be an explicit source fetch script")
        if not plan.transform_script.startswith("scripts/transform_"):
            issues.append(f"{source_id}: transform_script must be an explicit source transform script")
        raw_path = ROOT / plan.expected_raw_dir
        processed_path = ROOT / plan.expected_processed_artifact
        if plan.retrieval_status in {"downloaded_pending_transform", "processed_ready"} and not raw_path.exists():
            issues.append(f"{source_id}: retrieval status is advanced but raw directory is missing")
        if plan.retrieval_status == "processed_ready" and not processed_path.exists():
            issues.append(f"{source_id}: retrieval status is processed_ready but processed artifact is missing")
        if "patient-level" in plan.claim_boundary.lower() and "no patient-level" not in plan.claim_boundary.lower():
            issues.append(f"{source_id}: claim boundary may permit restricted person-level inputs")
    return tuple(issues)

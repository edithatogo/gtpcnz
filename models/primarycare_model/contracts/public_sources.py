"""Contracts for public source provenance and reproducible snapshots."""

from __future__ import annotations

from typing import Literal

from pydantic import Field

from models.primarycare_model.contracts.parameters import StrictContract

PublicAccessStatus = Literal["public", "published", "open"]
LicenceStatus = Literal["open", "public_reference", "open_or_public_reference"]
RetrievalStatus = Literal["reference_pinned_pending_download", "downloaded_pending_transform", "processed_ready"]


class PublicSource(StrictContract):
    source_id: str = Field(min_length=1)
    label: str = Field(min_length=1)
    url_or_reference: str = Field(min_length=1)
    retrieval_date: str = Field(pattern=r"^\d{4}-\d{2}-\d{2}$")
    licence_status: LicenceStatus
    public_access_status: PublicAccessStatus
    checksum: str = Field(min_length=1)
    transform_description: str = Field(min_length=1)
    claim_boundary: str = Field(min_length=1)


class PublicSourceSnapshot(StrictContract):
    snapshot_id: str = Field(min_length=1)
    created_at: str = Field(min_length=1)
    sources: tuple[PublicSource, ...]
    source_registry_sha256: str = Field(min_length=64, max_length=64)
    parameter_registry_sha256: str = Field(min_length=64, max_length=64)
    claim_boundary: str = Field(min_length=1)


class PublicSourceRetrievalPlan(StrictContract):
    source_id: str = Field(min_length=1)
    landing_page_url: str = Field(min_length=1)
    download_url: str | None = None
    expected_raw_dir: str = Field(min_length=1)
    expected_raw_artifact: str = Field(min_length=1)
    retrieval_method: str = Field(min_length=1)
    fetch_script: str = Field(min_length=1)
    retrieval_status: RetrievalStatus
    licence_basis: LicenceStatus
    public_access_status: PublicAccessStatus
    transform_script: str = Field(min_length=1)
    expected_processed_artifact: str = Field(min_length=1)
    claim_boundary: str = Field(min_length=1)

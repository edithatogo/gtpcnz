"""Input dataset contracts and privacy classification."""

from __future__ import annotations

from typing import Literal

from pydantic import Field

from models.primarycare_model.contracts.parameters import StrictContract

InputSensitivity = Literal["public", "public_aggregate", "template", "sensitive", "confidential"]


class InputField(StrictContract):
    field_name: str = Field(min_length=1)
    data_type: str = Field(min_length=1)
    unit: str = Field(min_length=1)
    required: bool = True
    description: str = Field(min_length=1)


class InputDataset(StrictContract):
    dataset_id: str = Field(min_length=1)
    label: str = Field(min_length=1)
    source: str = Field(min_length=1)
    sensitivity_class: InputSensitivity
    fields: tuple[InputField, ...]
    claim_boundary: str = Field(min_length=1)


# ── Provenance and data lineage ─────────────────────────────────────────

ProvenanceStatus = Literal["confirmed", "estimated", "placeholder", "gap"]


class ProvenanceEntry(StrictContract):
    """Typed provenance record for one public input source or transform.

    Tracks where the data came from, when it was retrieved, what transforms
    were applied, and what level of confidence can be claimed. This is the
    contract-side counterpart of a row in the ``provenance.v1.yaml`` registry.
    """

    source_id: str = Field(min_length=1, description="Unique identifier for this provenance entry")
    label: str = Field(min_length=1, description="Human-readable name of the input or source")
    source_url_or_reference: str = Field(
        min_length=1,
        description="URL, DOI, or stable reference for the original source",
    )
    retrieval_date: str = Field(
        min_length=1,
        pattern=r"^\d{4}-\d{2}-\d{2}$",
        description="Date the data was retrieved (YYYY-MM-DD format)",
    )
    transform_description: str = Field(
        min_length=1,
        description="Description of cleaning, aggregation or derivation steps applied",
    )
    status: ProvenanceStatus = Field(
        description=(
            "Confidence level of this provenance entry: "
            "``confirmed`` (directly extracted from the authoritative source), "
            "``estimated`` (imputed or modelled from related data), "
            "``placeholder`` (temporary value pending a real source), "
            "``gap`` (known shortfall — no data available yet)"
        ),
    )
    claim_boundary: str = Field(
        min_length=1,
        description=(
            "What can and cannot be legitimately claimed from this data source, "
            "including any known limitations or caveats"
        ),
    )

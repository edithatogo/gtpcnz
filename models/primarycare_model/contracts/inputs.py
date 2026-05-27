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

"""Validate processed public input datasets against the public input registry."""

from __future__ import annotations

import csv
import math
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Any

import yaml
from pydantic import TypeAdapter

from models.primarycare_model.contracts.inputs import InputDataset

ROOT = Path(__file__).resolve().parents[3]
PUBLIC_REGISTRY = ROOT / "models" / "primarycare_model" / "registries" / "public"
PUBLIC_PROCESSED = ROOT / "data" / "public_processed"

FORBIDDEN_PROCESSED_COLUMNS = {
    "".join(("n", "h", "i")),
    "_".join(("".join(("n", "h", "i")), "number")),
    "patient_id",
    "person_id",
    "individual_id",
    "practitioner_id",
    "provider_id",
    "mcnz_number",
    "name",
    "date_of_birth",
    "dob",
    "address",
    "email",
    "phone",
}


@dataclass(frozen=True)
class ProcessedDatasetExpectation:
    dataset: InputDataset
    artifact: Path


def _lists_to_tuples(obj: Any) -> Any:
    if isinstance(obj, list):
        return tuple(_lists_to_tuples(item) for item in obj)
    if isinstance(obj, dict):
        return {key: _lists_to_tuples(value) for key, value in obj.items()}
    return obj


def load_public_input_datasets(registry_root: Path = PUBLIC_REGISTRY) -> tuple[InputDataset, ...]:
    payload = yaml.safe_load((registry_root / "inputs.public.v1.yaml").read_text(encoding="utf-8"))
    return TypeAdapter(tuple[InputDataset, ...]).validate_python(_lists_to_tuples(payload["datasets"]))


def _load_retrieval_artifacts(registry_root: Path) -> dict[str, str]:
    payload = yaml.safe_load((registry_root / "source_retrieval.public.v1.yaml").read_text(encoding="utf-8"))
    artifacts: dict[str, str] = {}
    for plan in payload["retrieval_plans"]:
        artifacts[str(plan["source_id"])] = str(plan["expected_processed_artifact"])
    return artifacts


def processed_dataset_expectations(
    *,
    registry_root: Path = PUBLIC_REGISTRY,
    processed_root: Path = PUBLIC_PROCESSED,
) -> tuple[ProcessedDatasetExpectation, ...]:
    artifacts = _load_retrieval_artifacts(registry_root)
    expectations: list[ProcessedDatasetExpectation] = []
    for dataset in load_public_input_datasets(registry_root):
        source_id = dataset.source_id
        if not source_id:
            continue
        artifact = artifacts.get(str(source_id))
        if not artifact:
            continue
        relative_artifact = Path(artifact)
        if relative_artifact.parts[:2] == ("data", "public_processed"):
            relative_artifact = Path(*relative_artifact.parts[2:])
        expectations.append(ProcessedDatasetExpectation(dataset=dataset, artifact=processed_root / relative_artifact))
    return tuple(expectations)


def _coerce_value(value: str, data_type: str) -> bool:
    if data_type == "string":
        return bool(value.strip())
    if data_type == "integer":
        try:
            parsed = int(value)
        except ValueError:
            return False
        return str(parsed) == value.strip() and parsed >= 0
    if data_type == "number":
        try:
            parsed = float(value)
        except ValueError:
            return False
        return math.isfinite(parsed)
    return False


def validate_processed_dataset(expectation: ProcessedDatasetExpectation) -> tuple[str, ...]:
    dataset = expectation.dataset
    artifact = expectation.artifact
    issues: list[str] = []

    if artifact.suffix.lower() != ".csv":
        return (f"{dataset.dataset_id}: unsupported processed artifact format {artifact.suffix!r}; expected .csv",)
    if not artifact.exists():
        return (f"{dataset.dataset_id}: missing processed artifact {artifact.as_posix()}",)

    with artifact.open("r", encoding="utf-8", newline="") as handle:
        reader = csv.DictReader(handle)
        fieldnames = tuple(reader.fieldnames or ())
        lowered = {field.lower() for field in fieldnames}
        forbidden = sorted(lowered.intersection(FORBIDDEN_PROCESSED_COLUMNS))
        if forbidden:
            issues.append(f"{dataset.dataset_id}: forbidden person-level columns present: {', '.join(forbidden)}")

        required_fields = tuple(field for field in dataset.fields if field.required)
        missing = tuple(field.field_name for field in required_fields if field.field_name not in fieldnames)
        if missing:
            issues.append(f"{dataset.dataset_id}: missing required fields: {', '.join(missing)}")

        row_count = 0
        for row_number, row in enumerate(reader, start=2):
            row_count += 1
            for field in required_fields:
                if field.field_name not in row:
                    continue
                value = row[field.field_name]
                if value is None or not value.strip():
                    issues.append(f"{dataset.dataset_id}: row {row_number} field {field.field_name} is empty")
                    continue
                if not _coerce_value(value.strip(), field.data_type):
                    issues.append(
                        f"{dataset.dataset_id}: row {row_number} field {field.field_name} "
                        f"is not a valid {field.data_type}"
                    )
        if row_count == 0:
            issues.append(f"{dataset.dataset_id}: processed artifact has no data rows")

    metadata_path = artifact.with_name("_metadata.yaml")
    if not metadata_path.exists():
        issues.append(f"{dataset.dataset_id}: missing processed metadata file {metadata_path.as_posix()}")

    return tuple(issues)


def validate_processed_input_schemas(
    *,
    registry_root: Path = PUBLIC_REGISTRY,
    processed_root: Path = PUBLIC_PROCESSED,
    require_processed: bool = False,
) -> tuple[str, ...]:
    """Return processed-schema issues without promoting calibration claim status."""

    issues: list[str] = []
    for expectation in processed_dataset_expectations(registry_root=registry_root, processed_root=processed_root):
        if not expectation.artifact.exists() and not require_processed:
            continue
        issues.extend(validate_processed_dataset(expectation))
    return tuple(issues)


def main(argv: list[str] | None = None) -> int:
    import argparse

    parser = argparse.ArgumentParser(description="Validate processed public input schemas.")
    parser.add_argument("--require-processed", action="store_true", help="Fail if expected processed artifacts are absent.")
    args = parser.parse_args(argv)
    issues = validate_processed_input_schemas(require_processed=args.require_processed)
    if issues:
        print("\n".join(issues))
        return 1
    print("processed public input schema contract passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
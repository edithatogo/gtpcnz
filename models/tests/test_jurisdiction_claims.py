from __future__ import annotations

import yaml


def test_australia_is_comparative_context_only() -> None:
    with open("models/primarycare_model/registries/public/jurisdictions.public.v1.yaml", encoding="utf-8") as handle:
        payload = yaml.safe_load(handle)
    au = next(item for item in payload["jurisdictions"] if item["jurisdiction"] == "AU")
    assert au["first_class_model"] is False
    assert "Comparative policy context only" in au["claim_boundary"]

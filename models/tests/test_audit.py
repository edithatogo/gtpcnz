from pathlib import Path

from primarycare_model.audit import load_claims, validate_claims


def test_claim_source_ledger_is_valid():
    path = Path(__file__).resolve().parents[2] / "docs" / "audit" / "claim-to-source-ledger-v0.5.0.csv"
    claims = load_claims(path)
    assert len(claims) >= 20
    assert validate_claims(claims) == []


def test_claim_ledger_distinguishes_facts_from_hypotheses():
    path = Path(__file__).resolve().parents[2] / "docs" / "audit" / "claim-to-source-ledger-v0.5.0.csv"
    claims = load_claims(path)
    facts = [claim for claim in claims if claim.is_empirical_fact]
    to_validate = [claim for claim in claims if claim.requires_validation]
    assert facts
    assert to_validate
    assert any(claim.claim_id == "C002" for claim in facts)
    assert any(claim.claim_id == "C016" for claim in to_validate)

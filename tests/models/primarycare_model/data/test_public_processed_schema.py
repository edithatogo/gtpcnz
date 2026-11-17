import pytest

from models.primarycare_model.data.public_processed_schema import _coerce_value


def test_coerce_value_date_invalid():
    with pytest.raises(ValueError, match="Invalid ISO date format: 2024/01/01"):
        _coerce_value("2024/01/01", "date")


def test_coerce_value_date_valid():
    assert _coerce_value("2024-01-01", "date") is True

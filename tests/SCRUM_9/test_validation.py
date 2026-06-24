"""Unit tests for SCRUM-9 validation rules."""

import pytest
from pydantic import ValidationError

from src.SCRUM_9.models.expense import ExpenseCreate


def test_expense_create_accepts_valid_payload() -> None:
    """A valid payload should pass with normalized category."""
    payload = ExpenseCreate.model_validate(
        {
            "amount": "12.50",
            "category": "  groceries  ",
            "date": "2026-06-23",
        }
    )

    assert str(payload.amount) == "12.50"
    assert payload.category == "groceries"
    assert payload.date == "2026-06-23"


@pytest.mark.parametrize(
    "payload,missing_field",
    [
        ({"category": "food", "date": "2026-06-23"}, "amount"),
        ({"amount": "1.00", "date": "2026-06-23"}, "category"),
        ({"amount": "1.00", "category": "food"}, "date"),
    ],
)
def test_expense_create_rejects_missing_required_fields(payload: dict, missing_field: str) -> None:
    """Required fields amount/category/date must be present."""
    with pytest.raises(ValidationError) as exc_info:
        ExpenseCreate.model_validate(payload)

    error_locations = [error["loc"] for error in exc_info.value.errors()]
    assert (missing_field,) in error_locations


@pytest.mark.parametrize("amount", ["0", "-1", "-0.0001"])
def test_expense_create_rejects_non_positive_amount(amount: str) -> None:
    """Amount must be strictly greater than zero."""
    with pytest.raises(ValidationError):
        ExpenseCreate.model_validate(
            {"amount": amount, "category": "food", "date": "2026-06-23"}
        )


@pytest.mark.parametrize("category", ["", "   ", "\t"])
def test_expense_create_rejects_empty_category(category: str) -> None:
    """Category must contain non-whitespace content."""
    with pytest.raises(ValidationError):
        ExpenseCreate.model_validate(
            {"amount": "5.00", "category": category, "date": "2026-06-23"}
        )


@pytest.mark.parametrize("date_value", ["23-06-2026", "2026/06/23", "2026-6-3", "2026-02-30"])
def test_expense_create_rejects_invalid_date_format(date_value: str) -> None:
    """Date must follow strict YYYY-MM-DD semantics."""
    with pytest.raises(ValidationError):
        ExpenseCreate.model_validate(
            {"amount": "5.00", "category": "food", "date": date_value}
        )

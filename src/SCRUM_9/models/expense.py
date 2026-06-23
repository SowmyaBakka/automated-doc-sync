"""Data models and validation contracts for SCRUM-9 expenses."""

from datetime import datetime
from decimal import Decimal

from pydantic import BaseModel, ConfigDict, field_validator


class ExpenseCreate(BaseModel):
    """Request payload model for creating an expense."""

    model_config = ConfigDict(extra="forbid")

    amount: Decimal
    category: str
    date: str

    @field_validator("amount")
    @classmethod
    def validate_amount(cls, value: Decimal) -> Decimal:
        """Require strictly positive monetary value."""
        if value <= 0:
            raise ValueError("amount must be greater than 0")
        return value

    @field_validator("category")
    @classmethod
    def validate_category(cls, value: str) -> str:
        """Require non-empty category and normalize whitespace."""
        cleaned = value.strip()
        if not cleaned:
            raise ValueError("category must not be empty")
        return cleaned

    @field_validator("date")
    @classmethod
    def validate_date_format(cls, value: str) -> str:
        """Require strict date format YYYY-MM-DD."""
        try:
            parsed = datetime.strptime(value, "%Y-%m-%d")
        except ValueError as exc:
            raise ValueError("date must be in YYYY-MM-DD format") from exc

        if parsed.strftime("%Y-%m-%d") != value:
            raise ValueError("date must be in YYYY-MM-DD format")
        return value


class ExpenseItem(BaseModel):
    """Response model for a stored expense."""

    id: int
    amount: Decimal
    category: str
    date: str

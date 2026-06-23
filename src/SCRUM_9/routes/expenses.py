"""Expense routes for SCRUM-9.

Endpoint implementations are added in later tasks. This scaffold provides
router wiring and dependency injection so the app starts cleanly.
"""

from typing import Any

from fastapi import APIRouter, HTTPException, status
from pydantic import ValidationError

from src.SCRUM_9.models.expense import ExpenseCreate
from src.SCRUM_9.store.json_store import JsonStore

router = APIRouter(prefix="/expenses", tags=["expenses"])

_store: JsonStore | None = None


def set_store(store: JsonStore) -> None:
    """Inject the JSON store instance during app startup."""
    global _store
    _store = store


def validate_create_payload(payload: dict[str, Any]) -> ExpenseCreate:
    """Validate create-expense payload and map failures to HTTP 400."""
    try:
        return ExpenseCreate.model_validate(payload)
    except ValidationError as exc:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=exc.errors(),
        ) from exc

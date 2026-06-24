"""Expense routes for SCRUM-9.

Endpoint implementations are added in later tasks. This scaffold provides
router wiring and dependency injection so the app starts cleanly.
"""

from typing import Any

from fastapi import APIRouter, Body, HTTPException, Query, status
from pydantic import ValidationError

from src.SCRUM_9.models.expense import CategorySummary, ExpenseCreate, ExpenseItem
from src.SCRUM_9.services.expense_service import ExpenseService
from src.SCRUM_9.store.json_store import JsonStore

router = APIRouter(prefix="/expenses", tags=["expenses"])

_store: JsonStore | None = None


def set_store(store: JsonStore) -> None:
    """Inject the JSON store instance during app startup."""
    global _store
    _store = store


def _get_service() -> ExpenseService:
    """Build a service instance for the configured store."""
    if _store is None:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Store not initialized",
        )
    return ExpenseService(_store)


def validate_create_payload(payload: dict[str, Any]) -> ExpenseCreate:
    """Validate create-expense payload and map failures to HTTP 400."""
    try:
        return ExpenseCreate.model_validate(payload)
    except ValidationError as exc:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=exc.errors(),
        ) from exc


@router.post("", response_model=ExpenseItem, status_code=status.HTTP_201_CREATED)
async def create_expense(raw_payload: Any = Body(...)) -> ExpenseItem:
    """Create and persist an expense."""
    if not isinstance(raw_payload, dict):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="request body must be a JSON object",
        )

    payload = validate_create_payload(raw_payload)
    service = _get_service()
    created = await service.add_expense(payload)
    return ExpenseItem.model_validate(created)


@router.get("", response_model=list[ExpenseItem], status_code=status.HTTP_200_OK)
async def list_expenses(category: str | None = Query(default=None)) -> list[ExpenseItem]:
    """List all expenses with optional category filtering."""
    service = _get_service()
    expenses = await service.list_expenses(category=category)
    return [ExpenseItem.model_validate(item) for item in expenses]


@router.get(
    "/summary/categories",
    response_model=CategorySummary,
    status_code=status.HTTP_200_OK,
)
async def get_category_summary() -> CategorySummary:
    """Return Decimal-safe aggregated totals by category."""
    service = _get_service()
    totals = await service.summarize_by_category()
    return CategorySummary(totals=totals)

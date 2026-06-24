"""Unit tests for SCRUM-9 expense service behavior."""

import asyncio
from decimal import Decimal

import pytest

from src.SCRUM_9.models.expense import ExpenseCreate
from src.SCRUM_9.services.expense_service import ExpenseService
from src.SCRUM_9.store.json_store import JsonStore


@pytest.mark.asyncio
async def test_summary_uses_decimal_safe_aggregation(tmp_path) -> None:
    """Decimal math must preserve precision for category totals."""
    store_file = tmp_path / "expenses.json"
    store = JsonStore(str(store_file))
    service = ExpenseService(store)

    await service.add_expense(
        ExpenseCreate.model_validate(
            {"amount": "0.10", "category": "food", "date": "2026-06-23"}
        )
    )
    await service.add_expense(
        ExpenseCreate.model_validate(
            {"amount": "0.20", "category": "food", "date": "2026-06-24"}
        )
    )
    await service.add_expense(
        ExpenseCreate.model_validate(
            {"amount": "1.25", "category": "travel", "date": "2026-06-24"}
        )
    )

    totals = await service.summarize_by_category()

    assert totals == {
        "food": Decimal("0.30"),
        "travel": Decimal("1.25"),
    }


@pytest.mark.asyncio
async def test_list_expenses_applies_exact_category_filter(tmp_path) -> None:
    """Category filter should return only matching records."""
    store_file = tmp_path / "expenses.json"
    store = JsonStore(str(store_file))
    service = ExpenseService(store)

    await service.add_expense(
        ExpenseCreate.model_validate(
            {"amount": "10.00", "category": "food", "date": "2026-06-23"}
        )
    )
    await service.add_expense(
        ExpenseCreate.model_validate(
            {"amount": "4.00", "category": "travel", "date": "2026-06-23"}
        )
    )

    food_only = await service.list_expenses(category=" food ")

    assert len(food_only) == 1
    assert food_only[0]["category"] == "food"


@pytest.mark.asyncio
async def test_concurrent_add_expense_calls_do_not_lose_items(tmp_path) -> None:
    """Concurrent adds should persist every created expense without overwrites."""
    store_file = tmp_path / "expenses.json"
    store = JsonStore(str(store_file))
    service = ExpenseService(store)

    async def add_expense(index: int) -> dict:
        return await service.add_expense(
            ExpenseCreate.model_validate(
                {
                    "amount": f"{index + 1}.00",
                    "category": "food",
                    "date": "2026-06-24",
                }
            )
        )

    created = await asyncio.gather(*(add_expense(index) for index in range(10)))
    stored = await service.list_expenses()

    assert len(created) == 10
    assert len(stored) == 10
    assert sorted(item["id"] for item in stored) == list(range(1, 11))

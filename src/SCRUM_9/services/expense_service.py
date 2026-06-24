"""Business logic for expense operations in SCRUM-9."""

from decimal import Decimal
from typing import Any

from src.SCRUM_9.models.expense import ExpenseCreate
from src.SCRUM_9.store.json_store import JsonStore


class ExpenseService:
    """Service implementing route-independent expense operations."""

    def __init__(self, store: JsonStore) -> None:
        self._store = store

    async def add_expense(self, payload: ExpenseCreate) -> dict[str, Any]:
        """Create and persist a new expense record."""
        def append_expense(items: list[dict[str, Any]]) -> dict[str, Any]:
            next_id = self._next_id(items)
            created = {
                "id": next_id,
                "amount": self._serialize_amount(payload.amount),
                "category": payload.category,
                "date": payload.date,
            }
            items.append(created)
            return created

        created = await self._store.mutate(append_expense)
        return self._to_response(created)

    async def list_expenses(self, category: str | None = None) -> list[dict[str, Any]]:
        """Return all expenses, optionally filtered by category."""
        items = await self._store.get_all()
        normalized_filter = category.strip() if category else None

        response_items: list[dict[str, Any]] = []
        for item in items:
            if normalized_filter and item.get("category") != normalized_filter:
                continue
            response_items.append(self._to_response(item))

        return response_items

    async def summarize_by_category(self) -> dict[str, Decimal]:
        """Aggregate Decimal-safe totals by category in deterministic key order."""
        items = await self._store.get_all()

        totals: dict[str, Decimal] = {}
        for item in items:
            category = str(item.get("category", ""))
            amount = self._deserialize_amount(item.get("amount", "0"))
            totals[category] = totals.get(category, Decimal("0")) + amount

        return {category: totals[category] for category in sorted(totals.keys())}

    @staticmethod
    def _next_id(items: list[dict[str, Any]]) -> int:
        """Generate the next monotonically increasing integer id."""
        if not items:
            return 1
        return max(int(item.get("id", 0)) for item in items) + 1

    @staticmethod
    def _serialize_amount(value: Decimal) -> str:
        """Persist amount as a non-exponent string for stable JSON output."""
        return format(value, "f")

    @staticmethod
    def _deserialize_amount(value: Any) -> Decimal:
        """Convert a stored amount into Decimal without float precision drift."""
        return Decimal(str(value))

    def _to_response(self, item: dict[str, Any]) -> dict[str, Any]:
        """Normalize a persisted record into response-safe field types."""
        return {
            "id": int(item["id"]),
            "amount": self._deserialize_amount(item["amount"]),
            "category": str(item["category"]),
            "date": str(item["date"]),
        }

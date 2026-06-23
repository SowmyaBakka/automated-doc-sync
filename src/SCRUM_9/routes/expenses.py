"""Expense routes for SCRUM-9.

Endpoint implementations are added in later tasks. This scaffold provides
router wiring and dependency injection so the app starts cleanly.
"""

from fastapi import APIRouter

from src.SCRUM_9.store.json_store import JsonStore

router = APIRouter(prefix="/expenses", tags=["expenses"])

_store: JsonStore | None = None


def set_store(store: JsonStore) -> None:
    """Inject the JSON store instance during app startup."""
    global _store
    _store = store

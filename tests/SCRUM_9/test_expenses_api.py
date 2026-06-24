"""Integration tests for SCRUM-9 expense API happy paths."""

import json


def test_post_expenses_returns_201_and_persists(expense_client) -> None:
    """POST /expenses should create a record and write it to storage."""
    response = expense_client.post(
        "/expenses",
        json={"amount": "12.50", "category": "groceries", "date": "2026-06-23"},
    )

    assert response.status_code == 201
    payload = response.json()
    assert payload == {
        "id": 1,
        "amount": "12.50",
        "category": "groceries",
        "date": "2026-06-23",
    }

    with open(expense_client.test_store.file_path, "r", encoding="utf-8") as handle:
        persisted = json.load(handle)

    assert persisted == [
        {
            "id": 1,
            "amount": "12.50",
            "category": "groceries",
            "date": "2026-06-23",
        }
    ]


def test_get_expenses_returns_all_created_records(expense_client) -> None:
    """GET /expenses should return all persisted expenses."""
    expense_client.post(
        "/expenses",
        json={"amount": "12.50", "category": "groceries", "date": "2026-06-23"},
    )
    expense_client.post(
        "/expenses",
        json={"amount": "8.25", "category": "travel", "date": "2026-06-24"},
    )

    response = expense_client.get("/expenses")

    assert response.status_code == 200
    assert response.json() == [
        {"id": 1, "amount": "12.50", "category": "groceries", "date": "2026-06-23"},
        {"id": 2, "amount": "8.25", "category": "travel", "date": "2026-06-24"},
    ]


def test_get_expenses_filters_by_category(expense_client) -> None:
    """GET /expenses?category=... should return only matching items."""
    expense_client.post(
        "/expenses",
        json={"amount": "12.50", "category": "groceries", "date": "2026-06-23"},
    )
    expense_client.post(
        "/expenses",
        json={"amount": "8.25", "category": "travel", "date": "2026-06-24"},
    )
    expense_client.post(
        "/expenses",
        json={"amount": "4.75", "category": "groceries", "date": "2026-06-25"},
    )

    response = expense_client.get("/expenses", params={"category": "groceries"})

    assert response.status_code == 200
    assert response.json() == [
        {"id": 1, "amount": "12.50", "category": "groceries", "date": "2026-06-23"},
        {"id": 3, "amount": "4.75", "category": "groceries", "date": "2026-06-25"},
    ]

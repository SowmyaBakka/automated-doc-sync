"""Tests for SCRUM-9 fixture isolation behavior."""


def test_client_factory_creates_isolated_storage_files(expense_client_factory) -> None:
    """Separate clients should not share persisted state across temp files."""
    client_one = expense_client_factory()
    client_two = expense_client_factory()

    response_one = client_one.post(
        "/expenses",
        json={"amount": "3.50", "category": "coffee", "date": "2026-06-24"},
    )
    response_two = client_two.get("/expenses")

    assert response_one.status_code == 201
    assert response_two.status_code == 200
    assert response_two.json() == []
    assert client_one.test_store.file_path != client_two.test_store.file_path


def test_repeated_client_fixture_usage_starts_from_empty_state(expense_client_factory) -> None:
    """A fresh client from the fixture factory should start with an empty store."""
    first_client = expense_client_factory()
    first_client.post(
        "/expenses",
        json={"amount": "7.00", "category": "books", "date": "2026-06-24"},
    )

    second_client = expense_client_factory()
    response = second_client.get("/expenses")

    assert response.status_code == 200
    assert response.json() == []

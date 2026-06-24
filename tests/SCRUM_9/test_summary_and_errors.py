"""Integration tests for SCRUM-9 summary and fault handling."""

from src.SCRUM_9.store.json_store import JsonStoreWriteError


def test_get_category_summary_returns_decimal_safe_totals(expense_client) -> None:
    """Summary endpoint should return aggregated totals by category."""
    expense_client.post(
        "/expenses",
        json={"amount": "0.10", "category": "food", "date": "2026-06-23"},
    )
    expense_client.post(
        "/expenses",
        json={"amount": "0.20", "category": "food", "date": "2026-06-24"},
    )
    expense_client.post(
        "/expenses",
        json={"amount": "1.25", "category": "travel", "date": "2026-06-24"},
    )

    response = expense_client.get("/expenses/summary/categories")

    assert response.status_code == 200
    assert response.json() == {"food": "0.30", "travel": "1.25"}


def test_post_expenses_invalid_payload_returns_400(expense_client) -> None:
    """Malformed payloads should map to the SCRUM-9 400 contract."""
    response = expense_client.post(
        "/expenses",
        json={"amount": "0", "category": "", "date": "06/24/2026"},
    )

    assert response.status_code == 400
    payload = response.json()
    assert "detail" in payload


def test_corrupted_json_returns_sanitized_500(expense_client_factory) -> None:
    """Unreadable JSON should surface as a sanitized server error."""
    client = expense_client_factory(initial_content="{not-json}")

    response = client.get("/expenses")

    assert response.status_code == 500
    assert response.json() == {"detail": "storage data is corrupted"}


def test_write_failure_returns_sanitized_500(expense_client, monkeypatch) -> None:
    """Write errors should map to the storage-operation failure contract."""

    def fail_write(payload):
        raise JsonStoreWriteError("boom")

    monkeypatch.setattr(expense_client.test_store, "_write_payload", fail_write)

    response = expense_client.post(
        "/expenses",
        json={"amount": "4.50", "category": "food", "date": "2026-06-24"},
    )

    assert response.status_code == 500
    assert response.json() == {"detail": "storage operation failed"}


def test_missing_storage_file_auto_initializes_and_persists(expense_client_factory) -> None:
    """Missing storage file should behave like first run and allow writes."""
    client = expense_client_factory(create_file=False)

    create_response = client.post(
        "/expenses",
        json={"amount": "9.99", "category": "books", "date": "2026-06-24"},
    )

    assert create_response.status_code == 201
    assert client.test_store.file_path.exists()

    list_response = client.get("/expenses")
    assert list_response.status_code == 200
    assert list_response.json() == [
        {"id": 1, "amount": "9.99", "category": "books", "date": "2026-06-24"}
    ]
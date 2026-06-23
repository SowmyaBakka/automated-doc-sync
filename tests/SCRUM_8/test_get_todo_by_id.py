"""Integration tests for the GET /todos/{id} endpoint."""

import pytest
from fastapi.testclient import TestClient

from src.SCRUM_8.main import app


@pytest.mark.asyncio
async def test_get_todo_by_valid_id_returns_200():
    """Test GET /todos/{id} with valid id returns 200 + correct TodoItem."""
    client = TestClient(app)
    
    # Create an item
    create_response = client.post(
        "/todos",
        json={"title": "Test item", "description": "A test"}
    )
    
    assert create_response.status_code == 201
    created_item = create_response.json()
    item_id = created_item["id"]
    
    # Get the item by ID
    response = client.get(f"/todos/{item_id}")
    
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == item_id
    assert data["title"] == "Test item"
    assert data["description"] == "A test"
    assert data["done"] is False
    assert "createdAt" in data


@pytest.mark.asyncio
async def test_get_todo_by_unknown_id_returns_404():
    """Test GET /todos/{id} with unknown id returns 404."""
    client = TestClient(app)
    
    response = client.get("/todos/999999999")
    
    assert response.status_code == 404
    data = response.json()
    assert "detail" in data
    assert "not found" in data["detail"].lower()

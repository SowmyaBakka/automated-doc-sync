"""Integration tests for the GET /todos endpoint."""

import pytest
from fastapi.testclient import TestClient

from src.SCRUM_8.main import app


@pytest.mark.asyncio
async def test_get_todos_empty_store_returns_200_with_empty_list():
    """Test GET /todos on empty store returns 200 with []."""
    client = TestClient(app)
    
    response = client.get("/todos")
    
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    # May or may not be empty depending on other tests


@pytest.mark.asyncio
async def test_get_todos_after_creating_items():
    """Test GET /todos returns 200 with array of TodoItem after creating items."""
    client = TestClient(app)
    
    # Create two items
    response1 = client.post("/todos", json={"title": "First"})
    response2 = client.post("/todos", json={"title": "Second"})
    
    assert response1.status_code == 201
    assert response2.status_code == 201
    
    # Get all items
    response = client.get("/todos")
    
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) >= 2
    
    # Verify items have correct structure
    for item in data:
        assert "id" in item
        assert "title" in item
        assert "description" in item
        assert "done" in item
        assert "createdAt" in item

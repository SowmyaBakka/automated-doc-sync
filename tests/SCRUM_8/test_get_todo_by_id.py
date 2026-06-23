"""Integration tests for the GET /todos/{id} endpoint."""

import pytest
from fastapi.testclient import TestClient
import tempfile
from pathlib import Path

from src.SCRUM_8.main import app, store


@pytest.fixture
def client():
    """Provide a TestClient for the FastAPI app with initialized store."""
    # Use a temporary file for testing
    with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
        temp_file = f.name
        f.write('[]')
    
    # Recreate store with temp file
    test_store = store.__class__(temp_file)
    
    # Setup: initialize
    import asyncio
    asyncio.run(test_store.load())
    
    # Inject into router
    from src.SCRUM_8.routes.todos import set_store
    set_store(test_store)
    
    client = TestClient(app)
    
    yield client
    
    # Cleanup
    Path(temp_file).unlink(missing_ok=True)


def test_get_todo_by_valid_id_returns_200(client):
    """Test GET /todos/{id} with valid id returns 200 + correct TodoItem."""
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


def test_get_todo_by_unknown_id_returns_404(client):
    """Test GET /todos/{id} with unknown id returns 404."""
    response = client.get("/todos/999999999")
    
    assert response.status_code == 404
    data = response.json()
    assert "detail" in data
    assert "not found" in data["detail"].lower()

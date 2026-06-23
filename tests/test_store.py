"""Unit tests for the JSON store."""

import asyncio
import json
import pytest
import tempfile
from pathlib import Path

from src.store.json_store import JsonStore


@pytest.fixture
def temp_file():
    """Fixture to provide a temporary JSON file for testing."""
    with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
        temp_path = f.name
    
    yield temp_path
    
    # Cleanup
    Path(temp_path).unlink(missing_ok=True)


@pytest.mark.asyncio
async def test_get_all_empty_store(temp_file):
    """Test get_all() on empty store returns []."""
    store = JsonStore(temp_file)
    await store.load()
    
    items = await store.get_all()
    
    assert items == []


@pytest.mark.asyncio
async def test_add_returns_item_with_correct_fields(temp_file):
    """Test add() returns item with correct fields."""
    store = JsonStore(temp_file)
    await store.load()
    
    todo_dict = {"title": "Test task", "description": "A test"}
    created_item = await store.add(todo_dict)
    
    assert "id" in created_item
    assert created_item["title"] == "Test task"
    assert created_item["description"] == "A test"
    assert created_item["done"] is False
    assert "createdAt" in created_item
    assert created_item["createdAt"].endswith("Z")  # ISO UTC format


@pytest.mark.asyncio
async def test_get_by_id_returns_item(temp_file):
    """Test get_by_id() returns item when found."""
    store = JsonStore(temp_file)
    await store.load()
    
    created_item = await store.add({"title": "Buy milk"})
    item_id = created_item["id"]
    
    retrieved_item = await store.get_by_id(item_id)
    
    assert retrieved_item is not None
    assert retrieved_item["id"] == item_id
    assert retrieved_item["title"] == "Buy milk"


@pytest.mark.asyncio
async def test_get_by_id_returns_none_for_unknown_id(temp_file):
    """Test get_by_id() returns None when item not found."""
    store = JsonStore(temp_file)
    await store.load()
    
    retrieved_item = await store.get_by_id(999999)
    
    assert retrieved_item is None


@pytest.mark.asyncio
async def test_concurrent_add_calls_do_not_lose_items(temp_file):
    """Test concurrent add() calls with lock guard do not lose items."""
    store = JsonStore(temp_file)
    await store.load()
    
    # Create multiple tasks that add items concurrently
    async def add_item(title):
        return await store.add({"title": title})
    
    tasks = [add_item(f"Task {i}") for i in range(10)]
    created_items = await asyncio.gather(*tasks)
    
    # Verify all items were created
    assert len(created_items) == 10
    
    # Verify all items are retrievable
    all_items = await store.get_all()
    assert len(all_items) == 10
    
    # Verify all titles are present
    titles = {item["title"] for item in all_items}
    expected_titles = {f"Task {i}" for i in range(10)}
    assert titles == expected_titles


@pytest.mark.asyncio
async def test_store_persists_to_disk(temp_file):
    """Test that items are written to disk on add()."""
    store = JsonStore(temp_file)
    await store.load()
    
    await store.add({"title": "First"})
    await store.add({"title": "Second"})
    
    # Read the file directly
    with open(temp_file, "r") as f:
        data = json.load(f)
    
    assert len(data) == 2
    assert data[0]["title"] == "First"
    assert data[1]["title"] == "Second"


@pytest.mark.asyncio
async def test_store_loads_from_disk(temp_file):
    """Test that store loads items from disk on initialization."""
    # First store: add items and persist
    store1 = JsonStore(temp_file)
    await store1.load()
    await store1.add({"title": "Persisted item"})
    
    # Second store: load from same file
    store2 = JsonStore(temp_file)
    await store2.load()
    
    items = await store2.get_all()
    
    assert len(items) == 1
    assert items[0]["title"] == "Persisted item"


@pytest.mark.asyncio
async def test_add_handles_id_collisions(temp_file):
    """Test add() increments ID on collision."""
    store = JsonStore(temp_file)
    await store.load()
    
    # Manually add an item with a fixed ID
    store._items.append({
        "id": 1000,
        "title": "Existing",
        "description": None,
        "done": False,
        "createdAt": "2026-06-23T10:00:00Z"
    })
    
    # Create new items - they should get non-colliding IDs
    item1 = await store.add({"title": "New item 1"})
    item2 = await store.add({"title": "New item 2"})
    
    # IDs should be different
    assert item1["id"] != item2["id"]
    
    # Both should be retrievable
    assert await store.get_by_id(item1["id"]) is not None
    assert await store.get_by_id(item2["id"]) is not None

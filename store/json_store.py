"""JSON file-based store for to-do items.

Provides thread-safe read and write operations using asyncio.Lock.
"""

import asyncio
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Optional


class JsonStore:
    """In-memory store backed by a JSON file on disk.
    
    Items are loaded into memory at startup and written back to disk
    after every mutation. An asyncio.Lock guards all read-modify-write
    operations to prevent concurrent-write data loss.
    """

    def __init__(self, file_path: str = "todos.json"):
        """Initialize the store.
        
        Args:
            file_path: Path to the JSON file to persist to-do items.
        """
        self._file_path = Path(file_path)
        self._items: list[dict] = []
        self._lock = asyncio.Lock()

    async def load(self) -> None:
        """Load to-do items from the JSON file into memory.
        
        Called at application startup. If the file doesn't exist or is empty,
        initializes with an empty list.
        """
        if self._file_path.exists():
            try:
                with open(self._file_path, "r") as f:
                    content = f.read().strip()
                    if content:
                        self._items = json.loads(content)
                    else:
                        self._items = []
            except (json.JSONDecodeError, IOError):
                self._items = []
        else:
            self._items = []

    async def get_all(self) -> list[dict]:
        """Retrieve all to-do items.
        
        Returns:
            List of to-do item dictionaries.
        """
        return list(self._items)

    async def get_by_id(self, item_id: int) -> Optional[dict]:
        """Retrieve a single to-do item by ID.
        
        Args:
            item_id: The ID of the to-do item to retrieve.
            
        Returns:
            The to-do item dictionary if found, None otherwise.
        """
        for item in self._items:
            if item.get("id") == item_id:
                return item
        return None

    async def add(self, todo: dict) -> dict:
        """Add a new to-do item to the store.
        
        Generates a timestamp-based ID (milliseconds since epoch),
        increments on collision, sets done=False, and createdAt as ISO UTC.
        Thread-safe via asyncio.Lock.
        
        Args:
            todo: Dictionary with 'title' and optional 'description'.
            
        Returns:
            The created to-do item with id, title, description, done, createdAt.
        """
        async with self._lock:
            # Generate timestamp-based ID (milliseconds since epoch)
            now_utc = datetime.now(timezone.utc)
            item_id = int(now_utc.timestamp() * 1000)

            # Increment ID until we find a unique one (collision handling)
            while any(item.get("id") == item_id for item in self._items):
                item_id += 1

            # Create the full to-do item
            created_item = {
                "id": item_id,
                "title": todo.get("title"),
                "description": todo.get("description"),
                "done": False,
                "createdAt": now_utc.isoformat().replace("+00:00", "Z"),
            }

            # Append to in-memory list
            self._items.append(created_item)

            # Flush to disk
            self._flush()

            return created_item

    def _flush(self) -> None:
        """Write the in-memory items to the JSON file on disk."""
        with open(self._file_path, "w") as f:
            json.dump(self._items, f, indent=2)

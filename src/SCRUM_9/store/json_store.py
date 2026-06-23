"""JSON file-backed storage adapter for SCRUM-9."""

import json
from pathlib import Path


class JsonStore:
    """Simple in-memory collection backed by a JSON file."""

    def __init__(self, file_path: str) -> None:
        self._file_path = Path(file_path)
        self._items: list[dict] = []

    @property
    def file_path(self) -> Path:
        """Expose resolved file path for diagnostics and tests."""
        return self._file_path

    async def load(self) -> None:
        """Load items from disk, defaulting to an empty list."""
        if not self._file_path.exists():
            self._items = []
            return

        content = self._file_path.read_text(encoding="utf-8").strip()
        if not content:
            self._items = []
            return

        data = json.loads(content)
        self._items = data if isinstance(data, list) else []

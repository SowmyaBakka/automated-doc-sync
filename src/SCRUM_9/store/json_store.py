"""JSON file-backed storage adapter for SCRUM-9."""

import json
from pathlib import Path
from typing import Any


class JsonStoreError(Exception):
    """Base exception for all JSON store errors."""


class JsonStoreCorruptedDataError(JsonStoreError):
    """Raised when persisted JSON content cannot be parsed."""


class JsonStoreReadError(JsonStoreError):
    """Raised when reading from disk fails unexpectedly."""


class JsonStoreWriteError(JsonStoreError):
    """Raised when writing to disk fails."""


class JsonStore:
    """Simple in-memory collection backed by a JSON file."""

    def __init__(self, file_path: str) -> None:
        self._file_path = Path(file_path)
        self._items: list[dict[str, Any]] = []
        self._loaded = False

    @property
    def file_path(self) -> Path:
        """Expose resolved file path for diagnostics and tests."""
        return self._file_path

    async def load(self) -> None:
        """Load items from disk with deterministic fault handling.

        Missing file is treated as first-run initialization and results in
        an empty in-memory collection.
        """
        if not self._file_path.exists():
            self._items = []
            self._loaded = True
            return

        try:
            content = self._file_path.read_text(encoding="utf-8").strip()
        except OSError as exc:
            raise JsonStoreReadError("failed to read JSON storage file") from exc

        if not content:
            self._items = []
            self._loaded = True
            return

        try:
            data = json.loads(content)
        except json.JSONDecodeError as exc:
            raise JsonStoreCorruptedDataError("JSON storage file is corrupted") from exc

        if not isinstance(data, list):
            raise JsonStoreCorruptedDataError("JSON storage root must be a list")

        self._items = data
        self._loaded = True

    async def _ensure_loaded(self) -> None:
        """Load persisted data lazily on first access."""
        if not self._loaded:
            await self.load()

    async def get_all(self) -> list[dict[str, Any]]:
        """Return a shallow copy of all currently loaded items."""
        await self._ensure_loaded()
        return [item.copy() for item in self._items]

    async def save_all(self, items: list[dict[str, Any]]) -> None:
        """Persist a full collection to disk and update in-memory state."""
        await self._ensure_loaded()
        payload = [item.copy() for item in items]
        self._write_payload(payload)
        self._items = payload
        self._loaded = True

    def _write_payload(self, payload: list[dict[str, Any]]) -> None:
        """Write payload to storage file and propagate write failures."""
        try:
            if self._file_path.parent and not self._file_path.parent.exists():
                self._file_path.parent.mkdir(parents=True, exist_ok=True)
            self._file_path.write_text(
                json.dumps(payload, indent=2),
                encoding="utf-8",
            )
        except OSError as exc:
            raise JsonStoreWriteError("failed to write JSON storage file") from exc

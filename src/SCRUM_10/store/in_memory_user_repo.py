"""In-memory user repository for SCRUM-10."""

from __future__ import annotations

from datetime import datetime, timezone

from src.SCRUM_10.models.user import User


class InMemoryUserRepository:
    """Repository storing users in process memory keyed by normalized email."""

    def __init__(self) -> None:
        self._users_by_email: dict[str, User] = {}
        self._next_id = 1

    @staticmethod
    def _normalize_email(email: str) -> str:
        """Normalize email key used for all lookups and writes."""
        return email.strip().lower()

    def create_user(self, *, username: str, email: str, password_hash: str) -> User:
        """Create and store a new user record."""
        normalized_email = self._normalize_email(email)
        user = User(
            id=f"u_{self._next_id:04d}",
            username=username,
            email=normalized_email,
            password_hash=password_hash,
            created_at=datetime.now(timezone.utc),
        )
        self._users_by_email[normalized_email] = user
        self._next_id += 1
        return user

    def get_by_email(self, email: str) -> User | None:
        """Return a user by normalized email or None when not found."""
        return self._users_by_email.get(self._normalize_email(email))

    def exists_by_email(self, email: str) -> bool:
        """Check whether a normalized email is already registered."""
        return self._normalize_email(email) in self._users_by_email

    def clear(self) -> None:
        """Reset repository state for test isolation."""
        self._users_by_email.clear()
        self._next_id = 1

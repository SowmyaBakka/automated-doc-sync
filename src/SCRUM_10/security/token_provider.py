"""Token provider abstractions for SCRUM-10."""

from __future__ import annotations

import time
from typing import Protocol

from src.SCRUM_10.models.user import User


class TokenProvider(Protocol):
    """Protocol for generating authentication tokens."""

    def generate(self, user: User) -> str:
        """Generate a token string for the supplied user."""


class MockTokenProvider:
    """Temporary token provider used by SCRUM-10 scope."""

    def generate(self, user: User) -> str:
        """Generate a deterministic-shape mock token with timestamp suffix."""
        return f"mock-token-{user.id}-{int(time.time())}"

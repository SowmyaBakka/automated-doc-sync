"""User entity for SCRUM-10 authentication."""

from dataclasses import dataclass
from datetime import datetime


@dataclass(slots=True)
class User:
    """In-memory representation of a registered user."""

    id: str
    username: str
    email: str
    password_hash: str
    created_at: datetime

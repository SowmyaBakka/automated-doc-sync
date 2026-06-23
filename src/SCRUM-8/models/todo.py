from datetime import datetime
from typing import Optional

from pydantic import BaseModel, field_validator


class TodoCreate(BaseModel):
    """Request body for creating a new to-do item.

    `done` is intentionally excluded — it is always False at creation.
    """

    title: str
    description: Optional[str] = None

    @field_validator("title")
    @classmethod
    def title_must_not_be_empty(cls, v: str) -> str:
        if not v or not v.strip():
            raise ValueError("title must not be empty")
        return v


class TodoItem(BaseModel):
    """Full to-do item returned in API responses."""

    id: int
    title: str
    description: Optional[str] = None
    done: bool = False
    createdAt: datetime

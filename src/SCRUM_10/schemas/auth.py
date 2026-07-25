"""Authentication request and response schemas for SCRUM-10."""

from __future__ import annotations

import re

from pydantic import BaseModel, Field, field_validator

EMAIL_PATTERN = re.compile(r"^[^@\s]+@[^@\s]+\.[^@\s]+$")


class RegisterRequest(BaseModel):
    """Request model for user registration."""

    username: str = Field(min_length=3, max_length=50)
    email: str
    password: str = Field(min_length=8)

    @field_validator("username", "email", "password", mode="before")
    @classmethod
    def validate_non_empty_string(cls, value: object) -> str:
        """Require all authentication fields to be non-empty strings."""
        if not isinstance(value, str):
            raise ValueError("must be a string")
        normalized = value.strip()
        if not normalized:
            raise ValueError("must not be empty")
        return normalized

    @field_validator("email")
    @classmethod
    def validate_email(cls, value: str) -> str:
        """Validate and normalize email format."""
        normalized = value.strip().lower()
        if not EMAIL_PATTERN.match(normalized):
            raise ValueError("must be a valid email")
        return normalized


class LoginRequest(BaseModel):
    """Request model for user login."""

    email: str
    password: str

    @field_validator("email", "password", mode="before")
    @classmethod
    def validate_non_empty_string(cls, value: object) -> str:
        """Require both login fields to be non-empty strings."""
        if not isinstance(value, str):
            raise ValueError("must be a string")
        normalized = value.strip()
        if not normalized:
            raise ValueError("must not be empty")
        return normalized

    @field_validator("email")
    @classmethod
    def validate_email(cls, value: str) -> str:
        """Validate and normalize email format."""
        normalized = value.strip().lower()
        if not EMAIL_PATTERN.match(normalized):
            raise ValueError("must be a valid email")
        return normalized


class RegisterResponse(BaseModel):
    """Response model for successful registration."""

    id: str
    username: str
    email: str
    message: str


class LoginResponse(BaseModel):
    """Response model for successful login."""

    token: str
    token_type: str = "Bearer"

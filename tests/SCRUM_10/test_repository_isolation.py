"""Isolation tests for SCRUM-10 in-memory repository behavior."""

from src.SCRUM_10.routes.auth import reset_auth_state


def test_reset_auth_state_allows_re_registering_same_email(auth_client):
    first = auth_client.post(
        "/register",
        json={
            "username": "alice",
            "email": "alice@example.com",
            "password": "StrongPass123",
        },
    )
    assert first.status_code == 201

    reset_auth_state()

    second = auth_client.post(
        "/register",
        json={
            "username": "alice",
            "email": "alice@example.com",
            "password": "StrongPass123",
        },
    )
    assert second.status_code == 201


def test_autouse_fixture_starts_each_test_with_clean_state(auth_client):
    response = auth_client.post(
        "/register",
        json={
            "username": "alice",
            "email": "alice@example.com",
            "password": "StrongPass123",
        },
    )
    assert response.status_code == 201

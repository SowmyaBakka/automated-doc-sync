"""API tests for SCRUM-10 login endpoint."""


def _register_default_user(auth_client) -> None:
    auth_client.post(
        "/register",
        json={
            "username": "alice",
            "email": "alice@example.com",
            "password": "StrongPass123",
        },
    )


def test_login_success_returns_token(auth_client):
    _register_default_user(auth_client)

    response = auth_client.post(
        "/login",
        json={
            "email": "alice@example.com",
            "password": "StrongPass123",
        },
    )

    assert response.status_code == 200
    payload = response.json()
    assert payload["token_type"] == "Bearer"
    assert payload["token"].startswith("mock-token-")


def test_login_unknown_email_returns_401(auth_client):
    response = auth_client.post(
        "/login",
        json={
            "email": "missing@example.com",
            "password": "StrongPass123",
        },
    )

    assert response.status_code == 401
    assert response.json()["error"]["code"] == "INVALID_CREDENTIALS"


def test_login_wrong_password_returns_401(auth_client):
    _register_default_user(auth_client)

    response = auth_client.post(
        "/login",
        json={
            "email": "alice@example.com",
            "password": "WrongPass123",
        },
    )

    assert response.status_code == 401
    assert response.json()["error"]["code"] == "INVALID_CREDENTIALS"


def test_login_missing_password_returns_400(auth_client):
    response = auth_client.post(
        "/login",
        json={
            "email": "alice@example.com",
        },
    )

    assert response.status_code == 400
    assert response.json()["error"]["code"] == "VALIDATION_ERROR"

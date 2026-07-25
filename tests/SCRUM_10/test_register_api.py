"""API tests for SCRUM-10 registration endpoint."""


def test_register_success_returns_201_and_expected_fields(auth_client):
    response = auth_client.post(
        "/register",
        json={
            "username": "alice",
            "email": "alice@example.com",
            "password": "StrongPass123",
        },
    )

    assert response.status_code == 201
    payload = response.json()
    assert payload["id"].startswith("u_")
    assert payload["username"] == "alice"
    assert payload["email"] == "alice@example.com"
    assert payload["message"] == "User registered successfully"
    assert "password" not in payload
    assert "password_hash" not in payload


def test_register_duplicate_email_is_case_insensitive(auth_client):
    auth_client.post(
        "/register",
        json={
            "username": "alice",
            "email": "alice@example.com",
            "password": "StrongPass123",
        },
    )

    duplicate = auth_client.post(
        "/register",
        json={
            "username": "alice-two",
            "email": "ALICE@EXAMPLE.COM",
            "password": "AnotherPass123",
        },
    )

    assert duplicate.status_code == 409
    assert duplicate.json()["error"]["code"] == "EMAIL_ALREADY_EXISTS"


def test_register_missing_email_returns_validation_error(auth_client):
    response = auth_client.post(
        "/register",
        json={
            "username": "alice",
            "password": "StrongPass123",
        },
    )

    assert response.status_code == 400
    payload = response.json()
    assert payload["error"]["code"] == "VALIDATION_ERROR"
    assert any(detail["field"] == "email" for detail in payload["error"].get("details", []))


def test_register_short_password_returns_400(auth_client):
    response = auth_client.post(
        "/register",
        json={
            "username": "alice",
            "email": "alice@example.com",
            "password": "short",
        },
    )

    assert response.status_code == 400
    assert response.json()["error"]["code"] == "VALIDATION_ERROR"

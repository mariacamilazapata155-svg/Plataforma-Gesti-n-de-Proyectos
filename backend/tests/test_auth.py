from datetime import timedelta

from app.core.security import create_access_token


def test_register_user(client):
    response = client.post(
        "/auth/register",
        json={
            "username": "newuser",
            "email": "newuser@example.com",
            "password": "password123",
        },
    )

    assert response.status_code == 201

    data = response.json()

    assert data["username"] == "newuser"
    assert data["email"] == "newuser@example.com"


def test_register_duplicate_email(client, users):
    response = client.post(
        "/auth/register",
        json={
            "username": "anotheruser",
            "email": users["owner"].email,
            "password": "password123",
        },
    )

    assert response.status_code == 400


def test_login_success(client, users):
    response = client.post(
        "/auth/login",
        data={
            "username": users["owner"].email,
            "password": "password",
        },
    )

    assert response.status_code == 200

    data = response.json()

    assert "access_token" in data
    assert data["token_type"] == "bearer"


def test_login_wrong_password(client, users):
    response = client.post(
        "/auth/login",
        data={
            "username": users["owner"].email,
            "password": "wrong_password",
        },
    )

    assert response.status_code == 401


def test_login_unknown_user(client):
    response = client.post(
        "/auth/login",
        data={
            "username": "unknown@example.com",
            "password": "password",
        },
    )

    assert response.status_code == 401


def test_access_me_with_valid_token(client, users):
    token = create_access_token(users["owner"].id)

    response = client.get(
        "/auth/me",
        headers={
            "Authorization": f"Bearer {token}",
        },
    )

    assert response.status_code == 200

    data = response.json()

    assert data["username"] == users["owner"].username
    assert data["email"] == users["owner"].email


def test_access_me_without_token(client):
    response = client.get("/auth/me")

    assert response.status_code == 401


def test_access_me_with_invalid_token(client):
    response = client.get(
        "/auth/me",
        headers={
            "Authorization": "Bearer invalid.token",
        },
    )

    assert response.status_code == 401


def test_access_me_with_expired_token(client, users):
    expired_token = create_access_token(
        users["owner"].id,
        expires_delta=timedelta(seconds=-1),
    )

    response = client.get(
        "/auth/me",
        headers={
            "Authorization": f"Bearer {expired_token}",
        },
    )

    assert response.status_code == 401
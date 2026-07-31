from conftest import auth_headers


def test_user_can_read_own_profile(client, users):
    response = client.get(
        f"/users/{users['owner'].id}",
        headers=auth_headers(users["owner"]),
    )

    assert response.status_code == 200
    data = response.json()
    assert data["id"] == users["owner"].id
    assert data["username"] == "owner"


def test_user_cannot_read_other_profile(client, users):
    response = client.get(
        f"/users/{users['owner'].id}",
        headers=auth_headers(users["member"]),
    )

    assert response.status_code == 403


def test_user_can_update_own_profile(client, users):
    response = client.put(
        f"/users/{users['member'].id}",
        headers=auth_headers(users["member"]),
        json={"username": "member_updated"},
    )

    assert response.status_code == 200
    assert response.json()["username"] == "member_updated"


def test_user_cannot_update_other_profile(client, users):
    response = client.put(
        f"/users/{users['owner'].id}",
        headers=auth_headers(users["member"]),
        json={"username": "hacked"},
    )

    assert response.status_code == 403


def test_duplicate_email_is_rejected(client, users):
    response = client.put(
        f"/users/{users['member'].id}",
        headers=auth_headers(users["member"]),
        json={"email": users["owner"].email},
    )

    assert response.status_code == 400


def test_duplicate_username_is_rejected(client, users):
    response = client.put(
        f"/users/{users['member'].id}",
        headers=auth_headers(users["member"]),
        json={"username": users["owner"].username},
    )

    assert response.status_code == 400


def test_user_can_change_password(client, users):
    response = client.put(
        f"/users/{users['member'].id}",
        headers=auth_headers(users["member"]),
        json={"password": "NewPassword123!"},
    )

    assert response.status_code == 200


def test_user_cannot_delete_other_profile(client, users):
    response = client.delete(
        f"/users/{users['owner'].id}",
        headers=auth_headers(users["member"]),
    )

    assert response.status_code == 403


def test_user_can_delete_own_profile(client, users):
    response = client.delete(
        f"/users/{users['outsider'].id}",
        headers=auth_headers(users["outsider"]),
    )

    assert response.status_code == 204


def test_non_existing_user_returns_404(client, users):
    response = client.get(
        "/users/99999",
        headers=auth_headers(users["owner"]),
    )

    assert response.status_code == 403

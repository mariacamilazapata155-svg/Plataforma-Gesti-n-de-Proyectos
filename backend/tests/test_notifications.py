from conftest import auth_headers


def test_user_can_list_own_notifications(
    client,
    users,
):
    response = client.get(
        "/notifications/",
        headers=auth_headers(users["member"]),
    )

    assert response.status_code == 200

    data = response.json()

    assert len(data) >= 1
    assert data[0]["recipient_id"] == users["member"].id


def test_other_user_cannot_list_foreign_notifications(
    client,
    users,
):
    response = client.get(
        "/notifications/",
        headers=auth_headers(users["owner"]),
    )

    assert response.status_code == 200

    data = response.json()

    assert all(
        notification["recipient_id"] == users["owner"].id for notification in data
    )


def test_recipient_can_read_notification(
    client,
    users,
    notification_fixture,
):
    response = client.get(
        f"/notifications/{notification_fixture.id}",
        headers=auth_headers(users["member"]),
    )

    assert response.status_code == 200

    assert response.json()["id"] == notification_fixture.id


def test_other_user_cannot_read_notification(
    client,
    users,
    notification_fixture,
):
    response = client.get(
        f"/notifications/{notification_fixture.id}",
        headers=auth_headers(users["owner"]),
    )

    assert response.status_code == 403


def test_recipient_can_mark_notification_as_read(
    client,
    users,
    notification_fixture,
):
    response = client.put(
        f"/notifications/{notification_fixture.id}/read",
        headers=auth_headers(users["member"]),
    )

    assert response.status_code == 200

    data = response.json()

    assert data["is_read"] is True


def test_other_user_cannot_mark_notification_as_read(
    client,
    users,
    notification_fixture,
):
    response = client.put(
        f"/notifications/{notification_fixture.id}/read",
        headers=auth_headers(users["owner"]),
    )

    assert response.status_code == 403


def test_user_can_mark_all_notifications_as_read(
    client,
    users,
):
    response = client.put(
        "/notifications/read-all",
        headers=auth_headers(users["member"]),
    )

    assert response.status_code == 200

    assert response.json() == {"message": "All notifications marked as read."}


def test_recipient_can_delete_notification(
    client,
    users,
    notification_fixture,
):
    response = client.delete(
        f"/notifications/{notification_fixture.id}",
        headers=auth_headers(users["member"]),
    )

    assert response.status_code == 204


def test_other_user_cannot_delete_notification(
    client,
    users,
    notification_fixture,
):
    response = client.delete(
        f"/notifications/{notification_fixture.id}",
        headers=auth_headers(users["owner"]),
    )

    assert response.status_code == 403


def test_read_non_existing_notification(
    client,
    users,
):
    response = client.get(
        "/notifications/999999",
        headers=auth_headers(users["member"]),
    )

    assert response.status_code == 404


def test_mark_non_existing_notification(
    client,
    users,
):
    response = client.put(
        "/notifications/999999/read",
        headers=auth_headers(users["member"]),
    )

    assert response.status_code == 404


def test_delete_non_existing_notification(
    client,
    users,
):
    response = client.delete(
        "/notifications/999999",
        headers=auth_headers(users["member"]),
    )

    assert response.status_code == 404

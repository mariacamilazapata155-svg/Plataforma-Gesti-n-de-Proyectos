from conftest import auth_headers


def test_member_can_read_activity(
    client,
    users,
    activity_log_fixture,
):
    response = client.get(
        f"/activity-logs/{activity_log_fixture.id}",
        headers=auth_headers(users["member"]),
    )

    assert response.status_code == 200

    data = response.json()

    assert data["id"] == activity_log_fixture.id


def test_viewer_can_read_activity(
    client,
    users,
    activity_log_fixture,
):
    response = client.get(
        f"/activity-logs/{activity_log_fixture.id}",
        headers=auth_headers(users["viewer"]),
    )

    assert response.status_code == 200


def test_outsider_cannot_read_activity(
    client,
    users,
    activity_log_fixture,
):
    response = client.get(
        f"/activity-logs/{activity_log_fixture.id}",
        headers=auth_headers(users["outsider"]),
    )

    assert response.status_code == 403


def test_member_can_list_project_activity(
    client,
    users,
    authorization_data,
):
    response = client.get(
        f"/activity-logs/projects/{authorization_data['project'].id}",
        headers=auth_headers(users["member"]),
    )

    assert response.status_code == 200

    assert isinstance(response.json(), list)


def test_viewer_can_list_project_activity(
    client,
    users,
    authorization_data,
):
    response = client.get(
        f"/activity-logs/projects/{authorization_data['project'].id}",
        headers=auth_headers(users["viewer"]),
    )

    assert response.status_code == 200


def test_outsider_cannot_list_project_activity(
    client,
    users,
    authorization_data,
):
    response = client.get(
        f"/activity-logs/projects/{authorization_data['project'].id}",
        headers=auth_headers(users["outsider"]),
    )

    assert response.status_code == 403


def test_user_can_list_own_activity(
    client,
    users,
):
    response = client.get(
        f"/activity-logs/users/{users['owner'].id}",
        headers=auth_headers(users["owner"]),
    )

    assert response.status_code == 200

    assert isinstance(response.json(), list)


def test_user_cannot_list_other_user_activity(
    client,
    users,
):
    response = client.get(
        f"/activity-logs/users/{users['member'].id}",
        headers=auth_headers(users["owner"]),
    )

    assert response.status_code == 403


def test_read_non_existing_activity(
    client,
    users,
):
    response = client.get(
        "/activity-logs/999999",
        headers=auth_headers(users["owner"]),
    )

    assert response.status_code == 404
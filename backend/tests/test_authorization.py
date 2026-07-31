from app.enums.task import TaskStatus

from conftest import auth_headers


def test_boards_require_authentication(client):
    response = client.get("/boards/")

    assert response.status_code == 401


def test_user_only_sees_boards_from_its_projects(
    client,
    users,
    authorization_data,
):
    response = client.get(
        "/boards/",
        headers=auth_headers(users["member"]),
    )

    assert response.status_code == 200
    assert [
        board["id"] for board in response.json()
    ] == [
        authorization_data["board"].id
    ]


def test_viewer_can_read_but_cannot_update_task(
    client,
    users,
    authorization_data,
):
    task_id = authorization_data["task"].id

    headers = auth_headers(users["viewer"])

    read_response = client.get(
        f"/tasks/{task_id}",
        headers=headers,
    )

    update_response = client.put(
        f"/tasks/{task_id}",
        headers=headers,
        json={
            "status": TaskStatus.DONE.value,
        },
    )

    assert read_response.status_code == 200
    assert update_response.status_code == 403


def test_member_can_update_own_task(
    client,
    users,
    authorization_data,
):
    task_id = authorization_data["task"].id

    response = client.put(
        f"/tasks/{task_id}",
        headers=auth_headers(users["member"]),
        json={
            "status": TaskStatus.IN_PROGRESS.value,
        },
    )

    assert response.status_code == 200


def test_member_cannot_edit_or_delete_another_members_comment(
    client,
    users,
    authorization_data,
):
    comment_id = authorization_data["comment"].id

    headers = auth_headers(
        users["other_member"]
    )

    update_response = client.put(
        f"/comments/{comment_id}",
        headers=headers,
        json={
            "content": "Intento no autorizado",
        },
    )

    delete_response = client.delete(
        f"/comments/{comment_id}",
        headers=headers,
    )

    assert update_response.status_code == 403
    assert delete_response.status_code == 403


def test_author_can_edit_own_comment(
    client,
    users,
    authorization_data,
):
    comment_id = authorization_data["comment"].id

    response = client.put(
        f"/comments/{comment_id}",
        headers=auth_headers(users["member"]),
        json={
            "content": "Comentario actualizado",
        },
    )

    assert response.status_code == 200


def test_outsider_cannot_read_project_resources(
    client,
    users,
    authorization_data,
):
    headers = auth_headers(
        users["outsider"]
    )

    project_response = client.get(
        f"/projects/{authorization_data['project'].id}",
        headers=headers,
    )

    task_response = client.get(
        f"/tasks/{authorization_data['task'].id}",
        headers=headers,
    )

    attachment_response = client.get(
        f"/attachments/tasks/{authorization_data['task'].id}",
        headers=headers,
    )

    members_response = client.get(
        f"/project-members/projects/{authorization_data['project'].id}",
        headers=headers,
    )

    assert project_response.status_code == 403
    assert task_response.status_code == 403
    assert attachment_response.status_code == 403
    assert members_response.status_code == 403


def test_owner_can_access_every_project_resource(
    client,
    users,
    authorization_data,
):
    headers = auth_headers(
        users["owner"]
    )

    assert client.get(
        f"/projects/{authorization_data['project'].id}",
        headers=headers,
    ).status_code == 200

    assert client.get(
        f"/boards/{authorization_data['board'].id}",
        headers=headers,
    ).status_code == 200

    assert client.get(
        f"/tasks/{authorization_data['task'].id}",
        headers=headers,
    ).status_code == 200


def test_user_cannot_access_another_users_profile(
    client,
    users,
):
    response = client.get(
        f"/users/{users['owner'].id}",
        headers=auth_headers(users["member"]),
    )

    assert response.status_code == 403


def test_owner_can_access_own_profile(
    client,
    users,
):
    response = client.get(
        f"/users/{users['owner'].id}",
        headers=auth_headers(users["owner"]),
    )

    assert response.status_code == 200
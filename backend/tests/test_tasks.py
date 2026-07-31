from app.enums.task import TaskStatus


from conftest import auth_headers


def test_member_can_read_task(
    client,
    users,
    authorization_data,
):
    task_id = authorization_data["task"].id

    response = client.get(
        f"/tasks/{task_id}",
        headers=auth_headers(users["member"]),
    )

    assert response.status_code == 200
    assert response.json()["id"] == task_id


def test_outsider_cannot_read_task(
    client,
    users,
    authorization_data,
):
    task_id = authorization_data["task"].id

    response = client.get(
        f"/tasks/{task_id}",
        headers=auth_headers(users["outsider"]),
    )

    assert response.status_code == 403


def test_viewer_cannot_update_task(
    client,
    users,
    authorization_data,
):
    task_id = authorization_data["task"].id

    response = client.put(
        f"/tasks/{task_id}",
        headers=auth_headers(users["viewer"]),
        json={
            "status": TaskStatus.DONE.value,
        },
    )

    assert response.status_code == 403


def test_member_can_update_task(
    client,
    users,
    authorization_data,
):
    task_id = authorization_data["task"].id

    response = client.put(
        f"/tasks/{task_id}",
        headers=auth_headers(users["member"]),
        json={
            "status": TaskStatus.DONE.value,
        },
    )

    assert response.status_code == 200
    assert response.json()["status"] == TaskStatus.DONE.value


def test_get_tasks_of_board(
    client,
    users,
    authorization_data,
):
    board_id = authorization_data["board"].id

    response = client.get(
        f"/tasks/board/{board_id}",
        headers=auth_headers(users["member"]),
    )

    assert response.status_code == 200
    assert len(response.json()) >= 1


def test_assign_task(
    client,
    users,
    authorization_data,
):
    task_id = authorization_data["task"].id

    response = client.patch(
        f"/tasks/{task_id}/assign/{users['member'].id}",
        headers=auth_headers(users["owner"]),
    )

    assert response.status_code == 200


def test_unassign_task(
    client,
    users,
    authorization_data,
):
    task_id = authorization_data["task"].id

    response = client.patch(
        f"/tasks/{task_id}/unassign",
        headers=auth_headers(users["owner"]),
    )

    assert response.status_code == 200


def test_assign_non_member_returns_error(
    client,
    users,
    authorization_data,
):
    task_id = authorization_data["task"].id

    response = client.patch(
        f"/tasks/{task_id}/assign/{users['outsider'].id}",
        headers=auth_headers(users["owner"]),
    )

    assert response.status_code == 404


def test_delete_task_as_member(
    client,
    users,
    authorization_data,
):
    task_id = authorization_data["task"].id

    response = client.delete(
        f"/tasks/{task_id}",
        headers=auth_headers(users["member"]),
    )

    assert response.status_code == 204


def test_delete_task_as_viewer_forbidden(
    client,
    users,
    authorization_data,
):
    task_id = authorization_data["task"].id

    response = client.delete(
        f"/tasks/{task_id}",
        headers=auth_headers(users["viewer"]),
    )

    assert response.status_code == 403
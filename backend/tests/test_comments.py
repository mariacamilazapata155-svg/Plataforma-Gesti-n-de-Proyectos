from conftest import auth_headers


def test_member_can_create_comment(
    client,
    users,
    authorization_data,
):
    response = client.post(
        "/comments/",
        headers=auth_headers(users["member"]),
        json={
            "task_id": authorization_data["task"].id,
            "content": "Nuevo comentario",
        },
    )

    assert response.status_code == 201
    assert response.json()["content"] == "Nuevo comentario"


def test_outsider_cannot_create_comment(
    client,
    users,
    authorization_data,
):
    response = client.post(
        "/comments/",
        headers=auth_headers(users["outsider"]),
        json={
            "task_id": authorization_data["task"].id,
            "content": "Intento",
        },
    )

    assert response.status_code == 403


def test_member_can_read_comment(
    client,
    users,
    authorization_data,
):
    comment = authorization_data["comment"]

    response = client.get(
        f"/comments/{comment.id}",
        headers=auth_headers(users["member"]),
    )

    assert response.status_code == 200
    assert response.json()["id"] == comment.id


def test_outsider_cannot_read_comment(
    client,
    users,
    authorization_data,
):
    comment = authorization_data["comment"]

    response = client.get(
        f"/comments/{comment.id}",
        headers=auth_headers(users["outsider"]),
    )

    assert response.status_code == 403


def test_get_comments_of_task(
    client,
    users,
    authorization_data,
):
    response = client.get(
        f"/comments/task/{authorization_data['task'].id}",
        headers=auth_headers(users["member"]),
    )

    assert response.status_code == 200
    assert len(response.json()) >= 1


def test_author_can_update_comment(
    client,
    users,
    authorization_data,
):
    comment = authorization_data["comment"]

    response = client.put(
        f"/comments/{comment.id}",
        headers=auth_headers(users["member"]),
        json={
            "content": "Comentario actualizado",
        },
    )

    assert response.status_code == 200
    assert response.json()["content"] == "Comentario actualizado"


def test_other_member_cannot_update_comment(
    client,
    users,
    authorization_data,
):
    comment = authorization_data["comment"]

    response = client.put(
        f"/comments/{comment.id}",
        headers=auth_headers(users["other_member"]),
        json={
            "content": "No permitido",
        },
    )

    assert response.status_code == 403


def test_author_can_delete_comment(
    client,
    users,
    authorization_data,
):
    comment = authorization_data["comment"]

    response = client.delete(
        f"/comments/{comment.id}",
        headers=auth_headers(users["member"]),
    )

    assert response.status_code == 204


def test_other_member_cannot_delete_comment(
    client,
    users,
    authorization_data,
):
    comment = authorization_data["comment"]

    response = client.delete(
        f"/comments/{comment.id}",
        headers=auth_headers(users["other_member"]),
    )

    assert response.status_code == 403


def test_viewer_can_read_comments_but_cannot_create(
    client,
    users,
    authorization_data,
):
    read_response = client.get(
        f"/comments/task/{authorization_data['task'].id}",
        headers=auth_headers(users["viewer"]),
    )

    create_response = client.post(
        "/comments/",
        headers=auth_headers(users["viewer"]),
        json={
            "task_id": authorization_data["task"].id,
            "content": "Viewer",
        },
    )

    assert read_response.status_code == 200
    assert create_response.status_code == 403

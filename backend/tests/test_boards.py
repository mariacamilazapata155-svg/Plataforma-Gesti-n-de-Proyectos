from conftest import auth_headers


def test_member_can_create_board(
    client,
    users,
    authorization_data,
):
    response = client.post(
        "/boards/",
        headers=auth_headers(users["member"]),
        json={
            "title": "Nuevo tablero",
            "project_id": authorization_data["project"].id,
        },
    )

    assert response.status_code == 201
    assert response.json()["title"] == "Nuevo tablero"


def test_viewer_cannot_create_board(
    client,
    users,
    authorization_data,
):
    response = client.post(
        "/boards/",
        headers=auth_headers(users["viewer"]),
        json={
            "title": "No permitido",
            "project_id": authorization_data["project"].id,
        },
    )

    assert response.status_code == 403


def test_outsider_cannot_create_board(
    client,
    users,
    authorization_data,
):
    response = client.post(
        "/boards/",
        headers=auth_headers(users["outsider"]),
        json={
            "title": "Intento",
            "project_id": authorization_data["project"].id,
        },
    )

    assert response.status_code == 403


def test_member_can_read_board(
    client,
    users,
    authorization_data,
):
    board = authorization_data["board"]

    response = client.get(
        f"/boards/{board.id}",
        headers=auth_headers(users["member"]),
    )

    assert response.status_code == 200
    assert response.json()["id"] == board.id


def test_outsider_cannot_read_board(
    client,
    users,
    authorization_data,
):
    board = authorization_data["board"]

    response = client.get(
        f"/boards/{board.id}",
        headers=auth_headers(users["outsider"]),
    )

    assert response.status_code == 403


def test_viewer_can_read_board(
    client,
    users,
    authorization_data,
):
    board = authorization_data["board"]

    response = client.get(
        f"/boards/{board.id}",
        headers=auth_headers(users["viewer"]),
    )

    assert response.status_code == 200


def test_member_can_list_project_boards(
    client,
    users,
    authorization_data,
):
    response = client.get(
        f"/boards/project/{authorization_data['project'].id}",
        headers=auth_headers(users["member"]),
    )

    assert response.status_code == 200
    assert len(response.json()) >= 1


def test_outsider_cannot_list_project_boards(
    client,
    users,
    authorization_data,
):
    response = client.get(
        f"/boards/project/{authorization_data['project'].id}",
        headers=auth_headers(users["outsider"]),
    )

    assert response.status_code == 403


def test_member_cannot_update_board(
    client,
    users,
    authorization_data,
):
    board = authorization_data["board"]

    response = client.put(
        f"/boards/{board.id}",
        headers=auth_headers(users["member"]),
        json={
            "title": "Tablero actualizado",
        },
    )

    assert response.status_code == 403


def test_viewer_cannot_update_board(
    client,
    users,
    authorization_data,
):
    board = authorization_data["board"]

    response = client.put(
        f"/boards/{board.id}",
        headers=auth_headers(users["viewer"]),
        json={
            "title": "No permitido",
        },
    )

    assert response.status_code == 403


def test_member_cannot_delete_board(
    client,
    users,
    authorization_data,
):
    board = authorization_data["board"]

    response = client.delete(
        f"/boards/{board.id}",
        headers=auth_headers(users["member"]),
    )

    assert response.status_code == 403


def test_viewer_cannot_delete_board(
    client,
    users,
    authorization_data,
):
    board = authorization_data["board"]

    response = client.delete(
        f"/boards/{board.id}",
        headers=auth_headers(users["viewer"]),
    )

    assert response.status_code == 403


def test_owner_can_update_board(
    client,
    users,
    authorization_data,
):
    board = authorization_data["board"]

    response = client.put(
        f"/boards/{board.id}",
        headers=auth_headers(users["owner"]),
        json={
            "title": "Actualizado por owner",
        },
    )

    assert response.status_code == 200
    assert response.json()["title"] == "Actualizado por owner"


def test_owner_can_delete_board(
    client,
    users,
    authorization_data,
):
    board = authorization_data["board"]

    response = client.delete(
        f"/boards/{board.id}",
        headers=auth_headers(users["owner"]),
    )

    assert response.status_code == 204
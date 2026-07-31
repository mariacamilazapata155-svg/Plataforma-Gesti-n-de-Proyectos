from conftest import auth_headers


def test_create_project(client, users):
    response = client.post(
        "/projects/",
        headers=auth_headers(users["owner"]),
        json={
            "title": "Nuevo proyecto",
            "description": "Proyecto creado desde test",
        },
    )

    assert response.status_code == 201

    data = response.json()

    assert data["title"] == "Nuevo proyecto"
    assert data["owner_id"] == users["owner"].id


def test_owner_can_read_project(
    client,
    users,
    authorization_data,
):
    response = client.get(
        f"/projects/{authorization_data['project'].id}",
        headers=auth_headers(users["owner"]),
    )

    assert response.status_code == 200


def test_member_can_read_project(
    client,
    users,
    authorization_data,
):
    response = client.get(
        f"/projects/{authorization_data['project'].id}",
        headers=auth_headers(users["member"]),
    )

    assert response.status_code == 200


def test_viewer_can_read_project(
    client,
    users,
    authorization_data,
):
    response = client.get(
        f"/projects/{authorization_data['project'].id}",
        headers=auth_headers(users["viewer"]),
    )

    assert response.status_code == 200


def test_outsider_cannot_read_project(
    client,
    users,
    authorization_data,
):
    response = client.get(
        f"/projects/{authorization_data['project'].id}",
        headers=auth_headers(users["outsider"]),
    )

    assert response.status_code == 403


def test_project_not_found(
    client,
    users,
):
    response = client.get(
        "/projects/999999",
        headers=auth_headers(users["owner"]),
    )

    assert response.status_code == 404


def test_owner_can_update_project(
    client,
    users,
    authorization_data,
):
    response = client.put(
        f"/projects/{authorization_data['project'].id}",
        headers=auth_headers(users["owner"]),
        json={
            "title": "Proyecto actualizado",
        },
    )

    assert response.status_code == 200
    assert response.json()["title"] == "Proyecto actualizado"


def test_member_cannot_update_project(
    client,
    users,
    authorization_data,
):
    response = client.put(
        f"/projects/{authorization_data['project'].id}",
        headers=auth_headers(users["member"]),
        json={
            "title": "No permitido",
        },
    )

    assert response.status_code == 403


def test_owner_can_delete_project(
    client,
    users,
):
    response = client.post(
        "/projects/",
        headers=auth_headers(users["owner"]),
        json={
            "title": "Proyecto temporal",
            "description": "Eliminar",
        },
    )

    project_id = response.json()["id"]

    delete_response = client.delete(
        f"/projects/{project_id}",
        headers=auth_headers(users["owner"]),
    )

    assert delete_response.status_code == 204

    read_response = client.get(
        f"/projects/{project_id}",
        headers=auth_headers(users["owner"]),
    )

    assert read_response.status_code == 404


def test_member_cannot_delete_project(
    client,
    users,
    authorization_data,
):
    response = client.delete(
        f"/projects/{authorization_data['project'].id}",
        headers=auth_headers(users["member"]),
    )

    assert response.status_code == 403


def test_owner_can_list_only_own_projects(
    client,
    users,
):
    response = client.get(
        f"/projects/owner/{users['owner'].id}",
        headers=auth_headers(users["owner"]),
    )

    assert response.status_code == 200


def test_user_cannot_list_other_users_projects(
    client,
    users,
):
    response = client.get(
        f"/projects/owner/{users['outsider'].id}",
        headers=auth_headers(users["owner"]),
    )

    assert response.status_code == 403


def test_authenticated_user_can_list_projects(
    client,
    users,
):
    response = client.get(
        "/projects/",
        headers=auth_headers(users["owner"]),
    )

    assert response.status_code == 200
    assert isinstance(response.json(), list)
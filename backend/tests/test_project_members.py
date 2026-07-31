from app.core.security import create_access_token
from app.enums.project_role import ProjectRole


def auth_headers(user):
    token = create_access_token(user.id)

    return {
        "Authorization": f"Bearer {token}",
    }


def test_owner_can_add_member(
    client,
    users,
    authorization_data,
):
    project = authorization_data["project"]

    response = client.post(
        f"/project-members/projects/{project.id}",
        headers=auth_headers(users["owner"]),
        json={
            "user_id": users["outsider"].id,
            "role": ProjectRole.MEMBER.value,
        },
    )

    assert response.status_code == 201

    data = response.json()

    assert data["user_id"] == users["outsider"].id
    assert data["role"] == ProjectRole.MEMBER.value


def test_member_cannot_add_member(
    client,
    users,
    authorization_data,
):
    project = authorization_data["project"]

    response = client.post(
        f"/project-members/projects/{project.id}",
        headers=auth_headers(users["member"]),
        json={
            "user_id": users["outsider"].id,
            "role": ProjectRole.MEMBER.value,
        },
    )

    assert response.status_code == 403


def test_viewer_cannot_add_member(
    client,
    users,
    authorization_data,
):
    project = authorization_data["project"]

    response = client.post(
        f"/project-members/projects/{project.id}",
        headers=auth_headers(users["viewer"]),
        json={
            "user_id": users["outsider"].id,
            "role": ProjectRole.MEMBER.value,
        },
    )

    assert response.status_code == 403


def test_member_can_list_project_members(
    client,
    users,
    authorization_data,
):
    project = authorization_data["project"]

    response = client.get(
        f"/project-members/projects/{project.id}",
        headers=auth_headers(users["member"]),
    )

    assert response.status_code == 200

    assert len(response.json()) >= 4


def test_viewer_can_list_project_members(
    client,
    users,
    authorization_data,
):
    project = authorization_data["project"]

    response = client.get(
        f"/project-members/projects/{project.id}",
        headers=auth_headers(users["viewer"]),
    )

    assert response.status_code == 200


def test_outsider_cannot_list_project_members(
    client,
    users,
    authorization_data,
):
    project = authorization_data["project"]

    response = client.get(
        f"/project-members/projects/{project.id}",
        headers=auth_headers(users["outsider"]),
    )

    assert response.status_code == 403


def test_owner_can_read_member(
    client,
    db_session,
    users,
    authorization_data,
):
    from app.crud.crud_project_member import get_user_membership

    membership = get_user_membership(
        db=db_session,
        project_id=authorization_data["project"].id,
        user_id=users["member"].id,
    )

    response = client.get(
        f"/project-members/{membership.id}",
        headers=auth_headers(users["owner"]),
    )

    assert response.status_code == 200


def test_outsider_cannot_read_member(
    client,
    db_session,
    users,
    authorization_data,
):
    from app.crud.crud_project_member import get_user_membership

    membership = get_user_membership(
        db=db_session,
        project_id=authorization_data["project"].id,
        user_id=users["member"].id,
    )

    response = client.get(
        f"/project-members/{membership.id}",
        headers=auth_headers(users["outsider"]),
    )

    assert response.status_code == 403


def test_owner_can_update_member_role(
    client,
    db_session,
    users,
    authorization_data,
):
    from app.crud.crud_project_member import get_user_membership

    membership = get_user_membership(
        db=db_session,
        project_id=authorization_data["project"].id,
        user_id=users["member"].id,
    )

    response = client.put(
        f"/project-members/{membership.id}",
        headers=auth_headers(users["owner"]),
        json={
            "role": ProjectRole.ADMIN.value,
        },
    )

    assert response.status_code == 200

    assert response.json()["role"] == ProjectRole.ADMIN.value


def test_member_cannot_update_member_role(
    client,
    db_session,
    users,
    authorization_data,
):
    from app.crud.crud_project_member import get_user_membership

    membership = get_user_membership(
        db=db_session,
        project_id=authorization_data["project"].id,
        user_id=users["viewer"].id,
    )

    response = client.put(
        f"/project-members/{membership.id}",
        headers=auth_headers(users["member"]),
        json={
            "role": ProjectRole.ADMIN.value,
        },
    )

    assert response.status_code == 403


def test_owner_can_remove_member(
    client,
    db_session,
    users,
    authorization_data,
):
    from app.crud.crud_project_member import get_user_membership

    membership = get_user_membership(
        db=db_session,
        project_id=authorization_data["project"].id,
        user_id=users["other_member"].id,
    )

    response = client.delete(
        f"/project-members/{membership.id}",
        headers=auth_headers(users["owner"]),
    )

    assert response.status_code == 204


def test_member_cannot_remove_member(
    client,
    db_session,
    users,
    authorization_data,
):
    from app.crud.crud_project_member import get_user_membership

    membership = get_user_membership(
        db=db_session,
        project_id=authorization_data["project"].id,
        user_id=users["viewer"].id,
    )

    response = client.delete(
        f"/project-members/{membership.id}",
        headers=auth_headers(users["member"]),
    )

    assert response.status_code == 403

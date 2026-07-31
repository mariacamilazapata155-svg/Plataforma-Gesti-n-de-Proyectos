import io

from app.models.attachment import Attachment


def test_owner_can_upload_attachment(
    client,
    owner_headers,
    authorization_data,
):
    response = client.post(
        f"/attachments/tasks/{authorization_data['task'].id}",
        headers=owner_headers,
        files={
            "file": (
                "manual.pdf",
                io.BytesIO(b"PDF DATA"),
                "application/pdf",
            )
        },
    )

    assert response.status_code == 201

    data = response.json()

    assert data["original_filename"] == "manual.pdf"
    assert data["task_id"] == authorization_data["task"].id


def test_member_can_upload_attachment(
    client,
    member_headers,
    authorization_data,
):
    response = client.post(
        f"/attachments/tasks/{authorization_data['task'].id}",
        headers=member_headers,
        files={
            "file": (
                "manual.pdf",
                io.BytesIO(b"PDF DATA"),
                "application/pdf",
            )
        },
    )

    assert response.status_code == 201


def test_viewer_cannot_upload_attachment(
    client,
    viewer_headers,
    authorization_data,
):
    response = client.post(
        f"/attachments/tasks/{authorization_data['task'].id}",
        headers=viewer_headers,
        files={
            "file": (
                "manual.pdf",
                io.BytesIO(b"PDF DATA"),
                "application/pdf",
            )
        },
    )

    assert response.status_code == 403


def test_member_can_list_task_attachments(
    client,
    member_headers,
    authorization_data,
    attachment_fixture,
):
    response = client.get(
        f"/attachments/tasks/{authorization_data['task'].id}",
        headers=member_headers,
    )

    assert response.status_code == 200
    assert len(response.json()) >= 1


def test_outsider_cannot_list_task_attachments(
    client,
    outsider_headers,
    authorization_data,
):
    response = client.get(
        f"/attachments/tasks/{authorization_data['task'].id}",
        headers=outsider_headers,
    )

    assert response.status_code == 403


def test_member_can_read_attachment(
    client,
    member_headers,
    attachment_fixture,
):
    response = client.get(
        f"/attachments/{attachment_fixture.id}",
        headers=member_headers,
    )

    assert response.status_code == 200

    data = response.json()

    assert data["id"] == attachment_fixture.id


def test_outsider_cannot_read_attachment(
    client,
    outsider_headers,
    attachment_fixture,
):
    response = client.get(
        f"/attachments/{attachment_fixture.id}",
        headers=outsider_headers,
    )

    assert response.status_code == 403


def test_member_can_download_attachment(
    client,
    member_headers,
    attachment_fixture,
):
    response = client.get(
        f"/attachments/download/{attachment_fixture.id}",
        headers=member_headers,
    )

    assert response.status_code == 200


def test_member_can_delete_attachment(
    client,
    member_headers,
    attachment_fixture,
):
    response = client.delete(
        f"/attachments/{attachment_fixture.id}",
        headers=member_headers,
    )

    assert response.status_code == 204


def test_outsider_cannot_delete_attachment(
    client,
    outsider_headers,
    attachment_fixture,
):
    response = client.delete(
        f"/attachments/{attachment_fixture.id}",
        headers=outsider_headers,
    )

    assert response.status_code == 403
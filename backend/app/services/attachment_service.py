import os
import shutil
import uuid

from fastapi import UploadFile
from sqlalchemy.orm import Session

from app.models.user import User
from app.models.attachment import Attachment

from app.crud.crud_attachment import (
    create_attachment,
    get_attachment,
    get_attachments_by_task,
    delete_attachment,
)

from app.crud.crud_task import get_task

from app.core.permissions_project_member import (
    require_project_role,
)

from app.enums.project_role import ProjectRole

from app.services.activity_log_service import (
    log_activity,
)

from app.schemas.activity_log_schema import (
    ActivityLogCreate,
)

from app.enums.activity_action import (
    ActivityAction,
)

from app.services.notification_service import (
    notify,
)

from app.schemas.notification_schema import (
    NotificationCreate,
)

from app.enums.notification_type import (
    NotificationType,
)

from app.crud.crud_board import (
    get_board,
)

UPLOAD_DIRECTORY = "uploads/attachments"

MAX_FILE_SIZE = 10 * 1024 * 1024  # 10 MB

ALLOWED_CONTENT_TYPES = {
    "image/png",
    "image/jpeg",
    "image/jpg",
    "image/gif",
    "application/pdf",
    "application/zip",
    "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
    "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
    "application/vnd.openxmlformats-officedocument.presentationml.presentation",
}

def upload_new_attachment(
    db: Session,
    task_id: int,
    file: UploadFile,
    current_user: User,
):
    """
    Sube un archivo a una tarea.
    """

    task = get_task(
        db,
        task_id,
    )

    if task is None:
        raise ValueError(
            "Task not found."
        )

    require_project_role(
        db=db,
        project_id=task.board.project_id,
        current_user=current_user,
        allowed_roles=[
            ProjectRole.OWNER,
            ProjectRole.ADMIN,
            ProjectRole.MEMBER,
        ],
    )

    if file.content_type not in ALLOWED_CONTENT_TYPES:
        raise ValueError(
            "File type not allowed."
        )

    contents = file.file.read()

    if len(contents) > MAX_FILE_SIZE:
        raise ValueError(
            "Maximum file size exceeded."
        )

    os.makedirs(
        UPLOAD_DIRECTORY,
        exist_ok=True,
    )

    extension = os.path.splitext(
        file.filename
    )[1]

    generated_name = (
        f"{uuid.uuid4()}{extension}"
    )

    storage_path = os.path.join(
        UPLOAD_DIRECTORY,
        generated_name,
    )

    with open(
        storage_path,
        "wb",
    ) as buffer:
        buffer.write(contents)

    attachment = Attachment(
        filename=generated_name,
        original_filename=file.filename,
        content_type=file.content_type,
        file_size=len(contents),
        storage_path=storage_path,
        task_id=task_id,
        uploaded_by=current_user.id,
    )

    new_attachment = create_attachment(
        db,
        attachment,
    )

    board = get_board(
        db,
        task.board_id,
    )

    log_activity(
        db=db,
        current_user=current_user,
        activity=ActivityLogCreate(
            action=ActivityAction.ATTACHMENT_UPLOADED,
            entity_type="attachment",
            entity_id=new_attachment.id,
            description=(
                f'{current_user.username} subió el archivo '
                f'"{new_attachment.original_filename}" '
                f'a la tarea "{task.title}"'
            ),
            project_id=board.project_id,
        ),
    )

    if (
        task.assigned_to_id is not None
        and task.assigned_to_id != current_user.id
    ):
        notify(
            db=db,
            notification=NotificationCreate(
                type=NotificationType.ATTACHMENT_UPLOADED,
                title="Nuevo archivo adjunto",
                message=(
                    f'{current_user.username} subió el archivo '
                    f'"{new_attachment.original_filename}" '
                    f'a la tarea "{task.title}".'
                ),
                entity_type="attachment",
                entity_id=new_attachment.id,
                recipient_id=task.assigned_to_id,
                sender_id=current_user.id,
                project_id=board.project_id,
            ),
        )

    return new_attachment

def get_attachment_by_id(
    db: Session,
    attachment_id: int,
    current_user: User,
):
    attachment = get_attachment(
        db,
        attachment_id,
    )

    if attachment is None:
        return None

    require_project_role(
        db=db,
        project_id=attachment.task.board.project_id,
        current_user=current_user,
        allowed_roles=list(ProjectRole),
    )

    return attachment

def get_task_attachments(
    db: Session,
    task_id: int,
    current_user: User,
):
    task = get_task(db, task_id)

    if task is None:
        raise ValueError("Task not found.")

    require_project_role(
        db=db,
        project_id=task.board.project_id,
        current_user=current_user,
        allowed_roles=list(ProjectRole),
    )

    return get_attachments_by_task(
        db,
        task_id,
    )

def remove_attachment(
    db: Session,
    attachment_id: int,
    current_user: User,
):
    attachment = get_attachment(
        db,
        attachment_id,
    )

    if attachment is None:
        return None

    task = attachment.task

    board = get_board(
        db,
        task.board_id,
    )

    if board is None:
        raise ValueError(
            "Board not found."
        )

    require_project_role(
        db=db,
        project_id=board.project_id,
        current_user=current_user,
        allowed_roles=[
            ProjectRole.OWNER,
            ProjectRole.ADMIN,
            ProjectRole.MEMBER,
        ],
    )

    log_activity(
        db=db,
        current_user=current_user,
        activity=ActivityLogCreate(
            action=ActivityAction.ATTACHMENT_DELETED,
            entity_type="attachment",
            entity_id=attachment.id,
            description=(
                f'{current_user.username} eliminó el archivo '
                f'"{attachment.original_filename}" '
                f'de la tarea "{task.title}"'
            ),
            project_id=board.project_id,
        ),
    )

    if (
        task.assigned_to_id is not None
        and task.assigned_to_id != current_user.id
    ):
        notify(
            db=db,
            notification=NotificationCreate(
                type=NotificationType.ATTACHMENT_DELETED,
                title="Archivo adjunto eliminado",
                message=(
                    f'{current_user.username} eliminó el archivo '
                    f'"{attachment.original_filename}" '
                    f'de la tarea "{task.title}".'
                ),
                entity_type="attachment",
                entity_id=attachment.id,
                recipient_id=task.assigned_to_id,
                sender_id=current_user.id,
                project_id=board.project_id,
            ),
        )

    return delete_attachment(
        db,
        attachment_id,
    )

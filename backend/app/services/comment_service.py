from sqlalchemy.orm import Session

from app.models.user import User

from app.crud.crud_task import get_task

from app.crud.crud_comment import (
    create_comment,
    get_comment,
    get_comments_by_task,
    update_comment,
    delete_comment,
)

from app.crud.crud_project_member import (
    get_user_membership,
)

from app.schemas.comment_schema import (
    CommentCreate,
    CommentUpdate,
)

from app.enums.project_role import ProjectRole

from app.core.permissions_project_member import (
    require_project_role,
)

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

def create_new_comment(
    db: Session,
    comment: CommentCreate,
    current_user: User,
):
    """
    Crea un comentario en una tarea.
    """

    task = get_task(
        db,
        comment.task_id,
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

    new_comment = create_comment(
        db,
        comment,
        current_user.id,
    )

    board = get_board(
        db,
        task.board_id,
    )

    log_activity(
        db=db,
        current_user=current_user,
        activity=ActivityLogCreate(
            action=ActivityAction.COMMENT_CREATED,
            entity_type="comment",
            entity_id=new_comment.id,
            description=(
                f'{current_user.username} agregó un comentario '
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
                type=NotificationType.TASK_COMMENTED,
                title="Nuevo comentario",
                message=(
                    f'{current_user.username} comentó la tarea '
                    f'"{task.title}".'
                ),
                entity_type="comment",
                entity_id=new_comment.id,
                recipient_id=task.assigned_to_id,
                sender_id=current_user.id,
                project_id=board.project_id,
            ),
        )

    return new_comment


def get_comment_by_id(
    db: Session,
    comment_id: int,
    current_user: User,
):
    """
    Obtiene un comentario.
    """

    comment = get_comment(
        db,
        comment_id,
    )

    if comment is None:
        return None

    require_project_role(
        db=db,
        project_id=comment.task.board.project_id,
        current_user=current_user,
        allowed_roles=[
            ProjectRole.OWNER,
            ProjectRole.ADMIN,
            ProjectRole.MEMBER,
            ProjectRole.VIEWER,
        ],
    )

    return comment


def get_comments_of_task(
    db: Session,
    task_id: int,
    current_user: User,
):
    """
    Obtiene los comentarios de una tarea.
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
            ProjectRole.VIEWER,
        ],
    )

    return get_comments_by_task(
        db,
        task_id,
    )


def update_existing_comment(
    db: Session,
    comment_id: int,
    comment: CommentUpdate,
    current_user: User,
):
    db_comment = get_comment(
        db,
        comment_id,
    )

    if db_comment is None:
        return None

    task = db_comment.task

    board = get_board(
        db,
        task.board_id,
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

    membership = get_user_membership(
        db=db,
        project_id=board.project_id,
        user_id=current_user.id,
    )

    if (
        membership.role == ProjectRole.MEMBER
        and db_comment.author_id != current_user.id
    ):
        raise PermissionError(
            "You can only edit your own comments."
        )

    updated_comment = update_comment(
        db,
        comment_id,
        comment,
    )

    log_activity(
        db=db,
        current_user=current_user,
        activity=ActivityLogCreate(
            action=ActivityAction.COMMENT_UPDATED,
            entity_type="comment",
            entity_id=updated_comment.id,
            description=(
                f'{current_user.username} editó un comentario '
                f'en la tarea "{task.title}"'
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
                type=NotificationType.COMMENT_UPDATED,
                title="Comentario actualizado",
                message=(
                    f'{current_user.username} actualizó un comentario '
                    f'en la tarea "{task.title}".'
                ),
                entity_type="comment",
                entity_id=updated_comment.id,
                recipient_id=task.assigned_to_id,
                sender_id=current_user.id,
                project_id=board.project_id,
            ),
        )

    return updated_comment


def remove_comment(
    db: Session,
    comment_id: int,
    current_user: User,
):
    comment = get_comment(
        db,
        comment_id,
    )

    if comment is None:
        return None

    task = comment.task

    board = get_board(
        db,
        task.board_id,
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

    membership = get_user_membership(
        db=db,
        project_id=board.project_id,
        user_id=current_user.id,
    )

    if (
        membership.role == ProjectRole.MEMBER
        and comment.author_id != current_user.id
    ):
        raise PermissionError(
            "You can only delete your own comments."
        )

    log_activity(
        db=db,
        current_user=current_user,
        activity=ActivityLogCreate(
            action=ActivityAction.COMMENT_DELETED,
            entity_type="comment",
            entity_id=comment.id,
            description=(
                f'{current_user.username} eliminó un comentario '
                f'de la tarea "{task.title}"'
            ),
            project_id=board.project_id,
        ),
    )

    return delete_comment(
        db,
        comment_id,
    )
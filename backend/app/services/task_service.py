from sqlalchemy.orm import Session

from app.core.permissions_project_member import require_project_role
from app.crud.crud_board import get_board
from app.crud.crud_project_member import get_user_membership
from app.crud.crud_task import (
    assign_task,
    create_task,
    delete_task,
    get_task,
    get_tasks_by_board,
    get_tasks_for_user,
    update_task,
)
from app.crud.crud_user import get_user
from app.enums.activity_action import ActivityAction
from app.enums.notification_type import NotificationType
from app.enums.project_role import ProjectRole
from app.enums.task import TaskStatus
from app.models.user import User
from app.schemas.activity_log_schema import ActivityLogCreate
from app.schemas.notification_schema import NotificationCreate
from app.schemas.task_schema import TaskCreate, TaskUpdate
from app.services.activity_log_service import log_activity
from app.services.notification_service import notify


def create_new_task(
    db: Session,
    task: TaskCreate,
    current_user: User,
):
    """
    Crea una tarea si el usuario tiene permisos
    sobre el proyecto.
    """

    board = get_board(
        db,
        task.board_id,
    )

    if board is None:
        raise ValueError("Board not found.")

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

    new_task = create_task(
        db,
        task,
    )

    log_activity(
        db=db,
        current_user=current_user,
        activity=ActivityLogCreate(
            action=ActivityAction.TASK_CREATED,
            entity_type="task",
            entity_id=new_task.id,
            description=(
                f"{current_user.username} creó la tarea " f'"{new_task.title}"'
            ),
            project_id=board.project_id,
        ),
    )

    if new_task.assigned_to_id is not None:

        assigned_user = get_user(
            db,
            new_task.assigned_to_id,
        )

        if assigned_user is not None:

            log_activity(
                db=db,
                current_user=current_user,
                activity=ActivityLogCreate(
                    action=ActivityAction.TASK_ASSIGNED,
                    entity_type="task",
                    entity_id=new_task.id,
                    description=(
                        f"{current_user.username} asignó la tarea "
                        f'"{new_task.title}" a '
                        f"{assigned_user.username}"
                    ),
                    project_id=board.project_id,
                ),
            )

            if assigned_user.id != current_user.id:

                notify(
                    db=db,
                    notification=NotificationCreate(
                        type=NotificationType.TASK_ASSIGNED,
                        title="Nueva tarea asignada",
                        message=(
                            f"{current_user.username} te asignó la tarea "
                            f'"{new_task.title}".'
                        ),
                        entity_type="task",
                        entity_id=new_task.id,
                        recipient_id=assigned_user.id,
                        sender_id=current_user.id,
                        project_id=board.project_id,
                    ),
                )

    return new_task


def get_task_by_id(
    db: Session,
    task_id: int,
    current_user: User,
):
    task = get_task(
        db,
        task_id,
    )

    if task is None:
        return None

    require_project_role(
        db=db,
        project_id=task.board.project_id,
        current_user=current_user,
        allowed_roles=list(ProjectRole),
    )

    return task


def get_all_tasks(
    db: Session,
    current_user: User,
):
    return get_tasks_for_user(db, current_user.id)


def get_tasks_of_board(
    db: Session,
    board_id: int,
    current_user: User,
):
    board = get_board(db, board_id)

    if board is None:
        raise ValueError("Board not found.")

    require_project_role(
        db=db,
        project_id=board.project_id,
        current_user=current_user,
        allowed_roles=list(ProjectRole),
    )

    return get_tasks_by_board(
        db,
        board_id,
    )


def update_existing_task(
    db: Session,
    task_id: int,
    task: TaskUpdate,
    current_user: User,
):
    db_task = get_task(
        db,
        task_id,
    )

    if db_task is None:
        return None

    board = get_board(
        db,
        db_task.board_id,
    )

    previous_assigned = db_task.assigned_to_id
    previous_status = db_task.status

    require_project_role(
        db=db,
        project_id=board.project_id,
        current_user=current_user,
        allowed_roles=[ProjectRole.OWNER, ProjectRole.ADMIN, ProjectRole.MEMBER],
    )

    updated_task = update_task(
        db,
        task_id,
        task,
    )

    log_activity(
        db=db,
        current_user=current_user,
        activity=ActivityLogCreate(
            action=ActivityAction.TASK_UPDATED,
            entity_type="task",
            entity_id=updated_task.id,
            description=(
                f"{current_user.username} actualizó la tarea " f'"{updated_task.title}"'
            ),
            project_id=board.project_id,
        ),
    )

    if (
        updated_task.assigned_to_id is not None
        and updated_task.assigned_to_id != current_user.id
    ):

        notify(
            db=db,
            notification=NotificationCreate(
                type=NotificationType.TASK_UPDATED,
                title="Tarea actualizada",
                message=(
                    f"{current_user.username} actualizó la tarea "
                    f'"{updated_task.title}".'
                ),
                entity_type="task",
                entity_id=updated_task.id,
                recipient_id=updated_task.assigned_to_id,
                sender_id=current_user.id,
                project_id=board.project_id,
            ),
        )

    if (
        previous_assigned != updated_task.assigned_to_id
        and updated_task.assigned_to_id is not None
    ):

        assigned_user = get_user(
            db,
            updated_task.assigned_to_id,
        )

        if assigned_user is not None:

            log_activity(
                db=db,
                current_user=current_user,
                activity=ActivityLogCreate(
                    action=ActivityAction.TASK_ASSIGNED,
                    entity_type="task",
                    entity_id=updated_task.id,
                    description=(
                        f"{current_user.username} asignó la tarea "
                        f'"{updated_task.title}" a '
                        f"{assigned_user.username}"
                    ),
                    project_id=board.project_id,
                ),
            )

            if assigned_user.id != current_user.id:

                notify(
                    db=db,
                    notification=NotificationCreate(
                        type=NotificationType.TASK_ASSIGNED,
                        title="Nueva tarea asignada",
                        message=(
                            f"{current_user.username} te asignó la tarea "
                            f'"{updated_task.title}".'
                        ),
                        entity_type="task",
                        entity_id=updated_task.id,
                        recipient_id=assigned_user.id,
                        sender_id=current_user.id,
                        project_id=board.project_id,
                    ),
                )

    if (
        previous_status != updated_task.status
        and updated_task.status == TaskStatus.DONE
    ):

        log_activity(
            db=db,
            current_user=current_user,
            activity=ActivityLogCreate(
                action=ActivityAction.TASK_COMPLETED,
                entity_type="task",
                entity_id=updated_task.id,
                description=(
                    f"{current_user.username} completó la tarea "
                    f'"{updated_task.title}"'
                ),
                project_id=board.project_id,
            ),
        )

        if (
            updated_task.assigned_to_id is not None
            and updated_task.assigned_to_id != current_user.id
        ):

            notify(
                db=db,
                notification=NotificationCreate(
                    type=NotificationType.TASK_COMPLETED,
                    title="Tarea completada",
                    message=(
                        f"{current_user.username} marcó como completada "
                        f'"{updated_task.title}".'
                    ),
                    entity_type="task",
                    entity_id=updated_task.id,
                    recipient_id=updated_task.assigned_to_id,
                    sender_id=current_user.id,
                    project_id=board.project_id,
                ),
            )

    return updated_task


def remove_task(
    db: Session,
    task_id: int,
    current_user: User,
):
    task = get_task(
        db,
        task_id,
    )

    if task is None:
        return None

    board = get_board(
        db,
        task.board_id,
    )

    require_project_role(
        db=db,
        project_id=board.project_id,
        current_user=current_user,
        allowed_roles=[ProjectRole.OWNER, ProjectRole.ADMIN, ProjectRole.MEMBER],
    )

    log_activity(
        db=db,
        current_user=current_user,
        activity=ActivityLogCreate(
            action=ActivityAction.TASK_DELETED,
            entity_type="task",
            entity_id=task.id,
            description=(
                f"{current_user.username} eliminó la tarea " f'"{task.title}"'
            ),
            project_id=board.project_id,
        ),
    )

    return delete_task(
        db,
        task_id,
    )


def assign_task_to_user(
    db: Session,
    task_id: int,
    user_id: int | None,
    current_user: User,
):
    """
    Asigna una tarea a un miembro del proyecto.
    También permite desasignarla enviando None.
    """

    db_task = get_task(
        db,
        task_id,
    )

    if db_task is None:
        raise ValueError("Task not found.")

    board = get_board(
        db,
        db_task.board_id,
    )

    if board is None:
        raise ValueError("Board not found.")

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

    if user_id is not None:

        user = get_user(
            db,
            user_id,
        )

        if user is None:
            raise ValueError("User not found.")

        membership = get_user_membership(
            db=db,
            project_id=board.project_id,
            user_id=user_id,
        )

        if membership is None:
            raise ValueError("The user is not a member of this project.")

    updated_task = assign_task(
        db=db,
        task=db_task,
        user_id=user_id,
    )

    if user_id is not None:

        assigned_user = get_user(
            db,
            user_id,
        )

        log_activity(
            db=db,
            current_user=current_user,
            activity=ActivityLogCreate(
                action=ActivityAction.TASK_ASSIGNED,
                entity_type="task",
                entity_id=updated_task.id,
                description=(
                    f"{current_user.username} asignó la tarea "
                    f'"{updated_task.title}" a '
                    f"{assigned_user.username}"
                ),
                project_id=board.project_id,
            ),
        )

        if assigned_user.id != current_user.id:

            notify(
                db=db,
                notification=NotificationCreate(
                    type=NotificationType.TASK_ASSIGNED,
                    title="Nueva tarea asignada",
                    message=(
                        f"{current_user.username} te asignó la tarea "
                        f'"{updated_task.title}".'
                    ),
                    entity_type="task",
                    entity_id=updated_task.id,
                    recipient_id=assigned_user.id,
                    sender_id=current_user.id,
                    project_id=board.project_id,
                ),
            )

    return updated_task

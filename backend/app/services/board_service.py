from sqlalchemy.orm import Session

from app.core.permissions_project_member import require_project_role
from app.crud.crud_board import (
    create_board,
    delete_board,
    get_board,
    get_boards_by_project,
    get_boards_for_user,
    update_board,
)
from app.crud.crud_project import get_project
from app.crud.crud_project_member import get_project_members
from app.enums.activity_action import ActivityAction
from app.enums.notification_type import NotificationType
from app.enums.project_role import ProjectRole
from app.models.user import User
from app.schemas.activity_log_schema import ActivityLogCreate
from app.schemas.board_schema import BoardCreate, BoardUpdate
from app.schemas.notification_schema import NotificationCreate
from app.services.activity_log_service import log_activity
from app.services.notification_service import notify


def create_new_board(
    db: Session,
    board: BoardCreate,
    owner_id: int,
    current_user: User,
):
    project = get_project(
        db,
        board.project_id,
    )

    if not project:
        raise ValueError("Project not found.")

    require_project_role(
        db=db,
        project_id=project.id,
        current_user=current_user,
        allowed_roles=[
            ProjectRole.OWNER,
            ProjectRole.ADMIN,
            ProjectRole.MEMBER,
        ],
    )

    new_board = create_board(
        db,
        board,
        owner_id,
    )

    log_activity(
        db=db,
        current_user=current_user,
        activity=ActivityLogCreate(
            action=ActivityAction.BOARD_CREATED,
            entity_type="board",
            entity_id=new_board.id,
            description=(
                f"{current_user.username} creó el tablero " f'"{new_board.title}"'
            ),
            project_id=new_board.project_id,
        ),
    )

    members = get_project_members(
        db,
        new_board.project_id,
    )

    for member in members:

        if member.user_id == current_user.id:
            continue

        notify(
            db=db,
            notification=NotificationCreate(
                type=NotificationType.BOARD_CREATED,
                title="Nuevo tablero",
                message=(
                    f"{current_user.username} creó el tablero " f'"{new_board.title}".'
                ),
                entity_type="board",
                entity_id=new_board.id,
                recipient_id=member.user_id,
                sender_id=current_user.id,
                project_id=new_board.project_id,
            ),
        )

    return new_board


def get_board_by_id(
    db: Session,
    board_id: int,
    current_user: User,
):
    board = get_board(
        db,
        board_id,
    )

    if board is None:
        return None

    require_project_role(
        db=db,
        project_id=board.project_id,
        current_user=current_user,
        allowed_roles=[
            ProjectRole.OWNER,
            ProjectRole.ADMIN,
            ProjectRole.MEMBER,
            ProjectRole.VIEWER,
        ],
    )

    return board


def get_all_boards(db: Session, current_user: User):
    return get_boards_for_user(db, current_user.id)


def get_boards_of_project(
    db: Session,
    project_id: int,
    current_user: User,
):
    require_project_role(
        db=db,
        project_id=project_id,
        current_user=current_user,
        allowed_roles=[
            ProjectRole.OWNER,
            ProjectRole.ADMIN,
            ProjectRole.MEMBER,
            ProjectRole.VIEWER,
        ],
    )

    return get_boards_by_project(
        db,
        project_id,
    )


def update_existing_board(
    db: Session,
    board_id: int,
    board: BoardUpdate,
    current_user: User,
):
    existing_board = get_board(db, board_id)

    if existing_board is None:
        return None

    require_project_role(
        db=db,
        project_id=existing_board.project_id,
        current_user=current_user,
        allowed_roles=[ProjectRole.OWNER, ProjectRole.ADMIN],
    )

    updated_board = update_board(
        db,
        board_id,
        board,
    )

    if updated_board is None:
        return None

    log_activity(
        db=db,
        current_user=current_user,
        activity=ActivityLogCreate(
            action=ActivityAction.BOARD_UPDATED,
            entity_type="board",
            entity_id=updated_board.id,
            description=(
                f"{current_user.username} actualizó el tablero "
                f'"{updated_board.title}"'
            ),
            project_id=updated_board.project_id,
        ),
    )

    members = get_project_members(
        db,
        updated_board.project_id,
    )

    for member in members:

        if member.user_id == current_user.id:
            continue

        notify(
            db=db,
            notification=NotificationCreate(
                type=NotificationType.BOARD_UPDATED,
                title="Tablero actualizado",
                message=(
                    f"{current_user.username} actualizó el tablero "
                    f'"{updated_board.title}".'
                ),
                entity_type="board",
                entity_id=updated_board.id,
                recipient_id=member.user_id,
                sender_id=current_user.id,
                project_id=updated_board.project_id,
            ),
        )

    return updated_board


def remove_board(
    db: Session,
    board_id: int,
    current_user: User,
):
    board = get_board(
        db,
        board_id,
    )

    if board is None:
        return None

    require_project_role(
        db=db,
        project_id=board.project_id,
        current_user=current_user,
        allowed_roles=[ProjectRole.OWNER, ProjectRole.ADMIN],
    )

    log_activity(
        db=db,
        current_user=current_user,
        activity=ActivityLogCreate(
            action=ActivityAction.BOARD_DELETED,
            entity_type="board",
            entity_id=board.id,
            description=(
                f"{current_user.username} eliminó el tablero " f'"{board.title}"'
            ),
            project_id=board.project_id,
        ),
    )

    return delete_board(
        db,
        board_id,
    )

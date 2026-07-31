from sqlalchemy.orm import Session

from app.crud.crud_project import get_project
from app.crud.crud_user import get_user

from app.crud.crud_project_member import (
    create_project_member,
    get_project_member,
    get_project_members,
    get_user_membership,
    update_project_member,
    delete_project_member,
)

from app.schemas.project_member_schema import (
    ProjectMemberCreate,
    ProjectMemberUpdate,
)

from app.models.user import User

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

def create_new_project_member(
    db: Session,
    project_id: int,
    member: ProjectMemberCreate,
    current_user: User,
):
    """
    Agrega un usuario a un proyecto.
    """

    project = get_project(
        db,
        project_id
    )

    if project is None:
        raise ValueError(
            "Project not found."
        )

    require_project_role(
        db=db,
        project_id=project_id,
        current_user=current_user,
        allowed_roles=[
            ProjectRole.OWNER,
        ],
    )

    user = get_user(
        db,
        member.user_id
    )

    if user is None:
        raise ValueError(
            "User not found."
        )

    existing_member = get_user_membership(
        db,
        project_id,
        member.user_id
    )

    if existing_member:
        raise ValueError(
            "The user already belongs to the project."
        )

    new_member = create_project_member(
    db=db,
    project_id=project_id,
    member=member,
    )

    log_activity(
        db=db,
        current_user=current_user,
        activity=ActivityLogCreate(
            action=ActivityAction.MEMBER_ADDED,
            entity_type="project_member",
            entity_id=new_member.id,
            description=(
                f'{current_user.username} agregó al usuario '
                f'{user.username} como {member.role.value}'
            ),
            project_id=project_id,
        ),
    )

    if user.id != current_user.id:
        notify(
            db=db,
            notification=NotificationCreate(
                type=NotificationType.MEMBER_ADDED,
                title="Has sido agregado a un proyecto",
                message=(
                    f'{current_user.username} te agregó al proyecto '
                    f'"{project.title}".'
                ),
                entity_type="project_member",
                entity_id=new_member.id,
                recipient_id=user.id,
                sender_id=current_user.id,
                project_id=project.id,
            ),
        )

    return new_member


def get_member_by_id(
    db: Session,
    member_id: int,
    current_user: User,
):
    member = get_project_member(
        db,
        member_id
    )

    if member is None:
        return None

    require_project_role(
        db=db,
        project_id=member.project_id,
        current_user=current_user,
        allowed_roles=list(ProjectRole),
    )

    return member


def get_members_of_project(
    db: Session,
    project_id: int,
    current_user: User,
):
    require_project_role(
        db=db,
        project_id=project_id,
        current_user=current_user,
        allowed_roles=list(ProjectRole),
    )

    return get_project_members(
        db,
        project_id
    )


def update_existing_project_member(
    db: Session,
    member_id: int,
    member: ProjectMemberUpdate,
    current_user: User,
):
    """
    Actualiza el rol de un miembro.
    """

    db_member = get_project_member(
        db,
        member_id,
    )

    if db_member is None:
        raise ValueError(
            "Member not found."
        )

    require_project_role(
        db=db,
        project_id=db_member.project_id,
        current_user=current_user,
        allowed_roles=[
            ProjectRole.OWNER,
        ],
    )

    updated_member = update_project_member(
        db,
        member_id,
        member,
    )

    project = get_project(
        db,
        updated_member.project_id,
    )

    log_activity(
        db=db,
        current_user=current_user,
        activity=ActivityLogCreate(
            action=ActivityAction.MEMBER_ROLE_UPDATED,
            entity_type="project_member",
            entity_id=updated_member.id,
            description=(
                f'{current_user.username} cambió el rol del usuario '
                f'{updated_member.user.username} a {updated_member.role.value}'
            ),
            project_id=updated_member.project_id,
        ),
    )

    if updated_member.user_id != current_user.id:
        notify(
            db=db,
            notification=NotificationCreate(
                type=NotificationType.ROLE_CHANGED,
                title="Tu rol ha sido actualizado",
                message=(
                    f'{current_user.username} cambió tu rol a '
                    f'{updated_member.role.value} '
                    f'en el proyecto "{project.title}".'
                ),
                entity_type="project_member",
                entity_id=updated_member.id,
                recipient_id=updated_member.user_id,
                sender_id=current_user.id,
                project_id=updated_member.project_id,
            ),
        )

    return updated_member


def remove_project_member(
    db: Session,
    member_id: int,
    current_user: User,
):
    """
    Elimina un miembro del proyecto.
    """

    db_member = get_project_member(
        db,
        member_id,
    )

    if db_member is None:
        raise ValueError(
            "Member not found."
        )

    require_project_role(
        db=db,
        project_id=db_member.project_id,
        current_user=current_user,
        allowed_roles=[
            ProjectRole.OWNER,
        ],
    )

    member_to_remove = db_member

    deleted_member = delete_project_member(
        db,
        member_id,
    )

    log_activity(
        db=db,
        current_user=current_user,
        activity=ActivityLogCreate(
            action=ActivityAction.MEMBER_REMOVED,
            entity_type="project_member",
            entity_id=member_to_remove.id,
            description=(
                f'{current_user.username} eliminó al usuario '
                f'{member_to_remove.user.username} del proyecto'
            ),
            project_id=member_to_remove.project_id,
        ),
    )

    return deleted_member

from sqlalchemy.orm import Session

from app.crud.crud_project import (
    create_project,
    get_project,
    get_projects,
    get_projects_by_owner,
    get_projects_for_user,
    update_project,
    delete_project,
)

from app.crud.crud_project_member import (
    create_project_member,
    get_project_members,
)

from app.schemas.project_schema import (
    ProjectCreate,
    ProjectUpdate,
)

from app.schemas.project_member_schema import (
    ProjectMemberCreate,
)

from app.enums.project_role import (
    ProjectRole,
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

from app.models.user import User

def create_new_project(
    db: Session,
    project: ProjectCreate,
    owner_id: int,
    current_user: User,
):
    """
    Crea un proyecto y registra automáticamente
    al creador como OWNER.
    """

    new_project = create_project(
        db=db,
        project=project,
        owner_id=owner_id,
    )

    create_project_member(
        db=db,
        project_id=new_project.id,
        member=ProjectMemberCreate(
            user_id=owner_id,
            role=ProjectRole.OWNER,
        ),
    )

    log_activity(
        db=db,
        current_user=current_user,
        activity=ActivityLogCreate(
            action=ActivityAction.PROJECT_CREATED,
            entity_type="project",
            entity_id=new_project.id,
            description=(
                f'{current_user.username} creó el proyecto '
                f'"{new_project.title}"'
            ),
            project_id=new_project.id,
        ),
    )

    return new_project

def get_project_by_id(
    db: Session,
    project_id: int
):
    return get_project(db, project_id)


def get_all_projects(db: Session):
    return get_projects(db)


def get_projects_of_user(
    db: Session,
    user_id: int,
):
    return get_projects_for_user(db, user_id)


def update_existing_project(
    db: Session,
    project_id: int,
    project: ProjectUpdate,
    current_user: User,
):
    updated_project = update_project(
        db,
        project_id,
        project,
    )

    if updated_project is None:
        return None

    log_activity(
        db=db,
        current_user=current_user,
        activity=ActivityLogCreate(
            action=ActivityAction.PROJECT_UPDATED,
            entity_type="project",
            entity_id=updated_project.id,
            description=(
                f'{current_user.username} actualizó el proyecto '
                f'"{updated_project.title}"'
            ),
            project_id=updated_project.id,
        ),
    )

    members = get_project_members(
        db,
        updated_project.id,
    )

    for member in members:

        if member.user_id == current_user.id:
            continue

        notify(
            db=db,
            notification=NotificationCreate(
                type=NotificationType.PROJECT_UPDATED,
                title="Proyecto actualizado",
                message=(
                    f'{current_user.username} actualizó el proyecto '
                    f'"{updated_project.title}".'
                ),
                entity_type="project",
                entity_id=updated_project.id,
                recipient_id=member.user_id,
                sender_id=current_user.id,
                project_id=updated_project.id,
            ),
        )

    return updated_project


def remove_project(
    db: Session,
    project_id: int,
    current_user: User,
):
    project = get_project(
        db,
        project_id,
    )

    if project is None:
        return None

    log_activity(
        db=db,
        current_user=current_user,
        activity=ActivityLogCreate(
            action=ActivityAction.PROJECT_DELETED,
            entity_type="project",
            entity_id=project.id,
            description=(
                f'{current_user.username} eliminó el proyecto '
                f'"{project.title}"'
            ),
            project_id=project.id,
        ),
    )

    return delete_project(
        db,
        project_id,
    )

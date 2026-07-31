from sqlalchemy.orm import Session

from app.crud.crud_activity_log import (
    create_activity_log,
    get_activity_log,
    get_activity_logs_by_project,
    get_activity_logs_by_user,
)
from app.models.user import User
from app.schemas.activity_log_schema import ActivityLogCreate


def log_activity(
    db: Session,
    activity: ActivityLogCreate,
    current_user: User,
):
    """
    Registra una actividad en el historial.
    """

    return create_activity_log(
        db=db,
        activity=activity,
        user_id=current_user.id,
    )


def get_activity_by_id(
    db: Session,
    activity_id: int,
):
    """
    Obtiene una actividad por su ID.
    """

    return get_activity_log(
        db,
        activity_id,
    )


def get_project_activity(
    db: Session,
    project_id: int,
):
    """
    Obtiene el historial de un proyecto.
    """

    return get_activity_logs_by_project(
        db,
        project_id,
    )


def get_user_activity(
    db: Session,
    user_id: int,
):
    """
    Obtiene el historial de un usuario.
    """

    return get_activity_logs_by_user(
        db,
        user_id,
    )

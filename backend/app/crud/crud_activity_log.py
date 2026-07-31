from sqlalchemy.orm import Session

from app.models.activity_log import ActivityLog
from app.schemas.activity_log_schema import ActivityLogCreate


def get_activity_log(
    db: Session,
    activity_id: int,
):
    """
    Obtiene una actividad por su ID.
    """

    return (
        db.query(ActivityLog)
        .filter(ActivityLog.id == activity_id)
        .first()
    )


def get_activity_logs_by_project(
    db: Session,
    project_id: int,
):
    """
    Obtiene el historial de un proyecto,
    ordenado del más reciente al más antiguo.
    """

    return (
        db.query(ActivityLog)
        .filter(ActivityLog.project_id == project_id)
        .order_by(ActivityLog.created_at.desc())
        .all()
    )


def get_activity_logs_by_user(
    db: Session,
    user_id: int,
):
    """
    Obtiene todas las actividades
    realizadas por un usuario.
    """

    return (
        db.query(ActivityLog)
        .filter(ActivityLog.user_id == user_id)
        .order_by(ActivityLog.created_at.desc())
        .all()
    )


def create_activity_log(
    db: Session,
    activity: ActivityLogCreate,
    user_id: int,
):
    """
    Registra una nueva actividad.
    """

    db_activity = ActivityLog(
        action=activity.action,
        entity_type=activity.entity_type,
        entity_id=activity.entity_id,
        description=activity.description,
        project_id=activity.project_id,
        user_id=user_id,
    )

    db.add(db_activity)
    db.commit()
    db.refresh(db_activity)

    return db_activity


def delete_activity_log(
    db: Session,
    activity_id: int,
):
    """
    Elimina un registro de actividad.
    """

    activity = get_activity_log(
        db,
        activity_id,
    )

    if activity is None:
        return None

    db.delete(activity)
    db.commit()

    return activity
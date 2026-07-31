from sqlalchemy.orm import Session

from app.crud.crud_notification import (
    create_notification,
    get_notification,
    get_notifications_by_user,
    update_notification,
    mark_all_as_read,
    delete_notification,
)

from app.schemas.notification_schema import (
    NotificationCreate,
    NotificationUpdate,
)


def notify(
    db: Session,
    notification: NotificationCreate,
):
    """
    Crea una nueva notificación.
    """

    return create_notification(
        db=db,
        notification=notification,
    )


def get_notification_by_id(
    db: Session,
    notification_id: int,
):
    """
    Obtiene una notificación por su ID.
    """

    return get_notification(
        db=db,
        notification_id=notification_id,
    )


def get_user_notifications(
    db: Session,
    user_id: int,
):
    """
    Obtiene todas las notificaciones
    de un usuario.
    """

    return get_notifications_by_user(
        db=db,
        user_id=user_id,
    )


def mark_notification_as_read(
    db: Session,
    notification_id: int,
):
    """
    Marca una notificación como leída.
    """

    return update_notification(
        db=db,
        notification_id=notification_id,
        notification=NotificationUpdate(
            is_read=True,
        ),
    )


def mark_every_notification_as_read(
    db: Session,
    user_id: int,
):
    """
    Marca todas las notificaciones
    de un usuario como leídas.
    """

    return mark_all_as_read(
        db=db,
        user_id=user_id,
    )


def remove_notification(
    db: Session,
    notification_id: int,
):
    """
    Elimina una notificación.
    """

    return delete_notification(
        db=db,
        notification_id=notification_id,
    )
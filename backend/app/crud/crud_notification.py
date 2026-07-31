from sqlalchemy.orm import Session

from app.models.notification import Notification
from app.schemas.notification_schema import NotificationCreate, NotificationUpdate


def get_notification(
    db: Session,
    notification_id: int,
):
    """
    Obtiene una notificación por su ID.
    """

    return db.query(Notification).filter(Notification.id == notification_id).first()


def get_notifications_by_user(
    db: Session,
    user_id: int,
):
    """
    Obtiene todas las notificaciones
    de un usuario.
    """

    return (
        db.query(Notification)
        .filter(Notification.recipient_id == user_id)
        .order_by(Notification.created_at.desc())
        .all()
    )


def create_notification(
    db: Session,
    notification: NotificationCreate,
):
    """
    Crea una nueva notificación.
    """

    db_notification = Notification(**notification.model_dump())

    db.add(db_notification)
    db.commit()
    db.refresh(db_notification)

    return db_notification


def update_notification(
    db: Session,
    notification_id: int,
    notification: NotificationUpdate,
):
    """
    Actualiza una notificación.
    """

    db_notification = get_notification(
        db,
        notification_id,
    )

    if db_notification is None:
        return None

    update_data = notification.model_dump(
        exclude_unset=True,
    )

    for key, value in update_data.items():
        setattr(
            db_notification,
            key,
            value,
        )

    db.commit()
    db.refresh(db_notification)

    return db_notification


def mark_all_as_read(
    db: Session,
    user_id: int,
):
    """
    Marca todas las notificaciones
    del usuario como leídas.
    """

    notifications = (
        db.query(Notification)
        .filter(Notification.recipient_id == user_id)
        .filter(Notification.is_read.is_(False))
        .all()
    )

    for notification in notifications:
        notification.is_read = True

    db.commit()

    return notifications


def delete_notification(
    db: Session,
    notification_id: int,
):
    """
    Elimina una notificación.
    """

    db_notification = get_notification(
        db,
        notification_id,
    )

    if db_notification is None:
        return None

    db.delete(db_notification)
    db.commit()

    return db_notification

from typing import List

from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
    status,
)

from sqlalchemy.orm import Session

from app.db.session import get_db

from app.models.user import User

from app.core.dependencies import (
    get_current_user,
)

from app.schemas.notification_schema import (
    NotificationResponse,
)

from app.services.notification_service import (
    get_notification_by_id,
    get_user_notifications,
    mark_notification_as_read,
    mark_every_notification_as_read,
    remove_notification,
)

router = APIRouter(
    prefix="/notifications",
    tags=["Notifications"],
)


@router.get(
    "/",
    response_model=List[NotificationResponse],
)
def read_my_notifications(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return get_user_notifications(
        db=db,
        user_id=current_user.id,
    )


@router.get(
    "/{notification_id}",
    response_model=NotificationResponse,
)
def read_notification(
    notification_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    notification = get_notification_by_id(
        db=db,
        notification_id=notification_id,
    )

    if notification is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Notification not found.",
        )

    if notification.recipient_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized.",
        )

    return notification


@router.put(
    "/{notification_id}/read",
    response_model=NotificationResponse,
)
def mark_as_read(
    notification_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    notification = get_notification_by_id(
        db=db,
        notification_id=notification_id,
    )

    if notification is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Notification not found.",
        )

    if notification.recipient_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized.",
        )

    return mark_notification_as_read(
        db=db,
        notification_id=notification_id,
    )


@router.put(
    "/read-all",
)
def mark_all_as_read(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    mark_every_notification_as_read(
        db=db,
        user_id=current_user.id,
    )

    return {
        "message": "All notifications marked as read."
    }


@router.delete(
    "/{notification_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
def delete_notification(
    notification_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    notification = get_notification_by_id(
        db=db,
        notification_id=notification_id,
    )

    if notification is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Notification not found.",
        )

    if notification.recipient_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized.",
        )

    remove_notification(
        db=db,
        notification_id=notification_id,
    )

    return None
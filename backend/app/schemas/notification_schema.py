from datetime import datetime

from pydantic import BaseModel, ConfigDict

from app.enums.notification_type import NotificationType


class NotificationBase(BaseModel):
    type: NotificationType
    title: str
    message: str
    entity_type: str
    entity_id: int
    recipient_id: int
    sender_id: int
    project_id: int


class NotificationCreate(NotificationBase):
    pass


class NotificationUpdate(BaseModel):
    is_read: bool


class NotificationResponse(NotificationBase):
    id: int
    is_read: bool
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)

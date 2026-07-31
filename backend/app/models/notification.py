from sqlalchemy import (
    Column,
    Integer,
    String,
    Boolean,
    DateTime,
    ForeignKey,
    Enum,
)

from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from app.db.base import Base
from app.enums.notification_type import NotificationType


class Notification(Base):
    __tablename__ = "notifications"

    id = Column(
        Integer,
        primary_key=True,
        index=True,
    )

    type = Column(
        Enum(NotificationType),
        nullable=False,
    )

    title = Column(
        String(150),
        nullable=False,
    )

    message = Column(
        String(500),
        nullable=False,
    )

    entity_type = Column(
        String(50),
        nullable=False,
    )

    entity_id = Column(
        Integer,
        nullable=False,
    )

    is_read = Column(
        Boolean,
        nullable=False,
        default=False,
    )

    created_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
    )

    recipient_id = Column(
        Integer,
        ForeignKey(
            "users.id",
            ondelete="CASCADE",
        ),
        nullable=False,
    )

    sender_id = Column(
        Integer,
        ForeignKey(
            "users.id",
            ondelete="CASCADE",
        ),
        nullable=False,
    )

    project_id = Column(
        Integer,
        ForeignKey(
            "projects.id",
            ondelete="CASCADE",
        ),
        nullable=False,
    )

    recipient = relationship(
        "User",
        foreign_keys=[recipient_id],
        back_populates="notifications_received",
    )

    sender = relationship(
        "User",
        foreign_keys=[sender_id],
        back_populates="notifications_sent",
    )

    project = relationship(
        "Project",
        back_populates="notifications",
    )
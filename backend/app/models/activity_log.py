from sqlalchemy import Column, DateTime, Enum, ForeignKey, Integer, String
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from app.db.base import Base
from app.enums.activity_action import ActivityAction


class ActivityLog(Base):
    __tablename__ = "activity_logs"

    id = Column(
        Integer,
        primary_key=True,
        index=True,
    )

    action = Column(
        Enum(ActivityAction),
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

    description = Column(
        String(500),
        nullable=False,
    )

    created_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
    )

    user_id = Column(
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

    user = relationship(
        "User",
        back_populates="activity_logs",
    )

    project = relationship(
        "Project",
        back_populates="activity_logs",
    )

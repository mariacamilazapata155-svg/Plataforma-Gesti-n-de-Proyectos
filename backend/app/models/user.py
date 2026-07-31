from sqlalchemy import Column, DateTime, Integer, String
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from app.db.base import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)

    username = Column(String(50), unique=True, nullable=False)

    email = Column(String(100), unique=True, nullable=False)

    hashed_password = Column(String(255), nullable=False)

    created_at = Column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )

    updated_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False,
    )

    projects = relationship(
        "Project", back_populates="owner", cascade="all, delete-orphan"
    )

    project_memberships = relationship(
        "ProjectMember", back_populates="user", cascade="all, delete-orphan"
    )

    boards = relationship("Board", back_populates="owner", cascade="all, delete-orphan")

    assigned_tasks = relationship("Task", back_populates="assigned_to")

    comments = relationship(
        "Comment", back_populates="author", cascade="all, delete-orphan"
    )

    attachments = relationship(
        "Attachment", back_populates="uploader", cascade="all, delete-orphan"
    )

    activity_logs = relationship(
        "ActivityLog",
        back_populates="user",
        cascade="all, delete-orphan",
    )

    notifications_received = relationship(
        "Notification",
        foreign_keys="Notification.recipient_id",
        back_populates="recipient",
        cascade="all, delete-orphan",
    )

    notifications_sent = relationship(
        "Notification",
        foreign_keys="Notification.sender_id",
        back_populates="sender",
    )

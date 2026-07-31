from sqlalchemy import (
    Column,
    Integer,
    String,
    DateTime,
    ForeignKey,
    Enum,
)
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from app.db.base import Base
from app.enums.project import ProjectStatus


class Project(Base):
    __tablename__ = "projects"

    id = Column(Integer, primary_key=True, index=True)

    title = Column(String(100), nullable=False)
    description = Column(String(1000), nullable=True)

    status = Column(
        Enum(ProjectStatus),
        nullable=False,
        default=ProjectStatus.PENDING
    )

    created_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False
    )

    updated_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False
    )

    finished_at = Column(
        DateTime(timezone=True),
        nullable=True
    )

    owner_id = Column(
        Integer,
        ForeignKey("users.id"),
        nullable=False
    )

    owner = relationship(
        "User",
        back_populates="projects"
    )

    boards = relationship(
        "Board",
        back_populates="project",
        cascade="all, delete-orphan"
    )

    members = relationship(
        "ProjectMember",
        back_populates="project",
        cascade="all, delete-orphan"
    )

    activity_logs = relationship(
        "ActivityLog",
        back_populates="project",
        cascade="all, delete-orphan",
    )

    notifications = relationship(
        "Notification",
        back_populates="project",
        cascade="all, delete-orphan",
    )
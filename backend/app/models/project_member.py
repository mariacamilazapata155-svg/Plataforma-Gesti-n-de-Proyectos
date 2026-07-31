from sqlalchemy import (
    Column,
    Integer,
    ForeignKey,
    Enum,
    UniqueConstraint,
    DateTime,
)

from sqlalchemy.sql import func

from sqlalchemy.orm import relationship

from app.db.base import Base
from app.enums.project_role import ProjectRole


class ProjectMember(Base):
    __tablename__ = "project_members"

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    project_id = Column(
        Integer,
        ForeignKey(
            "projects.id",
            ondelete="CASCADE"
        ),
        nullable=False
    )

    user_id = Column(
        Integer,
        ForeignKey(
            "users.id",
            ondelete="CASCADE"
        ),
        nullable=False
    )

    role = Column(
        Enum(ProjectRole),
        nullable=False,
        default=ProjectRole.MEMBER
    )

    created_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
    )

    project = relationship(
        "Project",
        back_populates="members"
    )

    user = relationship(
        "User",
        back_populates="project_memberships"
    )

    __table_args__ = (
        UniqueConstraint(
            "project_id",
            "user_id",
            name="uq_project_member"
        ),
    )
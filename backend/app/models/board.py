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
from app.enums.board import BoardStatus


class Board(Base):
    __tablename__ = "boards"

    id = Column(Integer, primary_key=True, index=True)

    title = Column(String(100), nullable=False)
    description = Column(String(1000), nullable=True)

    status = Column(
        Enum(BoardStatus),
        nullable=False,
        default=BoardStatus.ACTIVE
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

    project_id = Column(
        Integer,
        ForeignKey("projects.id"),
        nullable=False
    )

    owner_id = Column(
    Integer,
    ForeignKey("users.id"),
    nullable=False
    )

    project = relationship(
        "Project",
        back_populates="boards"
    )

    owner = relationship(
    "User",
    back_populates="boards"
    )

    tasks = relationship(
        "Task",
        back_populates="board",
        cascade="all, delete-orphan"
    )

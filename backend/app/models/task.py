from sqlalchemy import Column, DateTime, Enum, ForeignKey, Integer, String, Text
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from app.db.base import Base
from app.enums.task import TaskPriority, TaskStatus


class Task(Base):
    __tablename__ = "tasks"

    id = Column(Integer, primary_key=True, index=True)

    title = Column(String(150), nullable=False)

    description = Column(Text, nullable=True)

    status = Column(Enum(TaskStatus), nullable=False, default=TaskStatus.TODO)

    priority = Column(Enum(TaskPriority), nullable=False, default=TaskPriority.MEDIUM)

    created_at = Column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )

    updated_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False,
    )

    due_date = Column(DateTime(timezone=True), nullable=True)

    completed_at = Column(DateTime(timezone=True), nullable=True)

    board_id = Column(Integer, ForeignKey("boards.id"), nullable=False)

    assigned_to_id = Column(Integer, ForeignKey("users.id"), nullable=True)

    board = relationship("Board", back_populates="tasks")

    assigned_to = relationship("User", back_populates="assigned_tasks")

    comments = relationship(
        "Comment", back_populates="task", cascade="all, delete-orphan"
    )

    attachments = relationship(
        "Attachment", back_populates="task", cascade="all, delete-orphan"
    )

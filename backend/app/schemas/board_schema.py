from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict

from app.enums.board import BoardStatus


class BoardBase(BaseModel):
    title: str
    description: Optional[str] = None


class BoardCreate(BoardBase):
    project_id: int


class BoardUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    status: Optional[BoardStatus] = None


class BoardResponse(BoardBase):
    id: int
    status: BoardStatus

    project_id: int

    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)

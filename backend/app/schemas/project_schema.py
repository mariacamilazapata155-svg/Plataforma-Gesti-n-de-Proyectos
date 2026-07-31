from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict
from app.enums.project import ProjectStatus


class ProjectBase(BaseModel):
    title: str
    description: Optional[str] = None


class ProjectCreate(ProjectBase):
    pass


class ProjectUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    status: Optional[ProjectStatus] = None
    finished_at: Optional[datetime] = None


class ProjectResponse(ProjectBase):
    id: int
    status: ProjectStatus

    owner_id: int

    created_at: datetime
    updated_at: datetime
    finished_at: Optional[datetime] = None

    model_config = ConfigDict(from_attributes=True)
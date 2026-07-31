from datetime import datetime

from pydantic import BaseModel, ConfigDict

from app.enums.project_role import ProjectRole


class ProjectMemberBase(BaseModel):
    user_id: int
    role: ProjectRole


class ProjectMemberCreate(ProjectMemberBase):
    pass


class ProjectMemberUpdate(BaseModel):
    role: ProjectRole


class ProjectMemberResponse(ProjectMemberBase):
    id: int
    project_id: int
    created_at: datetime

    model_config = ConfigDict(
        from_attributes=True
    )
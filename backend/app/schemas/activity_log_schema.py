from datetime import datetime

from pydantic import BaseModel, ConfigDict

from app.enums.activity_action import ActivityAction


class ActivityLogBase(BaseModel):
    action: ActivityAction
    entity_type: str
    entity_id: int
    description: str
    project_id: int


class ActivityLogCreate(ActivityLogBase):
    pass


class ActivityLogResponse(ActivityLogBase):
    id: int
    user_id: int
    created_at: datetime

    model_config = ConfigDict(
        from_attributes=True
    )
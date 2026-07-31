from datetime import datetime

from pydantic import BaseModel, ConfigDict


class AttachmentBase(BaseModel):
    filename: str
    original_filename: str
    content_type: str
    file_size: int
    storage_path: str
    task_id: int
    uploaded_by: int


class AttachmentResponse(AttachmentBase):
    id: int
    uploaded_at: datetime

    model_config = ConfigDict(from_attributes=True)

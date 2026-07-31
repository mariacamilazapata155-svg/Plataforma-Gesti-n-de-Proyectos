from typing import List

from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
    status,
)

from sqlalchemy.orm import Session

from app.db.session import get_db

from app.schemas.activity_log_schema import (
    ActivityLogResponse,
)

from app.services.activity_log_service import (
    get_activity_by_id,
    get_project_activity,
    get_user_activity,
)

from app.models.user import User

from app.core.dependencies import get_current_user
from app.core.permissions_project_member import require_project_role
from app.enums.project_role import ProjectRole

router = APIRouter(
    prefix="/activity-logs",
    tags=["Activity Logs"],
)


@router.get(
    "/{activity_id}",
    response_model=ActivityLogResponse,
)
def read_activity(
    activity_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    activity = get_activity_by_id(
        db,
        activity_id,
    )

    if activity is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Activity not found.",
        )

    require_project_role(
        db=db,
        project_id=activity.project_id,
        current_user=current_user,
        allowed_roles=list(ProjectRole),
    )

    return activity


@router.get(
    "/projects/{project_id}",
    response_model=List[ActivityLogResponse],
)
def read_project_activity(
    project_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    require_project_role(
        db=db,
        project_id=project_id,
        current_user=current_user,
        allowed_roles=list(ProjectRole),
    )

    return get_project_activity(
        db,
        project_id,
    )


@router.get(
    "/users/{user_id}",
    response_model=List[ActivityLogResponse],
)
def read_user_activity(
    user_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    if user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You can only access your own activity.",
        )

    return get_user_activity(
        db,
        user_id,
    )

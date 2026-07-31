from typing import List

from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
    status,
)
from sqlalchemy.orm import Session

from app.db.session import get_db

from app.models.user import User

from app.core.dependencies import (
    get_current_user,
)

from app.schemas.project_member_schema import (
    ProjectMemberCreate,
    ProjectMemberUpdate,
    ProjectMemberResponse,
)

from app.services.project_member_service import (
    create_new_project_member,
    get_member_by_id,
    get_members_of_project,
    update_existing_project_member,
    remove_project_member,
)

router = APIRouter(
    prefix="/project-members",
    tags=["Project Members"],
)

@router.post(
    "/projects/{project_id}",
    response_model=ProjectMemberResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_project_member(
    project_id: int,
    member: ProjectMemberCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    try:
        return create_new_project_member(
            db=db,
            project_id=project_id,
            member=member,
            current_user=current_user,
        )

    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e),
        )
    
@router.get(
    "/projects/{project_id}",
    response_model=List[ProjectMemberResponse],
)
def read_project_members(
    project_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return get_members_of_project(
        db,
        project_id,
        current_user,
    )

@router.get(
    "/{member_id}",
    response_model=ProjectMemberResponse,
)
def read_project_member(
    member_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    member = get_member_by_id(
        db,
        member_id,
        current_user,
    )

    if member is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Member not found.",
        )

    return member

@router.put(
    "/{member_id}",
    response_model=ProjectMemberResponse,
)
def update_project_member(
    member_id: int,
    member: ProjectMemberUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    updated = update_existing_project_member(
        db=db,
        member_id=member_id,
        member=member,
        current_user=current_user,
    )

    if updated is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Member not found.",
        )

    return updated

@router.delete(
    "/{member_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
def delete_project_member(
    member_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    deleted = remove_project_member(
        db=db,
        member_id=member_id,
        current_user=current_user,
    )

    if deleted is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Member not found.",
        )

    return None


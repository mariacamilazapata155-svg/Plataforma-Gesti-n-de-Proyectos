from typing import List

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.core.dependencies import get_current_user
from app.core.permissions import verify_project_owner
from app.core.permissions_project_member import require_project_role
from app.db.session import get_db
from app.enums.project_role import ProjectRole
from app.models.user import User
from app.schemas.project_schema import ProjectCreate, ProjectResponse, ProjectUpdate
from app.services.project_service import (
    create_new_project,
    get_project_by_id,
    get_projects_of_user,
    remove_project,
    update_existing_project,
)

router = APIRouter(prefix="/projects", tags=["Projects"])


@router.post("/", response_model=ProjectResponse, status_code=status.HTTP_201_CREATED)
def create_project(
    project: ProjectCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return create_new_project(
        db=db,
        project=project,
        owner_id=current_user.id,
        current_user=current_user,
    )


@router.get("/", response_model=List[ProjectResponse])
def read_projects(
    db: Session = Depends(get_db), current_user: User = Depends(get_current_user)
):
    return get_projects_of_user(db, current_user.id)


@router.get("/{project_id}", response_model=ProjectResponse)
def read_project(
    project_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    project = get_project_by_id(db, project_id)

    if not project:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Project not found."
        )

    require_project_role(
        db=db,
        project_id=project.id,
        current_user=current_user,
        allowed_roles=list(ProjectRole),
    )

    return project


@router.get("/owner/{owner_id}", response_model=List[ProjectResponse])
def read_projects_by_owner(
    owner_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    if owner_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You can only list your own projects.",
        )

    return get_projects_of_user(db, owner_id)


@router.put("/{project_id}", response_model=ProjectResponse)
def update_project(
    project_id: int,
    project: ProjectUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    db_project = get_project_by_id(db, project_id)

    if not db_project:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Project not found."
        )

    verify_project_owner(current_user=current_user, project=db_project)

    return update_existing_project(
        db=db,
        project_id=project_id,
        project=project,
        current_user=current_user,
    )


@router.delete("/{project_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_project(
    project_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    db_project = get_project_by_id(db, project_id)

    if not db_project:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Project not found."
        )

    verify_project_owner(current_user=current_user, project=db_project)

    remove_project(
        db=db,
        project_id=project_id,
        current_user=current_user,
    )

    return None

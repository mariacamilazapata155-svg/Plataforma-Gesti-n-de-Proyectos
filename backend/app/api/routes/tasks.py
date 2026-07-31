from typing import List

from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
    status,
)
from sqlalchemy.orm import Session

from app.db.session import get_db

from app.schemas.task_schema import (
    TaskCreate,
    TaskUpdate,
    TaskResponse,
)

from app.services.task_service import (
    create_new_task,
    get_task_by_id,
    get_all_tasks,
    get_tasks_of_board,
    update_existing_task,
    remove_task,
    assign_task_to_user,
)

from app.models.user import User
from app.core.dependencies import get_current_user

router = APIRouter(
    prefix="/tasks",
    tags=["Tasks"],
)


@router.post(
    "/",
    response_model=TaskResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_task(
    task: TaskCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    try:
        return create_new_task(
            db=db,
            task=task,
            current_user=current_user,
        )

    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e),
        )


@router.get(
    "/",
    response_model=List[TaskResponse],
)
def read_tasks(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return get_all_tasks(db, current_user)


@router.get(
    "/{task_id}",
    response_model=TaskResponse,
)
def read_task(
    task_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    task = get_task_by_id(
        db,
        task_id,
        current_user,
    )

    if task is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found.",
        )

    return task


@router.get(
    "/board/{board_id}",
    response_model=List[TaskResponse],
)
def read_tasks_by_board(
    board_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    try:
        return get_tasks_of_board(db, board_id, current_user)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))


@router.put(
    "/{task_id}",
    response_model=TaskResponse,
)
def update_task(
    task_id: int,
    task: TaskUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    updated = update_existing_task(
        db=db,
        task_id=task_id,
        task=task,
        current_user=current_user,
    )

    if updated is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found.",
        )

    return updated


@router.delete(
    "/{task_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
def delete_task(
    task_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    deleted = remove_task(
        db=db,
        task_id=task_id,
        current_user=current_user,
    )

    if deleted is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found.",
        )

    return None

@router.patch(
    "/{task_id}/assign/{user_id}",
    response_model=TaskResponse,
)
def assign_user_to_task(
    task_id: int,
    user_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """
    Asigna una tarea a un miembro del proyecto.
    """

    try:
        return assign_task_to_user(
            db=db,
            task_id=task_id,
            user_id=user_id,
            current_user=current_user,
        )

    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e),
        )
    
@router.patch(
    "/{task_id}/unassign",
    response_model=TaskResponse,
)
def unassign_task(
    task_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """
    Elimina el responsable de una tarea.
    """

    try:
        return assign_task_to_user(
            db=db,
            task_id=task_id,
            user_id=None,
            current_user=current_user,
        )

    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e),
        )    

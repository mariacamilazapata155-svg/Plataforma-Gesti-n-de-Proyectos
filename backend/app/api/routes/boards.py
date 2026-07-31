from typing import List

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.db.session import get_db

from app.schemas.board_schema import (
    BoardCreate,
    BoardUpdate,
    BoardResponse
)

from app.services.board_service import (
    create_new_board,
    get_board_by_id,
    get_all_boards,
    get_boards_of_project,
    update_existing_board,
    remove_board,
)

from app.models.user import User
from app.core.dependencies import get_current_user


router = APIRouter(
    prefix="/boards",
    tags=["Boards"]
)


@router.post(
    "/",
    response_model=BoardResponse,
    status_code=status.HTTP_201_CREATED
)
def create_board(
    board: BoardCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    try:
        return create_new_board(
            db=db,
            board=board,
            owner_id=current_user.id,
            current_user=current_user
        )

    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)
        )

@router.get("/", response_model=List[BoardResponse])
def read_boards(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return get_all_boards(db, current_user)


@router.get(
    "/{board_id}",
    response_model=BoardResponse
)
def read_board(
    board_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    board = get_board_by_id(
        db=db,
        board_id=board_id,
        current_user=current_user,
    )

    if board is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Board not found."
        )

    return board

@router.get(
    "/project/{project_id}",
    response_model=List[BoardResponse]
)
def read_boards_by_project(
    project_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return get_boards_of_project(
        db=db,
        project_id=project_id,
        current_user=current_user,
    )


@router.put(
    "/{board_id}",
    response_model=BoardResponse
)
def update_board(
    board_id: int,
    board: BoardUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    updated_board = update_existing_board(
        db=db,
        board_id=board_id,
        board=board,
        current_user=current_user,
    )

    if updated_board is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Board not found."
        )

    return updated_board


@router.delete(
    "/{board_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
def delete_board(
    board_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    deleted = remove_board(
        db=db,
        board_id=board_id,
        current_user=current_user,
    )

    if deleted is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Board not found."
        )

    return None

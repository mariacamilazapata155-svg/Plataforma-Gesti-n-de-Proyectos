from fastapi import HTTPException, status

from app.models.board import Board
from app.models.user import User


def verify_board_owner(current_user: User, board: Board):
    """
    Verifica que el usuario autenticado sea
    el propietario del board.
    """

    if board.owner_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="No tienes permisos para acceder a este board.",
        )

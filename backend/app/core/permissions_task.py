from fastapi import HTTPException, status

from app.models.user import User
from app.models.task import Task


def verify_task_owner(
    current_user: User,
    task: Task
):
    """
    Verifica que el usuario autenticado
    sea propietario de la tarea.
    """

    board = task.board

    if board.owner_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="No tienes permisos para acceder a esta tarea."
        )
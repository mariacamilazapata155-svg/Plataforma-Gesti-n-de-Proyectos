from fastapi import HTTPException, status

from app.models.project import Project
from app.models.user import User


def verify_project_owner(current_user: User, project: Project) -> None:
    """
    Verifica que el usuario autenticado
    sea el propietario del proyecto.
    """

    if project.owner_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="No tienes permisos para acceder a este proyecto.",
        )

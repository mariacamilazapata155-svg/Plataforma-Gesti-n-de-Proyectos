from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.models.user import User

from app.enums.project_role import ProjectRole

from app.crud.crud_project_member import (
    get_user_membership,
)


def get_project_membership(
    db: Session,
    project_id: int,
    current_user: User,
):
    """
    Obtiene la membresía del usuario
    dentro del proyecto.
    """

    membership = get_user_membership(
        db=db,
        project_id=project_id,
        user_id=current_user.id,
    )

    if membership is None:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You are not a member of this project.",
        )

    return membership


def require_project_role(
    db: Session,
    project_id: int,
    current_user: User,
    allowed_roles: list[ProjectRole],
):
    """
    Verifica que el usuario tenga
    alguno de los roles permitidos.
    """

    membership = get_project_membership(
        db=db,
        project_id=project_id,
        current_user=current_user,
    )

    if membership.role not in allowed_roles:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You do not have permission for this action.",
        )

    return membership
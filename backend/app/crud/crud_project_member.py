from sqlalchemy.orm import Session

from app.models.project_member import ProjectMember
from app.schemas.project_member_schema import (
    ProjectMemberCreate,
    ProjectMemberUpdate,
)


def get_project_member(
    db: Session,
    member_id: int
):
    """
    Obtiene una membresía por su ID.
    """

    return (
        db.query(ProjectMember)
        .filter(ProjectMember.id == member_id)
        .first()
    )


def get_project_members(
    db: Session,
    project_id: int
):
    """
    Obtiene todos los miembros de un proyecto.
    """

    return (
        db.query(ProjectMember)
        .filter(ProjectMember.project_id == project_id)
        .all()
    )


def get_user_membership(
    db: Session,
    project_id: int,
    user_id: int
):
    """
    Obtiene la membresía de un usuario
    dentro de un proyecto.
    """

    return (
        db.query(ProjectMember)
        .filter(
            ProjectMember.project_id == project_id,
            ProjectMember.user_id == user_id
        )
        .first()
    )


def create_project_member(
    db: Session,
    project_id: int,
    member: ProjectMemberCreate
):
    """
    Agrega un usuario al proyecto.
    """

    db_member = ProjectMember(
        project_id=project_id,
        user_id=member.user_id,
        role=member.role,
    )

    db.add(db_member)
    db.commit()
    db.refresh(db_member)

    return db_member


def update_project_member(
    db: Session,
    member_id: int,
    member: ProjectMemberUpdate
):
    """
    Actualiza el rol de un miembro.
    """

    db_member = get_project_member(
        db,
        member_id
    )

    if not db_member:
        return None

    update_data = member.model_dump(
        exclude_unset=True
    )

    for key, value in update_data.items():
        setattr(
            db_member,
            key,
            value
        )

    db.commit()
    db.refresh(db_member)

    return db_member


def delete_project_member(
    db: Session,
    member_id: int
):
    """
    Elimina un miembro del proyecto.
    """

    db_member = get_project_member(
        db,
        member_id
    )

    if not db_member:
        return None

    db.delete(db_member)
    db.commit()

    return db_member
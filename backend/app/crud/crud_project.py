from sqlalchemy.orm import Session

from app.models.project import Project
from app.models.project_member import ProjectMember
from app.schemas.project_schema import ProjectCreate, ProjectUpdate


def get_project(db: Session, project_id: int):
    """Obtiene un proyecto por su ID."""
    return db.query(Project).filter(Project.id == project_id).first()


def get_projects(db: Session, skip: int = 0, limit: int = 100):
    """Obtiene todos los proyectos."""
    return db.query(Project).offset(skip).limit(limit).all()


def get_projects_by_owner(db: Session, owner_id: int):
    """Obtiene todos los proyectos de un usuario."""
    return db.query(Project).filter(Project.owner_id == owner_id).all()


def get_projects_for_user(db: Session, user_id: int):
    """Obtiene los proyectos en los que el usuario es miembro."""
    return (
        db.query(Project)
        .join(ProjectMember, ProjectMember.project_id == Project.id)
        .filter(ProjectMember.user_id == user_id)
        .all()
    )


def create_project(db: Session, project: ProjectCreate, owner_id: int):
    """Crea un nuevo proyecto."""

    db_project = Project(
        title=project.title, description=project.description, owner_id=owner_id
    )

    db.add(db_project)
    db.commit()
    db.refresh(db_project)

    return db_project


def update_project(db: Session, project_id: int, project: ProjectUpdate):
    """Actualiza un proyecto."""

    db_project = get_project(db, project_id)

    if not db_project:
        return None

    update_data = project.model_dump(exclude_unset=True)

    for key, value in update_data.items():
        setattr(db_project, key, value)

    db.commit()
    db.refresh(db_project)

    return db_project


def delete_project(db: Session, project_id: int):
    """Elimina un proyecto."""

    db_project = get_project(db, project_id)

    if not db_project:
        return None

    db.delete(db_project)
    db.commit()

    return db_project

from sqlalchemy.orm import Session

from app.models.board import Board
from app.models.project_member import ProjectMember
from app.models.task import Task
from app.schemas.task_schema import TaskCreate, TaskUpdate


def get_task(db: Session, task_id: int):
    """Obtiene una tarea por su ID."""
    return db.query(Task).filter(Task.id == task_id).first()


def get_tasks(db: Session, skip: int = 0, limit: int = 100):
    """Obtiene todas las tareas."""
    return db.query(Task).offset(skip).limit(limit).all()


def get_tasks_by_board(db: Session, board_id: int):
    """Obtiene todas las tareas de un board."""
    return db.query(Task).filter(Task.board_id == board_id).all()


def get_tasks_for_user(db: Session, user_id: int):
    """Obtiene tareas de proyectos a los que pertenece el usuario."""
    return (
        db.query(Task)
        .join(Board, Board.id == Task.board_id)
        .join(ProjectMember, ProjectMember.project_id == Board.project_id)
        .filter(ProjectMember.user_id == user_id)
        .all()
    )


def create_task(db: Session, task: TaskCreate):
    """Crea una nueva tarea."""

    db_task = Task(
        title=task.title,
        description=task.description,
        board_id=task.board_id,
        priority=task.priority,
    )

    db.add(db_task)
    db.commit()
    db.refresh(db_task)

    return db_task


def update_task(db: Session, task_id: int, task: TaskUpdate):
    """Actualiza una tarea."""

    db_task = get_task(db, task_id)

    if not db_task:
        return None

    update_data = task.model_dump(exclude_unset=True)

    for key, value in update_data.items():
        setattr(db_task, key, value)

    db.commit()
    db.refresh(db_task)

    return db_task


def delete_task(db: Session, task_id: int):
    """Elimina una tarea."""

    db_task = get_task(db, task_id)

    if not db_task:
        return None

    db.delete(db_task)
    db.commit()

    return db_task


def assign_task(
    db: Session,
    task: Task,
    user_id: int | None,
):
    """
    Asigna una tarea a un usuario.
    Si user_id es None, desasigna la tarea.
    """

    task.assigned_to_id = user_id

    db.commit()
    db.refresh(task)

    return task

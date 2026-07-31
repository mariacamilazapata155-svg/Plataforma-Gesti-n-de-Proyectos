from sqlalchemy.orm import Session

from app.models.board import Board
from app.models.project_member import ProjectMember
from app.schemas.board_schema import BoardCreate, BoardUpdate


def get_board(db: Session, board_id: int):
    """Obtiene un board por su ID."""
    return db.query(Board).filter(Board.id == board_id).first()


def get_boards(db: Session, skip: int = 0, limit: int = 100):
    """Obtiene todos los boards."""
    return db.query(Board).offset(skip).limit(limit).all()


def get_boards_by_project(db: Session, project_id: int):
    """Obtiene todos los boards de un proyecto."""
    return db.query(Board).filter(Board.project_id == project_id).all()


def get_boards_for_user(db: Session, user_id: int):
    """Obtiene tableros pertenecientes a proyectos del usuario."""
    return (
        db.query(Board)
        .join(ProjectMember, ProjectMember.project_id == Board.project_id)
        .filter(ProjectMember.user_id == user_id)
        .all()
    )


def create_board(db: Session, board: BoardCreate, owner_id: int):
    """Crea un nuevo board."""

    db_board = Board(
        title=board.title,
        description=board.description,
        project_id=board.project_id,
        owner_id=owner_id
    )

    db.add(db_board)
    db.commit()
    db.refresh(db_board)

    return db_board


def update_board(
    db: Session,
    board_id: int,
    board: BoardUpdate
):
    """Actualiza un board."""

    db_board = get_board(db, board_id)

    if not db_board:
        return None

    update_data = board.model_dump(exclude_unset=True)

    for key, value in update_data.items():
        setattr(db_board, key, value)

    db.commit()
    db.refresh(db_board)

    return db_board


def delete_board(db: Session, board_id: int):
    """Elimina un board."""

    db_board = get_board(db, board_id)

    if not db_board:
        return None

    db.delete(db_board)
    db.commit()

    return db_board

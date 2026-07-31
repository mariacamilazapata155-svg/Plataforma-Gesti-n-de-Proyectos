from sqlalchemy.orm import Session

from app.models.comment import Comment
from app.schemas.comment_schema import (
    CommentCreate,
    CommentUpdate,
)


def get_comment(
    db: Session,
    comment_id: int
):
    """
    Obtiene un comentario por su ID.
    """

    return (
        db.query(Comment)
        .filter(Comment.id == comment_id)
        .first()
    )


def get_comments_by_task(
    db: Session,
    task_id: int
):
    """
    Obtiene todos los comentarios
    de una tarea.
    """

    return (
        db.query(Comment)
        .filter(Comment.task_id == task_id)
        .order_by(Comment.created_at.asc())
        .all()
    )


def create_comment(
    db: Session,
    comment: CommentCreate,
    author_id: int,
):
    """
    Crea un comentario.
    """

    db_comment = Comment(
        content=comment.content,
        task_id=comment.task_id,
        author_id=author_id,
    )

    db.add(db_comment)
    db.commit()
    db.refresh(db_comment)

    return db_comment


def update_comment(
    db: Session,
    comment_id: int,
    comment: CommentUpdate,
):
    """
    Actualiza un comentario.
    """

    db_comment = get_comment(
        db,
        comment_id,
    )

    if not db_comment:
        return None

    update_data = comment.model_dump(
        exclude_unset=True
    )

    for key, value in update_data.items():
        setattr(
            db_comment,
            key,
            value,
        )

    db.commit()
    db.refresh(db_comment)

    return db_comment


def delete_comment(
    db: Session,
    comment_id: int,
):
    """
    Elimina un comentario.
    """

    db_comment = get_comment(
        db,
        comment_id,
    )

    if not db_comment:
        return None

    db.delete(db_comment)
    db.commit()

    return db_comment
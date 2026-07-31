from sqlalchemy.orm import Session

from app.models.attachment import Attachment


def get_attachment(
    db: Session,
    attachment_id: int,
):
    """
    Obtiene un archivo por su ID.
    """

    return db.query(Attachment).filter(Attachment.id == attachment_id).first()


def get_attachments_by_task(
    db: Session,
    task_id: int,
):
    """
    Obtiene todos los archivos
    de una tarea.
    """

    return db.query(Attachment).filter(Attachment.task_id == task_id).all()


def create_attachment(
    db: Session,
    attachment: Attachment,
):
    """
    Guarda un archivo en la base
    de datos.
    """

    db.add(attachment)
    db.commit()
    db.refresh(attachment)

    return attachment


def delete_attachment(
    db: Session,
    attachment_id: int,
):
    """
    Elimina un archivo de la base
    de datos.
    """

    attachment = get_attachment(
        db,
        attachment_id,
    )

    if attachment is None:
        return None

    db.delete(attachment)
    db.commit()

    return attachment

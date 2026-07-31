from sqlalchemy.orm import Session

from app.models.user import User
from app.schemas.user_schema import UserCreate, UserUpdate


def get_user(db: Session, user_id: int):
    """Obtiene un usuario por su ID."""
    return db.query(User).filter(User.id == user_id).first()


def get_user_by_email(db: Session, email: str):
    """Obtiene un usuario por su correo electrónico."""
    return db.query(User).filter(User.email == email).first()


def get_user_by_username(db: Session, username: str):
    """Obtiene un usuario por su nombre de usuario."""
    return db.query(User).filter(User.username == username).first()


def get_users(db: Session, skip: int = 0, limit: int = 100):
    """Obtiene una lista de usuarios."""
    return db.query(User).offset(skip).limit(limit).all()


def create_user(db: Session, user: UserCreate, hashed_password: str):
    """Crea un nuevo usuario."""

    db_user = User(
        username=user.username, email=user.email, hashed_password=hashed_password
    )

    db.add(db_user)
    db.commit()
    db.refresh(db_user)

    return db_user


def update_user(
    db: Session,
    user_id: int,
    user: UserUpdate,
    hashed_password: str | None = None,
):
    """Actualiza un usuario."""

    db_user = get_user(db, user_id)

    if not db_user:
        return None

    update_data = user.model_dump(exclude_unset=True)

    if hashed_password is not None:
        update_data["hashed_password"] = hashed_password

    for key, value in update_data.items():
        setattr(db_user, key, value)

    db.commit()
    db.refresh(db_user)

    return db_user


def delete_user(db: Session, user_id: int):
    """Elimina un usuario."""

    db_user = get_user(db, user_id)

    if not db_user:
        return None

    db.delete(db_user)
    db.commit()

    return db_user

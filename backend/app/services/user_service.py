from sqlalchemy.orm import Session

from app.crud.crud_user import (
    get_user_by_email,
    get_user_by_username,
    create_user,
    get_user,
    get_users,
    update_user,
    delete_user,
)

from app.schemas.user_schema import UserCreate, UserUpdate
from app.core.security import hash_password


def create_new_user(db: Session, user: UserCreate):

    if get_user_by_email(db, user.email):
        raise ValueError("Email already exists.")

    if get_user_by_username(db, user.username):
        raise ValueError("Username already exists.")

    hashed_password = hash_password(user.password)

    return create_user(
        db=db,
        user=user,
        hashed_password=hashed_password
    )


def get_user_by_id(db: Session, user_id: int):
    return get_user(db, user_id)


def get_all_users(db: Session):
    return get_users(db)


def update_existing_user(
    db: Session,
    user_id: int,
    user: UserUpdate
):
    update_data = user.model_dump(exclude_unset=True)
    password = update_data.pop("password", None)

    if "email" in update_data:
        existing_user = get_user_by_email(db, update_data["email"])
        if existing_user and existing_user.id != user_id:
            raise ValueError("Email already exists.")

    if "username" in update_data:
        existing_user = get_user_by_username(db, update_data["username"])
        if existing_user and existing_user.id != user_id:
            raise ValueError("Username already exists.")

    return update_user(
        db,
        user_id,
        UserUpdate(**update_data),
        hashed_password=hash_password(password) if password is not None else None,
    )


def remove_user(db: Session, user_id: int):
    return delete_user(db, user_id)

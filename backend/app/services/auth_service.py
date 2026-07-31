from sqlalchemy.orm import Session

from app.core.security import create_access_token, hash_password, verify_password
from app.crud.crud_user import create_user, get_user_by_email, get_user_by_username
from app.schemas.auth import RegisterRequest


def register_user(db: Session, user_data: RegisterRequest):
    """
    Registra un nuevo usuario.
    """

    existing_email = get_user_by_email(db, user_data.email)

    if existing_email:
        raise ValueError("El correo ya está registrado")

    existing_username = get_user_by_username(db, user_data.username)

    if existing_username:
        raise ValueError("El nombre de usuario ya existe")

    hashed_password = hash_password(user_data.password)

    return create_user(db=db, user=user_data, hashed_password=hashed_password)


def authenticate_user(db: Session, email: str, password: str):
    """
    Valida las credenciales.
    """

    user = get_user_by_email(db, email)

    if not user:
        return None

    if not verify_password(password, user.hashed_password):
        return None

    return user


def login_user(db: Session, email: str, password: str):
    """
    Genera un JWT para un usuario válido.
    """

    user = authenticate_user(db, email, password)

    if not user:
        raise ValueError("Credenciales inválidas")

    access_token = create_access_token(subject=user.id)

    return {
        "access_token": access_token,
        "token_type": "bearer",  # nosec B105
    }

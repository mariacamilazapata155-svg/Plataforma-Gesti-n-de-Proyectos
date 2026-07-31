from datetime import datetime, timedelta, timezone
from typing import Any

from jose import JWTError, jwt
from passlib.context import CryptContext

from app.core.config import settings


pwd_context = CryptContext(
    schemes=["bcrypt"],
    deprecated="auto"
)


def hash_password(password: str) -> str:
    """
    Genera el hash de una contraseña.
    """
    return pwd_context.hash(password)


def verify_password(
    plain_password: str,
    hashed_password: str
) -> bool:
    """
    Verifica una contraseña contra su hash.
    """
    return pwd_context.verify(
        plain_password,
        hashed_password
    )


def create_access_token(
    subject: str | Any,
    expires_delta: timedelta | None = None
) -> str:
    """
    Genera un JWT.
    """

    if expires_delta:
        expire = datetime.now(
            timezone.utc
        ) + expires_delta
    else:
        expire = datetime.now(
            timezone.utc
        ) + timedelta(
            minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES
        )

    payload = {
        "sub": str(subject),
        "exp": expire
    }

    return jwt.encode(
        payload,
        settings.SECRET_KEY,
        algorithm=settings.ALGORITHM
    )


def decode_token(token: str) -> dict:
    """
    Decodifica y valida un JWT.
    """

    try:
        payload = jwt.decode(
            token,
            settings.SECRET_KEY,
            algorithms=[settings.ALGORITHM]
        )

        return payload

    except JWTError:
        raise JWTError("Token inválido")
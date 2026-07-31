from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from fastapi.security import OAuth2PasswordRequestForm

from app.db.session import get_db
from app.schemas.auth import (
    RegisterRequest,
    LoginRequest,
    TokenResponse
)
from app.schemas.user_schema import UserResponse
from app.services.auth_service import (
    register_user,
    login_user
)
from app.core.dependencies import get_current_user
from app.models.user import User


router = APIRouter(
    prefix="/auth",
    tags=["Auth"]
)


@router.post(
    "/register",
    response_model=UserResponse,
    status_code=status.HTTP_201_CREATED
)
def register(
    user_data: RegisterRequest,
    db: Session = Depends(get_db)
) -> UserResponse:
    """
    Registro de usuarios.
    """

    try:
        return register_user(
            db=db,
            user_data=user_data
        )

    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )


@router.post(
    "/login",
    response_model=TokenResponse
)
def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db)
) -> TokenResponse:
    """
    Inicio de sesión.
    """

    try:
        return login_user(
            db=db,
            email=form_data.username,
            password=form_data.password
        )

    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=str(e)
        )


@router.get(
    "/me",
    response_model=UserResponse
)
def get_me(
    current_user: User = Depends(get_current_user)
) -> UserResponse:
    """
    Obtiene el usuario autenticado.
    """

    return current_user
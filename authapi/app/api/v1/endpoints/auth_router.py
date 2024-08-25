from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi.security import OAuth2PasswordRequestForm
from app.services.auth_service import AuthService
from app.repositories.auth_repository import AuthRepository
from app.core.db import get_db
from app.schemas.user_auth import UserAuthCreate, UserAuthLogin, UserAuthResponse, Token

router = APIRouter()

async def get_auth_service(db: AsyncSession = Depends(get_db)) -> AuthService:
    auth_repo = AuthRepository(db)
    return AuthService(auth_repo)


@router.post("/login", response_model=Token)
async def login_for_access_token(
    form_data: OAuth2PasswordRequestForm = Depends(),
    auth_service: AuthService = Depends(get_auth_service)
):
    """Эндпоинт для логина и получения JWT токена."""
    user_login = UserAuthLogin(username=form_data.username, password=form_data.password)
    user = await auth_service.authenticate_user(user_login)  # Асинхронный вызов
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token = await auth_service.create_access_token_for_user(user)  # Асинхронный вызов
    return access_token

@router.post("/register", response_model=UserAuthResponse)
async def register_user(
    user_create: UserAuthCreate,
    auth_service: AuthService = Depends(get_auth_service)
):
    """Эндпоинт для регистрации нового пользователя."""
    user = await auth_service.create_user(user_create)  # Асинхронный вызов
    return user

@router.post("/change-password", response_model=UserAuthResponse)
async def change_password(
    user_id: str,
    new_password: str,
    auth_service: AuthService = Depends(get_auth_service)
):
    """Эндпоинт для изменения пароля пользователя."""
    user = await auth_service.change_user_password(user_id, new_password)  # Асинхронный вызов
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    return user

@router.delete("/delete-user")
async def delete_user(
    user_id: str,
    auth_service: AuthService = Depends(get_auth_service)
):
    """Эндпоинт для мягкого удаления пользователя."""
    user = await auth_service.delete_user(user_id)  # Асинхронный вызов
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    return {"detail": "User deleted successfully"}

from sqlalchemy.ext.asyncio import AsyncSession
from app.core.security import verify_password, get_password_hash, create_access_token
from app.repositories.auth_repository import AuthRepository
from app.schemas.user_auth import UserAuthCreate, UserAuthLogin, UserAuthResponse, Token

class AuthService:
    def __init__(self, db: AsyncSession):
        self.user_repo = AuthRepository(db)

    async def authenticate_user(self, user_login: UserAuthLogin) -> UserAuthResponse:
        """Аутентификация пользователя."""
        user = await self.user_repo.get_by_username(user_login.username)
        if user and verify_password(user_login.password, user.hashed_password):
            return UserAuthResponse.from_orm(user)
        return None

    async def create_user(self, user_create: UserAuthCreate) -> UserAuthResponse:
        """Создание нового пользователя."""
        hashed_password = get_password_hash(user_create.password)
        user_data = UserAuthCreate(
            username=user_create.username,
            email=user_create.email,
            password=hashed_password  # Хешированный пароль передается в репозиторий
        )
        user = await self.user_repo.create(user_data)
        return UserAuthResponse.from_orm(user)

    async def create_access_token_for_user(self, user: UserAuthResponse) -> Token:
        """Создание JWT токена для пользователя."""
        access_token = create_access_token(data={"sub": user.username})
        return Token(access_token=access_token)

    async def change_user_password(self, user_id: str, new_password: str) -> UserAuthResponse:
        """Смена пароля пользователя."""
        user = await self.user_repo.get_by_username(user_id)
        if user:
            hashed_password = get_password_hash(new_password)
            updated_user = await self.user_repo.update_password(user, hashed_password)
            return UserAuthResponse.from_orm(updated_user)
        return None

    async def delete_user(self, user_id: str) -> None:
        """Мягкое удаление пользователя."""
        user = await self.user_repo.get_by_username(user_id)
        if user:
            await self.user_repo.delete(user)

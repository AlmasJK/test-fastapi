from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy import update
from typing import Optional, List
from uuid import UUID
from datetime import datetime

from app.models.user import User
from app.schemas.user_auth import UserAuthCreate
from app.repositories.base_repository import BaseRepository

class AuthRepository(BaseRepository[User]):
    def __init__(self, session: AsyncSession):
        self._session = session  # Убедитесь, что сессия передается и инициализируется правильно

    async def get_by_id(self, id: UUID) -> Optional[User]:
        """Заглушка для метода get_by_id."""
        result = await self._session.execute(select(User).filter_by(id=id, is_deleted=False))
        return result.scalars().first()
    
    async def update(self, id: UUID, **kwargs) -> Optional[User]:
        query = update(User).where(User.id == id, User.is_deleted == False).values(**kwargs).returning(User)
        result = await self._session.execute(query)
        await self._session.commit()
        return result.scalars().first()
    
    async def get_by_username(self, username: str) -> Optional[User]:
        """Получение пользователя по имени пользователя."""
        result = await self._session.execute(select(User).filter_by(username=username, is_deleted=False))
        return result.scalars().first()

    async def get_by_email(self, email: str) -> Optional[User]:
        """Получение пользователя по email."""
        result = await self._session.execute(select(User).filter_by(email=email, is_deleted=False))
        return result.scalars().first()

    async def create(self, user_data: UserAuthCreate) -> User:
        """Создание нового пользователя."""
        new_user = User(
            username=user_data.username,
            email=user_data.email,
            hashed_password=user_data.password,  # Хешированный пароль передается из сервиса
            is_active=True
        )
        self._session.add(new_user)  # Использование метода add на объекте AsyncSession
        await self._session.commit()
        await self._session.refresh(new_user)
        return new_user

    async def update_password(self, id: UUID, new_password: str) -> Optional[User]:
        """Обновление пароля пользователя."""
        return await self.update(id, hashed_password=new_password)

    async def soft_delete(self, id: UUID) -> Optional[User]:
        """Мягкое удаление пользователя."""
        return await self.update(id, is_deleted=True)

    async def get_all(self) -> List[User]:
        """Получение всех пользователей."""
        result = await self._session.execute(select(User).filter_by(is_deleted=False))
        return result.scalars().all()

    async def filter_by_dates(self, start_date: datetime, end_date: datetime, include_deleted: bool = False) -> List[User]:
        """Фильтрация пользователей по дате создания."""
        query = select(User).filter(User.created_at >= start_date, User.created_at <= end_date)
        if not include_deleted:
            query = query.filter_by(is_deleted=False)
        result = await self._session.execute(query)
        return result.scalars().all()

from sqlalchemy.ext.asyncio import AsyncSession
from app.repositories.user_repository import UserRepository
from app.models.user import User
from app.schemas.user import UserCreate, UserUpdate
from typing import List, Optional
from uuid import UUID

class UserService:
    def __init__(self, user_repo: UserRepository):
        self._user_repo = user_repo

    async def get_user_by_id(self, id: UUID) -> Optional[User]:
        return await self._user_repo.get_by_id(id)

    async def get_all_users(self) -> List[User]:
        return await self._user_repo.get_all()

    async def create_user(self, user_data: UserCreate) -> User:
        new_user = User(**user_data.model_dump())
        return await self._user_repo.create(new_user)

    async def update_user(self, id: UUID, user_data: UserUpdate) -> Optional[User]:
        return await self._user_repo.update(id, **user_data.model_dump())

    async def delete_user(self, id: UUID) -> Optional[User]:
        return await self._user_repo.soft_delete(id)

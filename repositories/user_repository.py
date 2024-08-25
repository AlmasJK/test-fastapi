from typing import List, Optional
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy import update
from datetime import datetime
from uuid import UUID

from app.models.user import User
from app.repositories.base_repository import BaseRepository

class UserRepository(BaseRepository[User]):
    async def get_by_id(self, id: UUID) -> Optional[User]:
        result = await self._session.execute(select(User).filter_by(id=id, is_deleted=False))
        return result.scalars().first()

    async def get_all(self) -> List[User]:
        result = await self._session.execute(select(User).filter_by(is_deleted=False))
        return result.scalars().all()

    async def filter_by_dates(self, start_date: datetime, end_date: datetime, include_deleted: bool = False) -> List[User]:
        query = select(User).filter(User.created_at >= start_date, User.created_at <= end_date)
        if not include_deleted:
            query = query.filter_by(is_deleted=False)
        result = await self._session.execute(query)
        return result.scalars().all()

    async def create(self, entity: User) -> User:
        self._session.add(entity)
        await self._session.commit()
        await self._session.refresh(entity)
        return entity

    async def update(self, id: UUID, **kwargs) -> Optional[User]:
        query = update(User).where(User.id == id, User.is_deleted == False).values(**kwargs).returning(User)
        result = await self._session.execute(query)
        await self._session.commit()
        return result.scalars().first()

    async def soft_delete(self, id: UUID) -> Optional[User]:
        query = update(User).where(User.id == id).values(is_deleted=True).returning(User)
        result = await self._session.execute(query)
        await self._session.commit()
        return result.scalars().first()

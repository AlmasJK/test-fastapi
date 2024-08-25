from abc import ABC, abstractmethod
from typing import Generic, TypeVar, List, Optional
from uuid import UUID
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from datetime import datetime

T = TypeVar('T')

class BaseRepository(ABC, Generic[T]):
    def __init__(self, session: AsyncSession):
        self._session = session

    @abstractmethod
    async def get_by_id(self, id: UUID) -> Optional[T]:
        pass

    @abstractmethod
    async def get_all(self) -> List[T]:
        pass

    @abstractmethod
    async def filter_by_dates(self, start_date: datetime, end_date: datetime, include_deleted: bool = False) -> List[T]:
        pass

    @abstractmethod
    async def create(self, entity: T) -> T:
        pass

    @abstractmethod
    async def update(self, id: UUID, **kwargs) -> Optional[T]:
        pass

    @abstractmethod
    async def soft_delete(self, id: UUID) -> Optional[T]:
        pass

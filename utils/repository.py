from abc import ABC, abstractmethod
from collections.abc import Sequence
from typing import TYPE_CHECKING, Any, Generic, Never, TypeVar

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from models.base import Base


if TYPE_CHECKING:
    from sqlalchemy.engine import Result


class AbstractRepository(ABC):
    @abstractmethod
    async def get_by_query_one_or_none(self, *args: Any, **kwargs: Any):
        raise NotImplementedError

    @abstractmethod
    async def get_by_query_all(self, *args: Any, **kwargs: Any):
        raise NotImplementedError


M = TypeVar("M", bound=Base)


class SQLAlchemyRepository(AbstractRepository, Generic[M]):
    model: M

    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_by_query_one_or_none(self, *args: Any, **kwargs: Any) -> M | None:
        query = select(self.model.__table__).where(**kwargs)
        result: Result = await self.session.execute(query)
        return result.unique().scalar_one_or_none()

    async def get_by_query_all(self, *args: Any, **kwargs: Any) -> Sequence[M]:
        query = select(self.model.__table__).where(**kwargs)
        result: Result = await self.session.execute(query)
        return result.scalars().all()

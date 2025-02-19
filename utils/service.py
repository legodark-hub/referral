from collections.abc import Sequence
from typing import Any

from utils.uow import UnitOfWork, transaction_mode


class BaseService:
    base_repository: str

    def __init__(self) -> None:
        self.uow: UnitOfWork = UnitOfWork()

    @transaction_mode
    async def get_by_query_one_or_none(self, *args: Any, **kwargs: Any) -> Any | None:
        return await self.uow.__dict__[self.base_repository].get_by_query_one_or_none(
            *args, **kwargs
        )

    @transaction_mode
    async def get_by_query_all(self, *args: Any, **kwargs: Any) -> Sequence[Any]:
        return await self.uow.__dict__[self.base_repository].get_by_query_all(
            *args, **kwargs
        )

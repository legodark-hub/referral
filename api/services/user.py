from typing import Any
from utils.service import BaseService
from utils.uow import transaction_mode


class UserService(BaseService):
    base_repository = 'user'
    
    @transaction_mode
    async def create_user(self, user_data: dict) -> Any:
        return await self.uow.user.create_user(user_data)

    @transaction_mode
    async def get_user_by_id(self, user_id: int) -> Any:
        return await self.uow.user.get_user_by_id(user_id)

    @transaction_mode
    async def get_user_by_email(self, email: str) -> Any:
        return await self.uow.user.get_user_by_email(email)

    @transaction_mode
    async def get_user_by_username(self, username: str) -> Any:
        return await self.uow.user.get_user_by_username(username)

    @transaction_mode
    async def update_user(self, user: Any, update_data: dict) -> Any:
        return await self.uow.user.update_user(user, update_data)

    @transaction_mode
    async def delete_user(self, user: Any) -> None:
        await self.uow.user.delete_user(user)
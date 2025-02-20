from typing import Any
from utils.service import BaseService
from utils.uow import transaction_mode


class ReferralCodeService(BaseService):
    base_repository = "referral_code"
    
    @transaction_mode
    async def get_by_code(self, code: str) -> Any:
        return await self.uow.referral_code.get_by_code(code)

    @transaction_mode
    async def get_by_user_id(self, user_id: int) -> Any:
        return await self.uow.referral_code.get_by_user_id(user_id)

    @transaction_mode
    async def create(self, referral_code_data: Any) -> Any:
        return await self.uow.referral_code.create(referral_code_data)
    
    @transaction_mode
    async def update(self, referral_code: Any, update_data: dict) -> Any:
        return await self.uow.referral_code.update(referral_code, update_data)

    @transaction_mode
    async def delete(self, referral_code: Any) -> None:
        await self.uow.referral_code.delete(referral_code)

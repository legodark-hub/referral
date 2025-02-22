from datetime import datetime, timedelta
from typing import Any

from fastapi import HTTPException, status
from utils.service import BaseService
from utils.uow import transaction_mode
from schemas.referral_code import ReferralCodeCreate
from utils.code_gen import generate_referral_code

class ReferralCodeService(BaseService):
    base_repository = "referral_code"

    @transaction_mode
    async def get_by_code(self, code: str) -> Any:
        return await self.uow.referral_code.get_by_code(code)

    @transaction_mode
    async def get_by_user_id(self, user_id: int) -> Any:
        user_id = int(user_id)
        referral_code = await self.uow.referral_code.get_by_user_id(user_id)
        if not referral_code:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail={"message": "You do not have an referral code"},
            )
        return await self.uow.referral_code.get_by_user_id(user_id)

    @transaction_mode
    async def create(self, referral_data: ReferralCodeCreate, user_id) -> Any:
        referral_dict = referral_data.model_dump()
        referral_dict["code"] = generate_referral_code()
        referral_dict["expires_at"] = datetime.now() + timedelta(
            days=referral_dict.pop("expiry_period")
        )
        referral_dict["user_id"] = int(user_id)

        existing_referral = await self.uow.referral_code.get_by_user_id(int(user_id))
        if existing_referral:
            if existing_referral.expires_at > datetime.now():
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail={"message": "Active referral code already exists for this user"},
                )
            return await self.uow.referral_code.update(referral_dict)
        else:
            return await self.uow.referral_code.create(referral_dict)

    @transaction_mode
    async def update(self, update_data: dict) -> Any:
        return await self.uow.referral_code.update(update_data)

    @transaction_mode
    async def delete(self, user_id) -> None:
        await self.uow.referral_code.delete(int(user_id))
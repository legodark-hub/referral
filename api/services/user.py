from typing import Any

from fastapi import HTTPException, status
from schemas.user import UserCreate, UserLogin
from utils.security import get_password_hash, verify_password, security
from utils.service import BaseService
from utils.uow import transaction_mode


class UserService(BaseService):
    base_repository = "user"

    @transaction_mode
    async def create_user(self, user_data: UserCreate) -> Any:
        if await self.get_user_by_email(
            user_data.email
        ) or await self.get_user_by_username(user_data.username):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail={"message": "Email or username already registered"},
            )
        user_dict = user_data.model_dump()

        user_dict["password_hash"] = get_password_hash(user_dict.pop("password"))

        referral_code = user_dict.pop("referral_code", None)
        if referral_code:
            referrer = await self.uow.referral_code.get_by_code(referral_code)
            if not referrer:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail={"message": "Referral code not found"},
                )
            user_dict["referrer_id"] = referrer.user_id
        return await self.uow.user.create_user(user_dict)

    @transaction_mode
    async def authenticate_user(self, login_data: UserLogin) -> Any:
        user = await self.uow.user.get_user_by_email(login_data.email)
        if not user or not verify_password(login_data.password, user.password_hash):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail={"message": "Incorrect email or password"},
            )
        token = security.create_access_token(uid=str(user.id))
        return token

    @transaction_mode
    async def get_user_by_id(self, user_id: int) -> Any:
        return await self.uow.user.get_user_by_id(int(user_id))

    @transaction_mode
    async def get_user_by_email(self, email: str) -> Any:
        return await self.uow.user.get_user_by_email(email)

    @transaction_mode
    async def get_user_by_username(self, username: str) -> Any:
        return await self.uow.user.get_user_by_username(username)
    
    @transaction_mode
    async def get_user_referrals(self, user_id: int) -> Any:
        user_id = int(user_id)
        return await self.uow.user.get_user_referrals(user_id)

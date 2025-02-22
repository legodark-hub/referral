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
        return {"access_token": token, "token_type": "bearer"}

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

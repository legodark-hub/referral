from sqlalchemy import select
from models.referral_code import ReferralCode
from utils.repository import SQLAlchemyRepository


class ReferralCodeRepository(SQLAlchemyRepository):
    model: ReferralCode
    
    async def get_by_code(self, code: str) -> ReferralCode | None:
        query = select(ReferralCode).where(ReferralCode.code == code)
        result = await self.session.execute(query)
        return result.scalar_one_or_none()

    async def get_by_user_id(self, user_id: int) -> ReferralCode | None:
        query = select(ReferralCode).where(ReferralCode.user_id == user_id)
        result = await self.session.execute(query)
        return result.scalar_one_or_none()

    async def create(self, referral_code: ReferralCode) -> ReferralCode:
        self.session.add(referral_code)
        await self.session.flush()
        return referral_code

    async def delete(self, referral_code: ReferralCode) -> None:
        await self.session.delete(referral_code)
        await self.session.flush()
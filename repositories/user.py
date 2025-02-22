from sqlalchemy import select
from models.user import User
from utils.repository import SQLAlchemyRepository


class UserRepository(SQLAlchemyRepository):
    model: User
    
    async def create_user(self, user_data: dict) -> User:
        user = User(**user_data)
        self.session.add(user)
        await self.session.commit()
        return user

    async def get_user_by_id(self, user_id: int) -> User | None:
        return await self.session.get(User, user_id)

    async def get_user_by_email(self, email: str) -> User | None:
        query = await self.session.execute(
            select(User).where(User.email == email)
        )
        return query.scalar_one_or_none()

    async def get_user_by_username(self, username: str) -> User | None:
        query = await self.session.execute(
            select(User).where(User.username == username)
        )
        return query.scalar_one_or_none()

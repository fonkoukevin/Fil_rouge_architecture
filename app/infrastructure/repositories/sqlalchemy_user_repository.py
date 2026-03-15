from sqlalchemy import select, Column, Integer, String
from sqlalchemy.ext.asyncio import AsyncSession

from app.infrastructure.database import Base
from app.domain.entities.user import User
from app.domain.repositories.user_repository import UserRepository

class UserModel(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(255), unique=True, index=True, nullable=False)
    hashed_password = Column(String(255), nullable=False)
    role = Column(String(50), nullable=False)

class SQLAlchemyUserRepository(UserRepository):
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_by_email(self, email: str) -> User | None:
        result = await self.session.execute(select(UserModel).where(UserModel.email == email))
        model = result.scalar_one_or_none()
        if not model:
            return None
        return User(id=model.id, email=model.email, hashed_password=model.hashed_password, role=model.role)

    async def create(self, email: str, hashed_password: str, role: str) -> User:
        model = UserModel(email=email, hashed_password=hashed_password, role=role)
        self.session.add(model)
        await self.session.commit()
        await self.session.refresh(model)

        return User(id=model.id, email=model.email, hashed_password=model.hashed_password, role=model.role)

    
    async def get_by_id(self, user_id: int) -> User | None:
        stmt = select(UserModel).where(UserModel.id == user_id)
        res = await self.session.execute(stmt)
        model = res.scalar_one_or_none()
        if not model:
            return None
        return User(
            id=model.id,
            email=model.email,
            hashed_password=model.hashed_password,
            role=model.role,
        )





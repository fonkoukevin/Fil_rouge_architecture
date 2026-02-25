from fastapi import APIRouter, Depends
from pydantic import BaseModel
from sqlalchemy.ext.asyncio import AsyncSession

from app.infrastructure.database import get_db
from app.infrastructure.repositories.sqlalchemy_user_repository import (
    SQLAlchemyUserRepository,
)
from app.infrastructure.security.password_hasher import PasswordHasher
from app.infrastructure.security.jwt_provider import JWTProvider
from app.application.use_cases.login_use_case import LoginUseCase

router = APIRouter(prefix="/auth", tags=["Auth"])


class LoginRequest(BaseModel):
    email: str
    password: str


@router.post("/login")
async def login(request: LoginRequest, db: AsyncSession = Depends(get_db)):
    repository = SQLAlchemyUserRepository(db)
    hasher = PasswordHasher()
    jwt_provider = JWTProvider()

    use_case = LoginUseCase(repository, hasher, jwt_provider)

    return await use_case.execute(request.email, request.password)
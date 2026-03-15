from fastapi import APIRouter, Depends,HTTPException
from pydantic import BaseModel, EmailStr, Field
from sqlalchemy.ext.asyncio import AsyncSession

from app.presentation.auth_dependencies import get_current_user_id
from app.infrastructure.database import get_db
from app.infrastructure.repositories.sqlalchemy_user_repository import SQLAlchemyUserRepository
from app.infrastructure.security.password_hasher import PasswordHasher
from app.infrastructure.security.jwt_provider import JwtProvider
from app.domain.services.authentication_service import AuthenticationService
from app.application.use_cases.login_use_case import LoginUseCase
from app.application.use_cases.register_use_case import RegisterUseCase
from app.application.use_cases.get_me_use_case import GetMeUseCase

router = APIRouter(prefix="/auth", tags=["Auth"])


class LoginRequest(BaseModel):
    email: EmailStr
    password: str
    
class RegisterRequest(BaseModel):
    email: EmailStr
    password: str = Field(min_length=6, max_length=128)
    role: str = "LECTEUR"  # simple pour MVP


@router.post("/register", status_code=201)
async def register(request: RegisterRequest, db: AsyncSession = Depends(get_db)):
    repository = SQLAlchemyUserRepository(db)
    hasher = PasswordHasher()

    use_case = RegisterUseCase(repository, hasher)
    return await use_case.execute(request.email, request.password, request.role)


@router.post("/login")
async def login(request: LoginRequest, db: AsyncSession = Depends(get_db)):
    repository = SQLAlchemyUserRepository(db)
    hasher = PasswordHasher()
    jwt_provider = JwtProvider()

    auth_service = AuthenticationService(repository, hasher, jwt_provider)
    use_case = LoginUseCase(auth_service)

    return await use_case.execute(request.email, request.password)


@router.get("/me")
async def me(
    user_id: int = Depends(get_current_user_id),
    db: AsyncSession = Depends(get_db),
):
    repo = SQLAlchemyUserRepository(db)
    use_case = GetMeUseCase(repo)

    user = await use_case.execute(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    # sans DTO: on renvoie un JSON simple
    return {
        "id": user.id,
        "email": user.email,
        "role": getattr(user, "role", None),
    }
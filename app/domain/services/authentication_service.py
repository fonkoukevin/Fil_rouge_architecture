from fastapi import HTTPException, status

from app.domain.repositories.user_repository import UserRepository
from app.infrastructure.security.password_hasher import PasswordHasher
from app.infrastructure.security.jwt_provider import JwtProvider

class AuthenticationService:
    def __init__(
        self,
        repository: UserRepository,
        hasher: PasswordHasher,
        jwt_provider: JwtProvider,
    ):
        self.repository = repository
        self.hasher = hasher
        self.jwt_provider = jwt_provider

    async def authenticate(self, email: str, password: str):
        user = await self.repository.get_by_email(email)
        if not user:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")

        if not self.hasher.verify(password, user.hashed_password):
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")

        token = self.jwt_provider.create_access_token({"sub": str(user.id), "role": user.role})
        return {"access_token": token, "token_type": "bearer"}
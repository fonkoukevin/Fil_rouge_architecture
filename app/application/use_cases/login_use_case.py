from app.domain.repositories.user_repository import UserRepository
from app.infrastructure.security.password_hasher import PasswordHasher
from app.infrastructure.security.jwt_provider import JWTProvider
from fastapi import HTTPException

class LoginUseCase:

    def __init__(
        self,
        repository: UserRepository,
        hasher: PasswordHasher,
        jwt_provider: JWTProvider,
    ):
        self.repository = repository
        self.hasher = hasher
        self.jwt_provider = jwt_provider

    async def execute(self, email: str, password: str):
        user = await self.repository.get_by_email(email)

        if not user:
            raise HTTPException(status_code=401, detail="Invalid credentials")

        if not self.hasher.verify(password, user.hashed_password):
            raise HTTPException(status_code=401, detail="Invalid credentials")

        token = self.jwt_provider.create_access_token(
            {"sub": str(user.id), "role": user.role}
        )

        return {"access_token": token, "token_type": "bearer"}
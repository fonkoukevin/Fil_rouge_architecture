from fastapi import HTTPException, status

from app.domain.repositories.user_repository import UserRepository
from app.infrastructure.security.password_hasher import PasswordHasher

class RegisterUseCase:
    def __init__(self, repository: UserRepository, hasher: PasswordHasher):
        self.repository = repository
        self.hasher = hasher

    async def execute(self, email: str, password: str, role: str = "LECTEUR"):
        existing = await self.repository.get_by_email(email)
        if existing:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Email déjà utilisé",
            )

        hashed = self.hasher.hash(password)
        user = await self.repository.create(email=email, hashed_password=hashed, role=role)

        # On ne renvoie jamais le hash
        return {"id": user.id, "email": user.email, "role": user.role}
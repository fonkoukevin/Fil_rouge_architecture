import pytest

from app.application.use_cases.get_me_use_case import GetMeUseCase
from app.application.use_cases.login_use_case import LoginUseCase
from app.application.use_cases.register_use_case import RegisterUseCase

class FakeUserRepository:
    def __init__(self):
        self.users_by_id = {}
        self.users_by_email = {}
        self.created_args = None

    async def get_by_id(self, user_id: int):
        return self.users_by_id.get(user_id)

    async def get_by_email(self, email: str):
        return self.users_by_email.get(email)

    async def create(self, email: str, hashed_password: str, role: str):
        self.created_args = {
            "email": email,
            "hashed_password": hashed_password,
            "role": role,
        }
        user = {
            "id": 1,
            "email": email,
            "hashed_password": hashed_password,
            "role": role,
        }
        self.users_by_id[1] = user
        self.users_by_email[email] = user
        return user

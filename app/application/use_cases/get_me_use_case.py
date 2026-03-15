from app.domain.repositories.user_repository import UserRepository

class GetMeUseCase:
    def __init__(self, user_repo: UserRepository):
        self.user_repo = user_repo

    async def execute(self, user_id: int):
        user = await self.user_repo.get_by_id(user_id)
        if not user:
            return None
        return user
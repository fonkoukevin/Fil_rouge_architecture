class LoginUseCase:
    def __init__(self, auth_service):
        self.auth_service = auth_service

    async def execute(self, email: str, password: str):
        return await self.auth_service.authenticate(email, password)
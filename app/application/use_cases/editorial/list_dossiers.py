from app.domain.repositories.editorial_dossier_repository import EditorialDossierRepository


class ListEditorialDossiersUseCase:
    def __init__(self, dossier_repository: EditorialDossierRepository) -> None:
        self.dossier_repository = dossier_repository

    async def execute(self, status: str | None = None):
        return await self.dossier_repository.list_all(status=status)

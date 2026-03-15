from app.domain.repositories.editorial_dossier_repository import EditorialDossierRepository


class EditorialDossierNotFoundError(Exception):
    pass


class GetEditorialDossierUseCase:
    def __init__(self, dossier_repository: EditorialDossierRepository) -> None:
        self.dossier_repository = dossier_repository

    async def execute(self, dossier_id: str):
        dossier = await self.dossier_repository.get_by_id(dossier_id)
        if dossier is None:
            raise EditorialDossierNotFoundError("Dossier éditorial introuvable.")
        return dossier

from abc import ABC, abstractmethod

from app.domain.entities.editorial_dossier import EditorialDossier


class EditorialDossierRepository(ABC):
    @abstractmethod
    async def create(self, dossier: EditorialDossier) -> EditorialDossier:
        pass

    @abstractmethod
    async def get_by_id(self, dossier_id: str) -> EditorialDossier | None:
        pass

    @abstractmethod
    async def get_by_manuscript_id(self, manuscript_id: str) -> EditorialDossier | None:
        pass

    @abstractmethod
    async def update(self, dossier: EditorialDossier) -> EditorialDossier:
        pass

    @abstractmethod
    async def list_all(self, status: str | None = None) -> list[EditorialDossier]:
        pass

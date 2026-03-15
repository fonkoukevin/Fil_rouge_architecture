from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.domain.entities.editorial_dossier import EditorialDossier
from app.domain.repositories.editorial_dossier_repository import EditorialDossierRepository
from app.infrastructure.models import EditorialDossierModel


class SqlAlchemyEditorialDossierRepository(EditorialDossierRepository):
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    def _to_domain(self, model: EditorialDossierModel) -> EditorialDossier:
        return EditorialDossier(
            id=model.id,
            manuscript_id=model.manuscript_id,
            submitted_by_user_id=model.submitted_by_user_id,
            assigned_editor_id=model.assigned_editor_id,
            status=model.status,
            submission_note=model.submission_note,
            editorial_note=model.editorial_note,
            created_at=model.created_at,
            updated_at=model.updated_at,
        )

    async def create(self, dossier: EditorialDossier) -> EditorialDossier:
        model = EditorialDossierModel(
            manuscript_id=dossier.manuscript_id,
            submitted_by_user_id=dossier.submitted_by_user_id,
            assigned_editor_id=dossier.assigned_editor_id,
            status=dossier.status,
            submission_note=dossier.submission_note,
            editorial_note=dossier.editorial_note,
            created_at=dossier.created_at,
            updated_at=dossier.updated_at,
        )
        self.session.add(model)
        await self.session.flush()
        await self.session.refresh(model)
        return self._to_domain(model)

    async def get_by_id(self, dossier_id: str) -> EditorialDossier | None:
        stmt = select(EditorialDossierModel).where(EditorialDossierModel.id == dossier_id)
        result = await self.session.execute(stmt)
        model = result.scalar_one_or_none()
        if model is None:
            return None
        return self._to_domain(model)

    async def get_by_manuscript_id(self, manuscript_id: str) -> EditorialDossier | None:
        stmt = select(EditorialDossierModel).where(
            EditorialDossierModel.manuscript_id == manuscript_id
        )
        result = await self.session.execute(stmt)
        model = result.scalar_one_or_none()
        if model is None:
            return None
        return self._to_domain(model)

    async def update(self, dossier: EditorialDossier) -> EditorialDossier:
        stmt = select(EditorialDossierModel).where(EditorialDossierModel.id == dossier.id)
        result = await self.session.execute(stmt)
        model = result.scalar_one()

        model.assigned_editor_id = dossier.assigned_editor_id
        model.status = dossier.status
        model.submission_note = dossier.submission_note
        model.editorial_note = dossier.editorial_note
        model.updated_at = dossier.updated_at

        await self.session.flush()
        await self.session.refresh(model)
        return self._to_domain(model)

    async def list_all(self, status: str | None = None) -> list[EditorialDossier]:
        stmt = select(EditorialDossierModel).order_by(EditorialDossierModel.created_at.desc())

        if status:
            stmt = stmt.where(EditorialDossierModel.status == status)

        result = await self.session.execute(stmt)
        models = result.scalars().all()
        return [self._to_domain(model) for model in models]

from app.application.use_cases.manuscript.get_manuscript import ManuscriptNotFoundError
from app.domain.entities.chapter import Chapter
from app.domain.repositories.manuscript_repository import ManuscriptRepository


class AddChapterUseCase:
    def __init__(self, repository: ManuscriptRepository) -> None:
        self.repository = repository

    async def execute(self, author_id: str, manuscript_id: str, title: str, content: str) -> Chapter:
        manuscript = await self.repository.get_by_id_and_author_id(manuscript_id, author_id)
        if manuscript is None:
            raise ManuscriptNotFoundError("Manuscrit introuvable.")

        next_order = await self.repository.get_next_chapter_order(manuscript_id)

        chapter = Chapter(
            id=None,
            manuscript_id=manuscript_id,
            title=title.strip(),
            content=content.strip(),
            chapter_order=next_order,
        )

        manuscript.add_chapter(chapter)
        await self.repository.update_manuscript(manuscript)
        return await self.repository.add_chapter(chapter)

from app.application.use_cases.manuscript.get_manuscript import ManuscriptNotFoundError
from app.domain.repositories.manuscript_repository import ManuscriptRepository


class ChapterNotFoundError(Exception):
    pass


class UpdateChapterUseCase:
    def __init__(self, repository: ManuscriptRepository) -> None:
        self.repository = repository

    async def execute(
        self,
        author_id: str,
        manuscript_id: str,
        chapter_id: str,
        title: str,
        content: str,
    ):
        manuscript = await self.repository.get_by_id_and_author_id(manuscript_id, author_id)
        if manuscript is None:
            raise ManuscriptNotFoundError("Manuscrit introuvable.")

        chapter = await self.repository.get_chapter_by_id(chapter_id)
        if chapter is None:
            raise ChapterNotFoundError("Chapitre introuvable.")

        if chapter.manuscript_id != manuscript_id:
            raise ChapterNotFoundError("Ce chapitre n'appartient pas à ce manuscrit.")

        chapter.update(title, content)
        return await self.repository.update_chapter(chapter)

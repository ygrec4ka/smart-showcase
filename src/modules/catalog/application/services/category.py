from sqlalchemy.ext.asyncio import AsyncSession

from modules.catalog.infrastructure.repositories import (
    CategoryRepository,
)


class CategoryService:
    def __init__(
        self,
        category_repository: CategoryRepository,
        session: AsyncSession,
    ):
        self.category_repository = category_repository
        self.session = session

from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from modules.catalog.domain.entities import Category
from modules.catalog.infrastructure.models import CategoryTable


class CategoryRepository:
    def __init__(self, session: AsyncSession):
        self._session = session

    async def get_by_id(self, category_id: UUID, company_id: UUID) -> Category | None:
        result = await self._session.execute(
            select(CategoryTable).where(
                CategoryTable.id == category_id,
                CategoryTable.company_id == company_id,
            )
        )
        category_orm: CategoryTable | None = result.scalar_one_or_none()

        if not category_orm:
            return None

        return Category(
            name=category_orm.name,
            company_id=category_orm.company_id,
            parent_id=category_orm.parent_id,
            id=category_orm.id,
        )

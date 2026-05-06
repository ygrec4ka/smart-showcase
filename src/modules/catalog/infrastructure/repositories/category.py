from typing import Sequence

from uuid import UUID

from sqlalchemy import select, Result, update, delete
from sqlalchemy.ext.asyncio import AsyncSession

from modules.catalog.domain.entities import Category
from modules.catalog.infrastructure.models import CategoryTable


class CategoryRepository:
    def __init__(self, session: AsyncSession):
        self._session = session

    @staticmethod
    def _to_domain(category_orm: CategoryTable) -> Category:
        return Category(
            id=category_orm.id,
            name=category_orm.name,
            company_id=category_orm.company_id,
        )

    @staticmethod
    def _to_table(category: Category) -> CategoryTable:
        return CategoryTable(
            id=category.id,
            name=category.name,
            company_id=category.company_id,
        )

    async def create(self, category: Category) -> Category:
        category_orm = self._to_table(category)
        self._session.add(category_orm)
        return category

    async def get_by_id(
        self,
        category_id: UUID,
        company_id: UUID,
    ) -> Category | None:
        stmt = select(CategoryTable).where(
            CategoryTable.id == category_id,
            CategoryTable.company_id == company_id,
        )
        result: Result = await self._session.execute(stmt)
        category_orm: CategoryTable | None = result.scalar_one_or_none()

        if not category_orm:
            return None

        return self._to_domain(category_orm)

    async def list_categories(self, company_id: UUID) -> Sequence[Category]:
        stmt = (
            select(CategoryTable)
            .where(CategoryTable.company_id == company_id)
            .order_by(CategoryTable.name)
        )

        result: Result = await self._session.execute(stmt)
        categories_orm: Sequence[CategoryTable] = result.scalars().all()

        return [self._to_domain(c) for c in categories_orm]

    async def update(
        self,
        category_id: UUID,
        company_id: UUID,
        update_data: dict,
    ) -> Category | None:
        if not update_data:
            return await self.get_by_id(category_id, company_id)

        stmt = (
            update(CategoryTable)
            .where(
                CategoryTable.id == category_id,
                CategoryTable.company_id == company_id,
            )
            .values(**update_data)
            .returning(CategoryTable)
        )
        result: Result = await self._session.execute(stmt)
        category_orm: CategoryTable | None = result.scalar_one_or_none()

        if not category_orm:
            return None

        return self._to_domain(category_orm)

    async def delete(self, category_id: UUID, company_id: UUID) -> bool:
        stmt = delete(CategoryTable).where(
            CategoryTable.id == category_id,
            CategoryTable.company_id == company_id,
        )
        result: Result = await self._session.execute(stmt)

        return result.rowcount > 0

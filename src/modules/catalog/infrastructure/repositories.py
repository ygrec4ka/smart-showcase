from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from modules.catalog.domain.entities import Product, Category
from modules.catalog.infrastructure.models import ProductTable, CategoryTable


class CategoryRepository:
    def __init__(self, session: AsyncSession):
        self._session = session

    async def get_by_id(self, category_id: UUID, company_id: UUID) -> Category | None:
        """Получает категорию из базы и превращает его в доменную сущность"""
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


class ProductRepository:
    def __init__(self, session: AsyncSession):
        self._session = session

    async def get_by_id(self, product_id: UUID, company_id: UUID) -> Product | None:
        result = await self._session.execute(
            select(ProductTable).where(
                ProductTable.id == product_id,
                ProductTable.company_id == company_id,
            )
        )
        product_orm: ProductTable | None = result.scalar_one_or_none()

        if not product_orm:
            return None  # В будущем можно реализовать custom исключения.

        return Product(
            id=product_orm.id,
            title=product_orm.title,
            sku=product_orm.sku,
            base_price=product_orm.base_price,
            company_id=product_orm.company_id,
            category_id=product_orm.category_id,
            description=product_orm.description,
            is_active=product_orm.is_active,
        )

    async def get_by_sku(self, sku: str, company_id: UUID) -> Product | None:
        result = await self._session.execute(
            select(ProductTable).where(
                ProductTable.sku == sku,
                ProductTable.company_id == company_id,
            )
        )

        product_orm: ProductTable | None = result.scalar_one_or_none()

        if not product_orm:
            return None

        return Product(
            id=product_orm.id,
            title=product_orm.title,
            sku=product_orm.sku,
            base_price=product_orm.base_price,
            company_id=product_orm.company_id,
            category_id=product_orm.category_id,
            description=product_orm.description,
            is_active=product_orm.is_active,
        )

    async def save(
        self, product: Product
    ) -> None:  # Тяжелый метод, который в будущем при большой нагрузке стоит заменить.
        """Сохраняет или обновляет доменную сущность в базе."""
        product_orm = ProductTable(
            id=product.id,
            title=product.title,
            sku=product.sku,
            base_price=product.base_price,
            company_id=product.company_id,
            category_id=product.category_id,
            description=product.description,
            is_active=product.is_active,
        )
        await self._session.merge(product_orm)

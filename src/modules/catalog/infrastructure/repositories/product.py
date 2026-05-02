from uuid import UUID

from sqlalchemy import select, update, Result, Sequence, desc
from sqlalchemy.ext.asyncio import AsyncSession

from modules.catalog.domain.entities import Product
from modules.catalog.infrastructure.models import ProductTable


class ProductRepository:
    def __init__(self, session: AsyncSession):
        self._session = session

    @staticmethod
    def _to_domain(product_orm: ProductTable) -> Product:
        return Product(
            id=product_orm.id,
            title=product_orm.title,
            sku=product_orm.sku,
            base_price=product_orm.base_price,
            company_id=product_orm.company_id,
            category_id=product_orm.category_id,
            description=product_orm.description,
            is_active=product_orm.is_active,
            created_at=product_orm.created_at,
        )

    @staticmethod
    def _to_table(product: Product) -> ProductTable:
        return ProductTable(
            id=product.id,
            title=product.title,
            sku=product.sku,
            base_price=product.base_price,
            company_id=product.company_id,
            category_id=product.category_id,
            description=product.description,
            is_active=product.is_active,
            created_at=product.created_at,
        )

    async def create(self, product: Product) -> Product:
        product_orm = self._to_table(product)

        self._session.add(product_orm)
        return product

    async def get_by_id(self, product_id: UUID, company_id: UUID) -> Product | None:
        stmt = select(ProductTable).where(
            ProductTable.id == product_id,
            ProductTable.company_id == company_id,
        )
        result: Result = await self._session.execute(stmt)
        product_orm: ProductTable | None = result.scalar_one_or_none()

        if not product_orm:
            return None

        return self._to_domain(product_orm)

    async def get_by_ids(
        self,
        product_ids: list[UUID],
        company_id: UUID,
    ) -> Sequence[Product]:
        if not product_ids:
            return []

        stmt = select(ProductTable).where(
            ProductTable.id.in_(product_ids),
            ProductTable.company_id == company_id,
            ProductTable.is_active == True,
        )

        result: Result = await self._session.execute(stmt)
        products_orm: Sequence[ProductTable] = result.scalars().all()

        return [self._to_domain(p) for p in products_orm]

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

        return self._to_domain(product_orm)

    async def list_of_products(
        self,
        company_id: UUID,
        limit: int = 20,
        cursor_id: UUID | None = None,
        category_id: UUID | None = None,
        only_active: bool = True,
    ) -> Sequence[Product]:
        stmt = select(ProductTable).where(ProductTable.company_id == company_id)

        if only_active:
            stmt = stmt.where(ProductTable.is_active == True)

        if category_id:
            stmt = stmt.where(ProductTable.category_id == category_id)

        if cursor_id:
            stmt = stmt.where(ProductTable.id < cursor_id)

        stmt = stmt.order_by(desc(ProductTable.id)).limit(limit + 1)

        result: Result = await self._session.execute(stmt)
        products_orm: Sequence[ProductTable] = result.scalars().all()

        return [self._to_domain(p) for p in products_orm]

    async def update(
        self,
        product_id: UUID,
        update_data: dict,
        company_id: UUID,
    ) -> Product | None:

        if not update_data:
            return await self.get_by_id(product_id, company_id)

        stmt = (
            update(ProductTable)
            .where(
                ProductTable.id == product_id,
                ProductTable.company_id == company_id,
            )
            .values(**update_data)
            .returning(ProductTable)
        )
        result: Result = await self._session.execute(stmt)
        product_orm: ProductTable | None = result.scalar_one_or_none()

        if not product_orm:
            return None

        return self._to_domain(product_orm)

    async def deactivate(
        self,
        product_id: UUID,
        company_id: UUID,
    ) -> None:
        await self.update(product_id, {"is_active": False}, company_id)

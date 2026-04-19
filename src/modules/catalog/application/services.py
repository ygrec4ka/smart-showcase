from decimal import Decimal
from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession

from modules.catalog.domain.entities import Product, ProductFilter
from modules.catalog.domain.exceptions import (
    CategoryNotFoundError,
    SkuAlreadyExistsError,
    ProductNotFoundError,
)
from modules.catalog.infrastructure.repositories import (
    ProductRepository,
    CategoryRepository,
)


class CatalogService:
    def __init__(
        self,
        product_repository: ProductRepository,
        category_repository: CategoryRepository,
        session: AsyncSession,
    ):
        self.product_repository = product_repository
        self.category_repository = category_repository
        self.session = session

        async def create_product(
            self,
            title: str,
            sku: str,
            base_price: Decimal,
            company_id: UUID,
            category_id: UUID,
            description: str | None = None,
        ) -> Product:
            category = await self.category_repository.get_by_id(category_id, company_id)

            if not category:
                raise CategoryNotFoundError(f"Указанная категория не найдена")

            existing = await self.product_repository.get_by_sku(sku, company_id)
            if existing:
                raise SkuAlreadyExistsError(f"Товар с артикулом {sku} уже существует")

            product = Product(
                title=title,
                sku=sku,
                base_price=base_price,
                company_id=company_id,
                category_id=category_id,
                description=description,
            )

            await self.product_repository.save(product)
            await self.session.commit()

            return product

        async def get_product_by_id(product_id: UUID, company_id: UUID):
            product = await self.product_repository.get_by_id(product_id, company_id)

            if not product:
                raise ProductNotFoundError(f"Товар с id: {product_id} не найден")

            return product

        async def list_products(
            self, filters: ProductFilter
        ) -> list[Product]:  # (с пагинацией и фильтрами).
            pass

        async def update_product():
            pass

        async def get_category_tree():
            pass

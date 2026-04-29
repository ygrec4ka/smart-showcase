import base64
from datetime import datetime

from decimal import Decimal
from typing import Sequence

from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession

from modules.catalog.domain.entities import Product
from modules.catalog.domain.exceptions import (
    CategoryNotFoundError,
    SkuAlreadyExistsError,
    ProductNotFoundError,
)
from modules.catalog.infrastructure.models import ProductTable
from modules.catalog.infrastructure.repositories import (
    ProductRepository,
    CategoryRepository,
)


class ProductService:
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
        created_at: datetime,
        description: str | None = None,
    ) -> Product:
        category = await self.category_repository.get_by_id(
            category_id,
            company_id,
        )
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
            created_at=created_at,
            description=description,
        )

        self.session.add(product)
        await self.session.commit()
        return product

    async def get_product_by_id(
        self,
        product_id: UUID,
        company_id: UUID,
    ):
        product = await self.product_repository.get_by_id(product_id, company_id)
        if not product:
            raise ProductNotFoundError(f"Товар с id: {product_id} не найден")

        return product

    async def get_catalog_page(
        self, company_id: UUID, limit: int, cursor_b64: str | None = None
    ):
        cursor_id = None
        if cursor_b64:
            try:
                decoded_str = base64.b64decode(cursor_b64).decode("utf-8")
                cursor_id = UUID(decoded_str)
            except Exception:
                raise ValueError("Невалидный формат курсора.")

        products = await self.product_repository.list(
            company_id=company_id, limit=limit, cursor_id=cursor_id
        )

        has_more = len(products) > limit
        items_to_return = products[:limit]

        next_cursor_b64 = None
        if has_more:
            last_item = items_to_return[-1]
            next_cursor_b64 = base64.b64encode(str(last_item.id).encode()).decode(
                "utf-8"
            )

        return {
            "items": items_to_return,
            "next_cursor": next_cursor_b64,
            "has_more": has_more,
        }

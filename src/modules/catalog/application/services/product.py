import base64
from datetime import datetime, timezone
from typing import Sequence

from uuid import UUID
import uuid6

from sqlalchemy.ext.asyncio import AsyncSession


from modules.catalog.domain.entities import Product
from modules.catalog.infrastructure.repositories import (
    ProductRepository,
)
from modules.catalog.presentation.schemas.products import ProductCreate, ProductUpdate


class ProductService:
    def __init__(
        self,
        product_repository: ProductRepository,
        session: AsyncSession,
    ):
        self.product_repository = product_repository
        self._session = session

    def _generate_sku(self) -> str:
        pass

    async def create_product(
        self,
        company_id: UUID,
        data: ProductCreate
    ) -> Product:
        new_product = Product(
            id=uuid6.uuid7(),
            title=data.title,
            description=data.description,
            base_price=data.base_price,
            category_id=data.category_id,
            company_id=company_id,
            sku=self._generate_sku(),
            is_active=True,
            created_at=datetime.now(timezone.utc)
        )

        await self.product_repository.create(new_product)
        await self._session.commit()

        return new_product

    async def get_product_by_id(
        self,
        product_id: UUID,
        company_id: UUID,
    ) -> Product | None:
        return await self.product_repository.get_by_id(product_id=product_id, company_id=company_id)

    async def get_products_by_ids(
        self,
        product_ids: list[UUID],
        company_id: UUID
    ) -> Sequence[Product]:
        return await self.product_repository.get_by_ids(product_ids=product_ids, company_id=company_id)

    async def get_product_by_sku(
        self,
        sku: str,
        company_id: UUID
    ) -> Product | None:
        return await self.product_repository.get_by_sku(sku=sku, company_id=company_id)

    async def get_catalog_page(
        self,
        company_id: UUID,
        limit: int = 20,
        cursor_b64: str | None = None,
        category_id: UUID | None = None,
    ):
        cursor_id = None
        if cursor_b64:
            try:
                decoded_str = base64.b64decode(cursor_b64).decode("utf-8")
                cursor_id = UUID(decoded_str)
            except ValueError:
                raise ValueError("Невалидный формат курсора.")

        products = await self.product_repository.list_of_products(
            company_id=company_id,
            limit=limit,
            cursor_id=cursor_id,
            category_id=category_id,
        )

        has_more = len(products) > limit
        items_to_return = products[:limit]

        next_cursor_b64 = None
        if has_more:
            last_item = items_to_return[-1]
            next_cursor_b64 = base64.b64encode(str(last_item.id).encode("utf-8")).decode("utf-8")

        return {
            "items": items_to_return,
            "next_cursor": next_cursor_b64,
            "has_more": has_more,
        }

    async def update_product(
        self,
        product_id: UUID,
        company_id: UUID,
        data: ProductUpdate,
    ) -> Product | None:
        update_data = data.model_dump(exclude_unset=True)

        if not update_data:
            return await self.get_product_by_id(product_id, company_id)

        updated_product = await self.product_repository.update(
            product_id=product_id,
            company_id=company_id,
            update_data=update_data,
        )

        if updated_product:
            await self._session.commit()

        return updated_product

    async def deactivate_product(
        self,
        product_id: UUID,
        company_id: UUID,
    ) -> None:
        await self.product_repository.deactivate(product_id=product_id, company_id=company_id)
        await self._session.commit()
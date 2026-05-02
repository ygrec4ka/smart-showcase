from decimal import Decimal
from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession

from modules.catalog.domain.entities.product import Product, ProductFilter
from modules.catalog.domain.exceptions import (
    CategoryNotFoundError,
    SkuAlreadyExistsError,
    ProductNotFoundError,
)
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



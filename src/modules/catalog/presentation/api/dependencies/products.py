from fastapi import Depends

from infra import database_helper

from sqlalchemy.ext.asyncio import AsyncSession

from modules.catalog.application.services.product import ProductService
from modules.catalog.infrastructure.repositories import ProductRepository


def get_product_repository(
    session: AsyncSession = Depends(database_helper.session_getter),
):
    return ProductRepository(session=session)


def get_product_service(
    session: AsyncSession = Depends(database_helper.session_getter),
    product_repository: ProductRepository = Depends(get_product_repository)
):
    return ProductService(session=session, product_repository=product_repository)
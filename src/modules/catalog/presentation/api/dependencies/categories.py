from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from infra import database_helper

from modules.catalog.application.services.category import CategoryService
from modules.catalog.infrastructure.repositories import CategoryRepository


def get_category_repository(
    session: AsyncSession = Depends(database_helper.get_session)
):
    return CategoryRepository(session=session)


def get_category_service(
    session: AsyncSession = Depends(database_helper.get_session),
    category_repository: CategoryRepository = Depends(get_category_repository),
):
    return CategoryService(session=session, category_repository=category_repository)

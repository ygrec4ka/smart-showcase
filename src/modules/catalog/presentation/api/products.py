from typing import Optional
from uuid import UUID

from fastapi import APIRouter, Depends, status, HTTPException, Query

from core.config import settings
from modules.catalog.application.services import ProductService
from modules.catalog.presentation.api.dependencies import get_product_service
from modules.catalog.presentation.schemas.products import (
    ProductCreate,
    ProductResponse,
    ProductUpdate,
    PaginatedProductResponse,
)

router = APIRouter(
    prefix=settings.api.products,
    tags=["Products"],
)


@router.post(
    "/",
    response_model=ProductResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Создать новый товар",
)
async def create_product(
    data: ProductCreate,
    company_id: UUID = Depends(...),
    product_service: ProductService = Depends(get_product_service),
):
    return await product_service.create_product(
        company_id=company_id,
        data=data,
    )


@router.get(
    "/{product_id}",
    response_model=ProductResponse,
    summary="Получить товар по ID",
)
async def get_product(
    product_id: UUID,
    company_id: UUID = Depends(...),
    product_service: ProductService = Depends(get_product_service),
):
    product = await product_service.get_product_by_id(
        product_id=product_id, company_id=company_id
    )

    if not product:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Товар не найден"
        )

    return product


@router.get(
    "/",
    response_model=PaginatedProductResponse,
    summary="Получить список товаров",
)
async def list_products(
    limit: int = Query(20, ge=1, le=100, description="Количество товаров на странице"),
    cursor: Optional[str] = Query(None, description="Base64 курсор для пагинации"),
    category_id: Optional[UUID] = Query(None, description="Фильтр по категории"),
    company_id: UUID = Depends(...),
    product_service: ProductService = Depends(get_product_service),
):
    try:
        page_data = await product_service.get_catalog_page(
            company_id=company_id,
            limit=limit,
            cursor_b64=cursor,
            category_id=category_id,
        )
        return page_data
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@router.patch("/{product_id}", response_model=ProductResponse, summary="Обновить товар")
async def update_product(
    product_id: UUID,
    data: ProductUpdate,
    company_id: UUID = Depends(...),
    product_service: ProductService = Depends(get_product_service),
):
    product = await product_service.update_product(
        product_id=product_id, company_id=company_id, data=data
    )

    if not product:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Товар не найден или у вас нет прав на его редактирование",
        )

    return product


@router.delete(
    "/{product_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Деактивировать товар (Soft Delete)",
)
async def deactivate_product(
    product_id: UUID,
    company_id: UUID = Depends(...),
    product_service: ProductService = Depends(get_product_service),
):

    product = await product_service.get_product_by_id(
        product_id=product_id, company_id=company_id
    )
    if not product:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Товар не найден"
        )

    await product_service.deactivate_product(
        product_id=product_id, company_id=company_id
    )

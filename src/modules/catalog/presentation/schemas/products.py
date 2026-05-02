from datetime import datetime
from decimal import Decimal
from typing import Optional, List
from uuid import UUID
from pydantic import BaseModel, ConfigDict


class ProductBase(BaseModel):
    title: str
    description: Optional[str] = None
    base_price: Decimal
    category_id: UUID


class ProductCreate(ProductBase):
    pass


class ProductUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    base_price: Optional[Decimal] = None


class ProductResponse(ProductBase):
    id: UUID
    sku: str
    is_active: bool
    created_at: datetime
    updated_at: Optional[datetime] = None

    model_config = ConfigDict(from_attributes=True)


class PaginatedProductResponse(BaseModel):
    items: List[ProductResponse]
    next_cursor: Optional[str]
    has_more: bool

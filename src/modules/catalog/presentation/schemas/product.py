from datetime import datetime
from decimal import Decimal
from typing import Optional, List
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field


class ProductBase(BaseModel):
    title: str = Field(..., max_length=512)
    description: Optional[str] = Field(None, max_length=2000)
    base_price: Decimal = Field(..., ge=0)
    category_id: Optional[UUID] = None


class ProductCreate(ProductBase):
    sku: str = Field(..., max_length=100)
    stock_quantity: int = Field(default=0, ge=0)
    is_active: bool = True


class ProductUpdate(BaseModel):
    title: Optional[str] = Field(None, max_length=512)
    description: Optional[str] = Field(None, max_length=2000)
    base_price: Optional[Decimal] = Field(None, ge=0)
    category_id: Optional[UUID] = None
    sku: Optional[str] = Field(None, max_length=100)
    stock_quantity: Optional[int] = Field(None, ge=0)
    is_active: Optional[bool] = None


class ProductResponse(ProductBase):
    id: UUID
    sku: str
    stock_quantity: int
    is_active: bool
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)


class PaginatedProductResponse(BaseModel):
    items: List[ProductResponse]
    next_cursor: Optional[str] = None
    has_more: bool

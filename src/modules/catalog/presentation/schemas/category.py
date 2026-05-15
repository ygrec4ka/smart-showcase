from datetime import datetime
from typing import Optional
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field


class CategoryCreate(BaseModel):
    name: str = Field(..., max_length=255, description="Название категории")
    slug: str = Field(..., max_length=255, description="Slug (URL) категории")
    is_active: bool = Field(default=True, description="Активна ли категория")


class CategoryUpdate(BaseModel):
    name: Optional[str] = Field(None, max_length=255)
    slug: Optional[str] = Field(None, max_length=255)
    is_active: Optional[bool] = None


class CategoryResponse(BaseModel):
    id: UUID
    name: str
    slug: str
    is_active: bool
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)

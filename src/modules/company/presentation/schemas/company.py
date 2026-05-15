from datetime import datetime
from typing import Optional
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field


class CompanyCreate(BaseModel):
    name: str = Field(..., max_length=255, description="Название компании")


class CompanyUpdate(BaseModel):
    name: Optional[str] = Field(None, max_length=255, description="Название компании")


class CompanyResponse(BaseModel):
    id: UUID
    name: str
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)

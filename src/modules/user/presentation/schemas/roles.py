from typing import Optional, List
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field


class RoleCreate(BaseModel):
    name: str = Field(
        ..., max_length=100, description="Название роли (например, Manager)"
    )
    permissions: List[str] = Field(
        default_factory=list,
        description="Список прав (например, ['create_product', 'read_users'])",
    )


class RoleUpdate(BaseModel):
    name: Optional[str] = Field(None, max_length=100)
    permissions: Optional[List[str]] = None


class RoleResponse(BaseModel):
    id: UUID
    name: str
    permissions: List[str]
    company_id: Optional[UUID]

    model_config = ConfigDict(from_attributes=True)

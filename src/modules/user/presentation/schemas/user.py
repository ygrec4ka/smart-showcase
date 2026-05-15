from datetime import datetime
from typing import Any, Optional
from uuid import UUID

from pydantic import BaseModel, ConfigDict, EmailStr, Field

from modules.user.domain.entities.user import UserStatus


class UserCreateByAdmin(BaseModel):
    email: EmailStr
    password: str = Field(..., min_length=8, description="Сырой пароль")
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    phone: Optional[str] = None
    position: Optional[str] = None
    role_id: UUID


class UserUpdate(BaseModel):
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    phone: Optional[str] = None
    preferences: Optional[dict[str, Any]] = None


class UserUpdateByAdmin(BaseModel):
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    phone: Optional[str] = None
    position: Optional[str] = None
    status: Optional[UserStatus] = None
    role_id: Optional[UUID] = None


class UserResponse(BaseModel):
    id: UUID
    email: EmailStr
    first_name: Optional[str]
    last_name: Optional[str]
    phone: Optional[str]
    position: Optional[str]
    status: UserStatus
    preferences: dict[str, Any]
    company_id: UUID
    role_id: UUID
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)

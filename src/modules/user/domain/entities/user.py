import enum
from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional, Any
from uuid import UUID

import uuid6


class UserStatus(str, enum.Enum):
    ACTIVE = "active"
    INACTIVE = "inactive"
    BANNED = "banned"


@dataclass
class User:
    email: str
    hashed_password: str
    created_at: datetime
    company_id: Optional[UUID] = None
    role_id: Optional[UUID] = None
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    phone: Optional[str] = None
    position: Optional[str] = None
    status: UserStatus = UserStatus.ACTIVE
    preferences: dict[str, Any] = field(default_factory=dict)
    id: UUID = field(default_factory=uuid6.uuid7)

from dataclasses import dataclass, field
from typing import Optional
from uuid import UUID

import uuid6


@dataclass
class Role:
    name: str
    company_id: Optional[UUID] = None
    permissions: list[str] = field(default_factory=list)
    id: UUID = field(default_factory=uuid6.uuid7)

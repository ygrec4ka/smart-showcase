from dataclasses import dataclass, field
from datetime import datetime
from uuid import UUID
import uuid6


@dataclass
class Category:
    name: str
    slug: str
    company_id: UUID
    created_at: datetime
    updated_at: datetime
    id: UUID = field(default_factory=uuid6.uuid7)
    is_active: bool = True

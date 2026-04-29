from dataclasses import dataclass, field
from uuid import UUID
import uuid6


@dataclass
class Category:
    name: str
    company_id: UUID
    parent_id: UUID | None = None
    id: UUID = field(default_factory=uuid6.uuid7)

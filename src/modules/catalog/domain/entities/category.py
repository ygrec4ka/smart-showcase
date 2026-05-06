from dataclasses import dataclass, field
from uuid import UUID
import uuid6


@dataclass
class Category:
    name: str
    company_id: UUID
    id: UUID = field(default_factory=uuid6.uuid7)

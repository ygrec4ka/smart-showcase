from dataclasses import dataclass, field
from datetime import datetime
from uuid import UUID
import uuid6


@dataclass
class Company:
    name: str
    created_at: datetime
    updated_at: datetime
    id: UUID = field(default_factory=uuid6.uuid7)

from dataclasses import dataclass, field
from decimal import Decimal
from typing import Optional
from uuid import UUID
import uuid6
from datetime import datetime


@dataclass
class Product:
    title: str
    sku: str
    base_price: Decimal
    company_id: UUID
    category_id: UUID
    created_at: datetime
    id: UUID = field(default_factory=uuid6.uuid7)
    description: Optional[str] = None
    is_active: bool = True

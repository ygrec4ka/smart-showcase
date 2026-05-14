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
    created_at: datetime
    updated_at: datetime
    id: UUID = field(default_factory=uuid6.uuid7)
    category_id: Optional[UUID] = None
    description: Optional[str] = None
    stock_quantity: int = 0
    is_active: bool = True

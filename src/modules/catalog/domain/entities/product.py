from dataclasses import dataclass, field
from decimal import Decimal
from typing import Optional
from uuid import UUID, uuid4


@dataclass
class Product:
    title: str
    sku: str
    base_price: Decimal
    company_id: UUID
    category_id: UUID
    id: UUID = field(default_factory=uuid4)
    description: Optional[str] = None
    is_active: bool = True

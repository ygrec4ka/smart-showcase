from dataclasses import dataclass, field
from decimal import Decimal
from uuid import UUID, uuid4


@dataclass
class Product:
    title: str
    sku: str
    base_price: Decimal
    company_id: UUID
    category_id: UUID
    id: UUID = field(default_factory=uuid4)
    description: str | None = None
    is_active: bool = True


@dataclass
class ProductFilter:
    company_id: UUID
    limit: int = 20
    offset: int = 0
    category_id: UUID | None = None
    is_active: bool = True


@dataclass
class Category:
    name: str
    company_id: UUID
    parent_id: UUID | None = None
    id: UUID = field(default_factory=uuid4)

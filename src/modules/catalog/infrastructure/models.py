import uuid
from decimal import Decimal

from sqlalchemy import String, Numeric, ForeignKey

from infra.base import Base, TenantBase

from sqlalchemy.dialects.postgresql import UUID as PG_UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship


class CategoryTable(TenantBase, Base):
    __tablename__ = "categories"

    id: Mapped[uuid.UUID] = mapped_column(
        PG_UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
    )
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    parent_id: Mapped[uuid.UUID | None] = mapped_column(
        PG_UUID(as_uuid=True), ForeignKey("categories.id", ondelete="SET NULL")
    )
    products: Mapped[list["ProductTable"]] = relationship(back_populates="category")


class ProductTable(TenantBase, Base):
    __tablename__ = "products"

    id: Mapped[uuid.UUID] = mapped_column(
        PG_UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
    )
    title: Mapped[str] = mapped_column(String(512), nullable=False)
    description: Mapped[str | None] = mapped_column(String(2000))
    sku: Mapped[str] = mapped_column(String(100), nullable=False)
    base_price: Mapped[Decimal] = mapped_column(Numeric(12, 2), nullable=False)
    is_active: Mapped[bool] = mapped_column(default=True)

    category: Mapped["CategoryTable"] = relationship(back_populates="products")
    category_id: Mapped[uuid.UUID] = mapped_column(
        PG_UUID(as_uuid=True), ForeignKey("categories.id", ondelete="CASCADE")
    )

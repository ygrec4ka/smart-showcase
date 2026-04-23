import uuid
from typing import TYPE_CHECKING

from sqlalchemy import String, ForeignKey

from infra.base import Base, TenantBase

from sqlalchemy.dialects.postgresql import UUID as PG_UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

if TYPE_CHECKING:
    from .product import ProductTable


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

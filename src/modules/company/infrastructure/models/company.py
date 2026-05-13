import uuid
from datetime import datetime
from typing import TYPE_CHECKING

from sqlalchemy import String, DateTime, func
from sqlalchemy.dialects.postgresql import UUID as PG_UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from infra.base import Base

if TYPE_CHECKING:
    from modules.user.infrastructure.models import UserTable
    from modules.catalog.infrastructure.models import ProductTable, CategoryTable


class CompanyTable(Base):
    __tablename__ = "companies"

    id: Mapped[uuid.UUID] = mapped_column(
        PG_UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
    )

    name: Mapped[str] = mapped_column(String(255), index=True, nullable=False)

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False,
    )

    users: Mapped[list["UserTable"]] = relationship(
        "UserTable",
        back_populates="company",
        cascade="all, delete-orphan",
    )

    categories: Mapped[list["CategoryTable"]] = relationship(
        back_populates="company",
        cascade="all, delete-orphan",
    )
    products: Mapped[list["ProductTable"]] = relationship(
        back_populates="company",
        cascade="all, delete-orphan",
    )

import enum
import uuid
from datetime import datetime
from typing import TYPE_CHECKING, Any

from sqlalchemy import String, DateTime, func, ForeignKey, Enum as SQLEnum
from sqlalchemy.dialects.postgresql import UUID as PG_UUID, JSONB
from sqlalchemy.orm import Mapped, mapped_column, relationship

from infra.base import Base, TenantBase

if TYPE_CHECKING:
    from modules.user.infrastructure.models import RoleTable
    from modules.company.infrastructure.models import CompanyTable


class UserStatus(str, enum.Enum):
    ACTIVE = "active"
    INACTIVE = "inactive"
    BANNED = "banned"


class UserTable(Base, TenantBase):
    __tablename__ = "users"

    id: Mapped[uuid.UUID] = mapped_column(
        PG_UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
    )
    email: Mapped[str] = mapped_column(
        String(255), unique=True, index=True, nullable=False
    )
    hashed_password: Mapped[str] = mapped_column(String(255), nullable=False)

    first_name: Mapped[str | None] = mapped_column(String(100), nullable=True)
    last_name: Mapped[str | None] = mapped_column(String(100), nullable=True)
    phone: Mapped[str | None] = mapped_column(String(20), nullable=True)

    position: Mapped[str | None] = mapped_column(String(100), nullable=True)
    status: Mapped[UserStatus] = mapped_column(
        SQLEnum(UserStatus, native_enum=False),
        default=UserStatus.ACTIVE,
        nullable=False,
    )
    preferences: Mapped[dict[str, Any]] = mapped_column(
        JSONB,
        default=dict,
        server_default="{}",
        nullable=False,
    )

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

    company_id: Mapped[uuid.UUID | None] = mapped_column(
        PG_UUID(as_uuid=True),
        ForeignKey("companies.id", ondelete="SET NULL"),
        nullable=True,
    )
    company: Mapped["CompanyTable"] = relationship(
        back_populates="users",
    )

    role_id: Mapped[uuid.UUID | None] = mapped_column(
        PG_UUID(as_uuid=True),
        ForeignKey("roles.id", ondelete="SET NULL"),
        nullable=True,
    )
    role: Mapped["RoleTable"] = relationship("RoleTable", back_populates="users")

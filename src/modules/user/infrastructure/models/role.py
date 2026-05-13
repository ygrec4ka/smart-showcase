import uuid
from typing import TYPE_CHECKING, Any

from sqlalchemy import String
from sqlalchemy.dialects.postgresql import UUID as PG_UUID, JSONB
from sqlalchemy.orm import Mapped, mapped_column, relationship

from infra.base import Base, TenantBase

if TYPE_CHECKING:
    from modules.user.infrastructure.models import UserTable


class RoleTable(Base, TenantBase):
    __tablename__ = "roles"

    id: Mapped[uuid.UUID] = mapped_column(
        PG_UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
    )

    name: Mapped[str] = mapped_column(String(100), nullable=False)

    permissions: Mapped[list[str]] = mapped_column(
        JSONB,
        default=list,
        server_default="[]",
        nullable=False,
    )

    users: Mapped[list["UserTable"]] = relationship(
        back_populates="role",
    )

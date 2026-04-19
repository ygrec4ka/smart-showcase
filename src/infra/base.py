import uuid

from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy.dialects.postgresql import UUID as PG_UUID


class Base(DeclarativeBase):
    """Единая декларативная база для всего проекта"""

    pass


class TenantBase(Base):
    """Базовый класс для всех мультитенантных таблиц"""

    __abstract__ = True

    company_id: Mapped[uuid.UUID] = mapped_column(
        PG_UUID(as_uuid=True),
        index=True,
        nullable=False,
    )

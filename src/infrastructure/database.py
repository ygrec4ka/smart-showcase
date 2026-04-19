from typing import AsyncGenerator

from sqlalchemy.ext.asyncio import (
    create_async_engine,
    AsyncEngine,
    async_sessionmaker,
    AsyncSession,
)


class DatabaseHelper:
    def __init__(
        self,
        url: str,
        echo: bool = False,
        echo_pool: int = 5,
        max_overflow: int = 10,
    ) -> None:
        self.engine: AsyncEngine = create_async_engine(
            url=url,
            echo=echo,
            echo_pool=echo_pool,
            max_overflow=max_overflow,
        )
        self.session_factory = async_sessionmaker(
            bind=self.engine,
            expire_on_commit=False,
            autocommit=False,
            autoflush=False,
        )

    async def dispose(self):
        """Close all connections to database"""
        await self.engine.dispose()

    async def session_getter(self) -> AsyncGenerator[AsyncSession, None]:
        """Dependency for FastAPI"""
        async with self.session_factory() as session:
            try:
                yield session
            finally:
                await session.close()


database_helper = DatabaseHelper(
    url=str(settings.url),
    echo=settings.echo,
    echo_pool=settings.echo_pool,
    max_overflow=settings.max_overflow,
)

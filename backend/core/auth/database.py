from typing import AsyncGenerator

from sqlalchemy.ext.asyncio import AsyncSession

from core.database import async_session_maker


async def get_async_session() -> AsyncGenerator[AsyncSession, None]:
    """Dependency for getting async database sessions."""
    async with async_session_maker() as session:
        try:
            yield session
            await session.commit()
        except Exception:
            await session.rollback()
            raise

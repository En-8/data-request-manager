from sqlalchemy.ext.asyncio import AsyncSession


class BaseRepository:
    """Base repository class with session dependency injection."""

    def __init__(self, session: AsyncSession) -> None:
        self.session = session

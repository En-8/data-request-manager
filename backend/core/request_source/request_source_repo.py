from sqlalchemy import select

from core.repository import BaseRepository
from core.request_source.request_source import RequestSource
from core.request_source.request_source_model import RequestSourceModel


class RequestSourceRepository(BaseRepository):
    """Repository for request source data access."""

    async def get_all(self) -> list[RequestSource]:
        """Load all request sources from the database."""
        stmt = select(RequestSourceModel).order_by(RequestSourceModel.name)
        result = await self.session.execute(stmt)
        rows = result.scalars().all()

        return [
            RequestSource(
                id=row.id,
                name=row.name,
            )
            for row in rows
        ]

    async def get_by_id(self, request_source_id: str) -> RequestSource | None:
        """Get a request source by its ID."""
        stmt = select(RequestSourceModel).where(
            RequestSourceModel.id == request_source_id
        )
        result = await self.session.execute(stmt)
        row = result.scalar_one_or_none()

        if row is None:
            return None

        return RequestSource(
            id=row.id,
            name=row.name,
        )

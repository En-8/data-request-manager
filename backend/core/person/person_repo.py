from sqlalchemy import select

from core.person.person import Person
from core.person.person_model import PersonModel
from core.repository import BaseRepository


class PersonRepository(BaseRepository):
    """Repository for person data access."""

    async def get_all(self) -> list[Person]:
        """Load all people from the database."""
        stmt = select(PersonModel).order_by(
            PersonModel.last_name, PersonModel.first_name
        )
        result = await self.session.execute(stmt)
        rows = result.scalars().all()

        return [
            Person(
                id=row.id,
                first_name=row.first_name,
                last_name=row.last_name,
                date_of_birth=row.date_of_birth,
            )
            for row in rows
        ]

    async def get_by_id(self, person_id: int) -> Person | None:
        """Get a person by their ID."""
        stmt = select(PersonModel).where(PersonModel.id == person_id)
        result = await self.session.execute(stmt)
        row = result.scalar_one_or_none()

        if row is None:
            return None

        return Person(
            id=row.id,
            first_name=row.first_name,
            last_name=row.last_name,
            date_of_birth=row.date_of_birth,
        )

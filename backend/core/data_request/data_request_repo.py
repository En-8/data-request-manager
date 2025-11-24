from datetime import datetime

from sqlalchemy import select

from core.data_request.data_request import DataRequest, Status
from core.data_request.data_request_model import DataRequestModel
from core.person.person import Person
from core.repository import BaseRepository


class DataRequestRepository(BaseRepository):
    """Repository for data request data access."""

    async def get_all(self) -> list[DataRequest]:
        """Load all data requests from the database."""
        stmt = select(DataRequestModel).order_by(DataRequestModel.id)
        result = await self.session.execute(stmt)
        rows = result.scalars().all()

        return [
            DataRequest(
                id=row.id,
                person_id=row.person_id,
                first_name=row.first_name,
                last_name=row.last_name,
                date_of_birth=row.date_of_birth,
                status=Status(row.status),
                created_on=row.created_on,
                created_by=row.created_by,
                request_source_id=row.request_source_id,
            )
            for row in rows
        ]

    async def create(
        self,
        person: Person,
        request_source_id: str,
        created_by: str,
    ) -> DataRequest:
        """Create a new data request in the database."""
        model = DataRequestModel(
            person_id=person.id,
            first_name=person.first_name,
            last_name=person.last_name,
            date_of_birth=person.date_of_birth,
            status=Status.PROCESSING,
            created_on=datetime.now(),
            created_by=created_by,
            request_source_id=request_source_id,
        )

        self.session.add(model)
        await self.session.flush()
        await self.session.refresh(model)

        return DataRequest(
            id=model.id,
            person_id=model.person_id,
            first_name=model.first_name,
            last_name=model.last_name,
            date_of_birth=model.date_of_birth,
            status=Status(model.status),
            created_on=model.created_on,
            created_by=model.created_by,
            request_source_id=model.request_source_id,
        )

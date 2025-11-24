from core.data_request.data_request import DataRequest
from core.data_request.data_request_repo import DataRequestRepository
from core.person.person_repo import PersonRepository


class PersonNotFoundError(ValueError):
    """Raised when a person is not found in the database."""

    pass


class DataRequestService:
    """Service for data request business logic."""

    def __init__(
        self,
        data_request_repo: DataRequestRepository,
        person_repo: PersonRepository,
    ) -> None:
        self.data_request_repo = data_request_repo
        self.person_repo = person_repo

    async def create_data_request(
        self,
        person_id: int,
        request_source_id: str,
        created_by: str = "demo_user",
    ) -> DataRequest:
        """Create a new data request.

        Validates that the person exists before creating the request.

        Raises:
            PersonNotFoundError: If the person with the given ID does not exist.
        """
        person = await self.person_repo.get_by_id(person_id)
        if person is None:
            raise PersonNotFoundError(f"Person with id {person_id} not found")

        return await self.data_request_repo.create(
            person=person,
            request_source_id=request_source_id,
            created_by=created_by,
        )

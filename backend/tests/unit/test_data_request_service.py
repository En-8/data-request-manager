from datetime import date, datetime
from unittest.mock import AsyncMock, MagicMock

import pytest

from core.data_request import (
    DataRequest,
    DataRequestService,
    PersonNotFoundError,
    Status,
)
from core.person import Person


class TestDataRequestService:
    """Unit tests for DataRequestService with mocked repositories."""

    @pytest.fixture
    def mock_person_repo(self) -> MagicMock:
        """Create a mock PersonRepository."""
        return MagicMock()

    @pytest.fixture
    def mock_data_request_repo(self) -> MagicMock:
        """Create a mock DataRequestRepository."""
        return MagicMock()

    @pytest.fixture
    def service(
        self, mock_data_request_repo: MagicMock, mock_person_repo: MagicMock
    ) -> DataRequestService:
        """Create a DataRequestService with mocked dependencies."""
        return DataRequestService(mock_data_request_repo, mock_person_repo)

    @pytest.fixture
    def sample_person(self) -> Person:
        """Create a sample person for testing."""
        return Person(
            id=1,
            first_name="John",
            last_name="Smith",
            date_of_birth=date(1985, 3, 15),
        )

    @pytest.fixture
    def sample_data_request(self) -> DataRequest:
        """Create a sample data request for testing."""
        return DataRequest(
            id=1,
            person_id=1,
            first_name="John",
            last_name="Smith",
            date_of_birth=date(1985, 3, 15),
            status=Status.PROCESSING,
            created_on=datetime(2024, 1, 15, 9, 30, 0),
            created_by="test@example.com",
            request_source_id="acme-corp",
        )

    @pytest.mark.asyncio
    async def test_create_data_request_success(
        self,
        service: DataRequestService,
        mock_person_repo: MagicMock,
        mock_data_request_repo: MagicMock,
        sample_person: Person,
        sample_data_request: DataRequest,
    ) -> None:
        """Test successful creation of a data request."""
        mock_person_repo.get_by_id = AsyncMock(return_value=sample_person)
        mock_data_request_repo.create = AsyncMock(return_value=sample_data_request)

        result = await service.create_data_request(
            person_id=1,
            request_source_id="acme-corp",
            created_by="test@example.com",
        )

        assert result == sample_data_request
        mock_person_repo.get_by_id.assert_called_once_with(1)
        mock_data_request_repo.create.assert_called_once_with(
            person=sample_person,
            request_source_id="acme-corp",
            created_by="test@example.com",
        )

    @pytest.mark.asyncio
    async def test_create_data_request_person_not_found(
        self,
        service: DataRequestService,
        mock_person_repo: MagicMock,
        mock_data_request_repo: MagicMock,
    ) -> None:
        """Test that PersonNotFoundError is raised when person doesn't exist."""
        mock_person_repo.get_by_id = AsyncMock(return_value=None)

        with pytest.raises(PersonNotFoundError) as exc_info:
            await service.create_data_request(
                person_id=9999,
                request_source_id="acme-corp",
                created_by="test@example.com",
            )

        assert "Person with id 9999 not found" in str(exc_info.value)
        mock_person_repo.get_by_id.assert_called_once_with(9999)
        mock_data_request_repo.create.assert_not_called()

    @pytest.mark.asyncio
    async def test_create_data_request_uses_default_created_by(
        self,
        service: DataRequestService,
        mock_person_repo: MagicMock,
        mock_data_request_repo: MagicMock,
        sample_person: Person,
        sample_data_request: DataRequest,
    ) -> None:
        """Test that default created_by value is used when not provided."""
        mock_person_repo.get_by_id = AsyncMock(return_value=sample_person)
        mock_data_request_repo.create = AsyncMock(return_value=sample_data_request)

        await service.create_data_request(
            person_id=1,
            request_source_id="acme-corp",
        )

        mock_data_request_repo.create.assert_called_once_with(
            person=sample_person,
            request_source_id="acme-corp",
            created_by="demo_user",
        )

    @pytest.mark.asyncio
    async def test_create_data_request_passes_person_to_repo(
        self,
        service: DataRequestService,
        mock_person_repo: MagicMock,
        mock_data_request_repo: MagicMock,
        sample_data_request: DataRequest,
    ) -> None:
        """Test that the person object is passed correctly to the repository."""
        custom_person = Person(
            id=5,
            first_name="Jane",
            last_name="Doe",
            date_of_birth=date(1990, 6, 20),
        )
        mock_person_repo.get_by_id = AsyncMock(return_value=custom_person)
        mock_data_request_repo.create = AsyncMock(return_value=sample_data_request)

        await service.create_data_request(
            person_id=5,
            request_source_id="globex-inc",
            created_by="admin@example.com",
        )

        mock_data_request_repo.create.assert_called_once_with(
            person=custom_person,
            request_source_id="globex-inc",
            created_by="admin@example.com",
        )


class TestStatus:
    """Unit tests for the Status enum."""

    def test_status_values(self) -> None:
        """Test that status enum values are correct."""
        assert Status.CREATED == 1
        assert Status.PROCESSING == 2
        assert Status.NEEDS_REVIEW == 3
        assert Status.COMPLETE == 99

    def test_status_from_int(self) -> None:
        """Test that status enum can be created from integers."""
        assert Status(1) == Status.CREATED
        assert Status(2) == Status.PROCESSING
        assert Status(3) == Status.NEEDS_REVIEW
        assert Status(99) == Status.COMPLETE


class TestDataRequestDataclass:
    """Unit tests for the DataRequest dataclass."""

    def test_create_data_request(self) -> None:
        """Test that DataRequest dataclass can be instantiated correctly."""
        created_on = datetime(2024, 1, 15, 9, 30, 0)
        data_request = DataRequest(
            id=1,
            person_id=1,
            first_name="John",
            last_name="Smith",
            date_of_birth=date(1985, 3, 15),
            status=Status.CREATED,
            created_on=created_on,
            created_by="admin@example.com",
            request_source_id="acme-corp",
        )

        assert data_request.id == 1
        assert data_request.person_id == 1
        assert data_request.first_name == "John"
        assert data_request.last_name == "Smith"
        assert data_request.date_of_birth == date(1985, 3, 15)
        assert data_request.status == Status.CREATED
        assert data_request.created_on == created_on
        assert data_request.created_by == "admin@example.com"
        assert data_request.request_source_id == "acme-corp"


class TestPersonDataclass:
    """Unit tests for the Person dataclass."""

    def test_create_person(self) -> None:
        """Test that Person dataclass can be instantiated correctly."""
        person = Person(
            id=1,
            first_name="John",
            last_name="Smith",
            date_of_birth=date(1985, 3, 15),
        )

        assert person.id == 1
        assert person.first_name == "John"
        assert person.last_name == "Smith"
        assert person.date_of_birth == date(1985, 3, 15)

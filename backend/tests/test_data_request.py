from datetime import date, datetime

import pytest
from httpx import ASGITransport, AsyncClient

from core import (
    DataRequest,
    Person,
    RequestSource,
    Status,
    create_data_request,
    get_all_data_requests,
    get_all_people,
    get_all_request_sources,
)
from main import app


@pytest.fixture(scope="module")
async def client():
    """Shared async client for all tests in this module."""
    async with AsyncClient(
        transport=ASGITransport(app=app), base_url="http://test"
    ) as c:
        yield c


@pytest.fixture(scope="module")
async def auth_headers(client: AsyncClient) -> dict:
    """Shared auth headers for authenticated endpoint tests."""
    # Register user
    await client.post(
        "/api/v1/auth/register",
        json={
            "email": "endpoint_test@example.com",
            "password": "testpassword123",
        },
    )

    # Login and get token
    login_response = await client.post(
        "/api/v1/auth/jwt/login",
        data={
            "username": "endpoint_test@example.com",
            "password": "testpassword123",
        },
    )
    token = login_response.json()["access_token"]
    return {"Authorization": f"Bearer {token}"}


class TestStatus:
    def test_status_values(self) -> None:
        assert Status.CREATED == 1
        assert Status.PROCESSING == 2
        assert Status.NEEDS_REVIEW == 3
        assert Status.COMPLETE == 99

    def test_status_from_int(self) -> None:
        assert Status(1) == Status.CREATED
        assert Status(2) == Status.PROCESSING
        assert Status(3) == Status.NEEDS_REVIEW
        assert Status(99) == Status.COMPLETE


class TestPerson:
    def test_create_person(self) -> None:
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


class TestDataRequest:
    def test_create_data_request(self) -> None:
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

    def test_data_request_status_is_int_enum(self) -> None:
        data_request = DataRequest(
            id=1,
            person_id=1,
            first_name="Test",
            last_name="User",
            date_of_birth=date(1990, 1, 1),
            status=Status.PROCESSING,
            created_on=datetime.now(),
            created_by="test@example.com",
            request_source_id="test-corp",
        )

        # Status should be usable as an int
        assert data_request.status == 2
        assert int(data_request.status) == 2


class TestGetAllDataRequests:
    @pytest.mark.asyncio
    async def test_returns_list_of_data_requests(self) -> None:
        data_requests = await get_all_data_requests()

        assert isinstance(data_requests, list)
        assert len(data_requests) > 0
        assert all(isinstance(dr, DataRequest) for dr in data_requests)

    @pytest.mark.asyncio
    async def test_data_requests_have_correct_types(self) -> None:
        data_requests = await get_all_data_requests()

        for dr in data_requests:
            assert isinstance(dr.id, int)
            assert isinstance(dr.person_id, int)
            assert isinstance(dr.first_name, str)
            assert isinstance(dr.last_name, str)
            assert isinstance(dr.date_of_birth, date)
            assert isinstance(dr.status, Status)
            assert isinstance(dr.created_on, datetime)
            assert isinstance(dr.created_by, str)
            assert isinstance(dr.request_source_id, str)

    @pytest.mark.asyncio
    async def test_loads_expected_test_data(self) -> None:
        data_requests = await get_all_data_requests()

        # Verify we have the expected number of test records
        assert len(data_requests) == 6

        # Verify first record matches expected data
        first = data_requests[0]
        assert first.id == 1
        assert first.person_id == 1
        assert first.first_name == "John"
        assert first.last_name == "Smith"
        assert first.date_of_birth == date(1985, 3, 15)
        assert first.status == Status.CREATED
        assert first.request_source_id == "acme-corp"

    @pytest.mark.asyncio
    async def test_contains_all_status_types(self) -> None:
        data_requests = await get_all_data_requests()
        statuses = {dr.status for dr in data_requests}

        assert Status.CREATED in statuses
        assert Status.PROCESSING in statuses
        assert Status.NEEDS_REVIEW in statuses
        assert Status.COMPLETE in statuses


class TestGetDataRequestsEndpoint:
    @pytest.mark.asyncio
    async def test_get_all_data_requests(
        self, client: AsyncClient, auth_headers: dict
    ) -> None:
        response = await client.get("/api/v1/data-requests", headers=auth_headers)

        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)
        assert len(data) >= 6  # At least the seeded data

    @pytest.mark.asyncio
    async def test_filter_by_status_created(
        self, client: AsyncClient, auth_headers: dict
    ) -> None:
        response = await client.get(
            "/api/v1/data-requests?status=1", headers=auth_headers
        )

        assert response.status_code == 200
        data = response.json()
        assert all(item["status"] == 1 for item in data)

    @pytest.mark.asyncio
    async def test_filter_by_status_processing(
        self, client: AsyncClient, auth_headers: dict
    ) -> None:
        response = await client.get(
            "/api/v1/data-requests?status=2", headers=auth_headers
        )

        assert response.status_code == 200
        data = response.json()
        assert all(item["status"] == 2 for item in data)

    @pytest.mark.asyncio
    async def test_filter_by_status_needs_review(
        self, client: AsyncClient, auth_headers: dict
    ) -> None:
        response = await client.get(
            "/api/v1/data-requests?status=3", headers=auth_headers
        )

        assert response.status_code == 200
        data = response.json()
        assert all(item["status"] == 3 for item in data)

    @pytest.mark.asyncio
    async def test_filter_by_status_complete(
        self, client: AsyncClient, auth_headers: dict
    ) -> None:
        response = await client.get(
            "/api/v1/data-requests?status=99", headers=auth_headers
        )

        assert response.status_code == 200
        data = response.json()
        assert all(item["status"] == 99 for item in data)

    @pytest.mark.asyncio
    async def test_filter_by_invalid_status_returns_empty(
        self, client: AsyncClient, auth_headers: dict
    ) -> None:
        response = await client.get(
            "/api/v1/data-requests?status=999", headers=auth_headers
        )

        assert response.status_code == 200
        data = response.json()
        assert data == []

    @pytest.mark.asyncio
    async def test_filter_returns_correct_count(
        self, client: AsyncClient, auth_headers: dict
    ) -> None:
        # Get counts for each status from unfiltered data
        all_response = await client.get("/api/v1/data-requests", headers=auth_headers)
        all_data = all_response.json()

        for status_value in [1, 2, 3, 99]:
            expected_count = sum(
                1 for item in all_data if item["status"] == status_value
            )
            filtered_response = await client.get(
                f"/api/v1/data-requests?status={status_value}", headers=auth_headers
            )
            filtered_data = filtered_response.json()
            assert len(filtered_data) == expected_count


class TestRequestSource:
    def test_create_request_source(self) -> None:
        request_source = RequestSource(
            id="test-corp",
            name="Test Corporation",
        )

        assert request_source.id == "test-corp"
        assert request_source.name == "Test Corporation"


class TestGetAllRequestSources:
    @pytest.mark.asyncio
    async def test_returns_list_of_request_sources(self) -> None:
        request_sources = await get_all_request_sources()

        assert isinstance(request_sources, list)
        assert len(request_sources) > 0
        assert all(isinstance(rs, RequestSource) for rs in request_sources)

    @pytest.mark.asyncio
    async def test_request_sources_have_correct_types(self) -> None:
        request_sources = await get_all_request_sources()

        for rs in request_sources:
            assert isinstance(rs.id, str)
            assert isinstance(rs.name, str)

    @pytest.mark.asyncio
    async def test_loads_expected_request_sources(self) -> None:
        request_sources = await get_all_request_sources()

        # Verify we have the expected number of request sources
        assert len(request_sources) == 5

        # Verify sources are ordered by name
        names = [rs.name for rs in request_sources]
        assert names == sorted(names)

    @pytest.mark.asyncio
    async def test_contains_known_request_source(self) -> None:
        request_sources = await get_all_request_sources()
        ids = {rs.id for rs in request_sources}

        assert "acme-corp" in ids
        assert "wayne-enterprises" in ids


class TestGetAllPeople:
    @pytest.mark.asyncio
    async def test_returns_list_of_people(self) -> None:
        people = await get_all_people()

        assert isinstance(people, list)
        assert len(people) > 0
        assert all(isinstance(p, Person) for p in people)

    @pytest.mark.asyncio
    async def test_people_have_correct_types(self) -> None:
        people = await get_all_people()

        for p in people:
            assert isinstance(p.id, int)
            assert isinstance(p.first_name, str)
            assert isinstance(p.last_name, str)
            assert isinstance(p.date_of_birth, date)

    @pytest.mark.asyncio
    async def test_loads_expected_people(self) -> None:
        people = await get_all_people()

        # Verify we have the expected number of people
        assert len(people) == 8

        # Verify a known person exists
        john = next((p for p in people if p.id == 1), None)
        assert john is not None
        assert john.first_name == "John"
        assert john.last_name == "Smith"
        assert john.date_of_birth == date(1985, 3, 15)


class TestGetPeopleEndpoint:
    @pytest.mark.asyncio
    async def test_get_all_people(
        self, client: AsyncClient, auth_headers: dict
    ) -> None:
        response = await client.get("/api/v1/people", headers=auth_headers)

        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)
        assert len(data) == 8

    @pytest.mark.asyncio
    async def test_person_has_required_fields(
        self, client: AsyncClient, auth_headers: dict
    ) -> None:
        response = await client.get("/api/v1/people", headers=auth_headers)

        data = response.json()
        for item in data:
            assert "id" in item
            assert "first_name" in item
            assert "last_name" in item
            assert "date_of_birth" in item
            assert isinstance(item["id"], int)
            assert isinstance(item["first_name"], str)
            assert isinstance(item["last_name"], str)
            assert isinstance(item["date_of_birth"], str)


class TestCreateDataRequest:
    @pytest.mark.asyncio
    async def test_creates_data_request_with_correct_values(self) -> None:
        data_request = await create_data_request(
            person_id=1,
            request_source_id="acme-corp",
        )

        assert isinstance(data_request, DataRequest)
        assert data_request.person_id == 1
        assert data_request.first_name == "John"
        assert data_request.last_name == "Smith"
        assert data_request.date_of_birth == date(1985, 3, 15)
        assert data_request.request_source_id == "acme-corp"
        assert data_request.status == Status.PROCESSING
        assert data_request.created_by == "demo_user"
        assert isinstance(data_request.id, int)
        assert isinstance(data_request.created_on, datetime)

    @pytest.mark.asyncio
    async def test_creates_data_request_with_auto_generated_id(self) -> None:
        data_request = await create_data_request(
            person_id=2,
            request_source_id="globex-inc",
        )

        assert data_request.id > 0

    @pytest.mark.asyncio
    async def test_creates_data_request_with_invalid_person_raises_error(self) -> None:
        with pytest.raises(ValueError) as exc_info:
            await create_data_request(
                person_id=9999,
                request_source_id="acme-corp",
            )

        assert "Person with id 9999 not found" in str(exc_info.value)


class TestGetRequestSourcesEndpoint:
    @pytest.mark.asyncio
    async def test_get_all_request_sources(
        self, client: AsyncClient, auth_headers: dict
    ) -> None:
        response = await client.get("/api/v1/request-sources", headers=auth_headers)

        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)
        assert len(data) == 5

    @pytest.mark.asyncio
    async def test_request_source_has_id_and_name(
        self, client: AsyncClient, auth_headers: dict
    ) -> None:
        response = await client.get("/api/v1/request-sources", headers=auth_headers)

        data = response.json()
        for item in data:
            assert "id" in item
            assert "name" in item
            assert isinstance(item["id"], str)
            assert isinstance(item["name"], str)

    @pytest.mark.asyncio
    async def test_contains_known_request_sources(
        self, client: AsyncClient, auth_headers: dict
    ) -> None:
        response = await client.get("/api/v1/request-sources", headers=auth_headers)

        data = response.json()
        ids = {item["id"] for item in data}

        assert "acme-corp" in ids
        assert "globex-inc" in ids
        assert "initech" in ids
        assert "umbrella-corp" in ids
        assert "wayne-enterprises" in ids


class TestPostDataRequestEndpoint:
    @pytest.mark.asyncio
    async def test_create_data_request_success(
        self, client: AsyncClient, auth_headers: dict
    ) -> None:
        response = await client.post(
            "/api/v1/data-requests",
            json={
                "person_id": 1,
                "request_source_id": "acme-corp",
            },
            headers=auth_headers,
        )

        assert response.status_code == 200
        data = response.json()
        assert data["person_id"] == 1
        assert data["first_name"] == "John"
        assert data["last_name"] == "Smith"
        assert data["date_of_birth"] == "1985-03-15"
        assert data["request_source_id"] == "acme-corp"
        assert data["status"] == Status.PROCESSING
        assert data["created_by"] == "endpoint_test@example.com"
        assert "id" in data
        assert "created_on" in data

    @pytest.mark.asyncio
    async def test_create_data_request_missing_person_id(
        self, client: AsyncClient, auth_headers: dict
    ) -> None:
        response = await client.post(
            "/api/v1/data-requests",
            json={
                "request_source_id": "acme-corp",
            },
            headers=auth_headers,
        )

        assert response.status_code == 422

    @pytest.mark.asyncio
    async def test_create_data_request_missing_request_source_id(
        self, client: AsyncClient, auth_headers: dict
    ) -> None:
        response = await client.post(
            "/api/v1/data-requests",
            json={
                "person_id": 1,
            },
            headers=auth_headers,
        )

        assert response.status_code == 422

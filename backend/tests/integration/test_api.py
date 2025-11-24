import os

import pytest
from dotenv import load_dotenv
from httpx import ASGITransport, AsyncClient

from core.data_request import Status
from main import app

load_dotenv()


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
    demo_password = os.getenv("DEMO_USER_PASSWORD")
    login_response = await client.post(
        "/api/v1/auth/jwt/login",
        data={
            "username": "demo@example.com",
            "password": demo_password,
        },
    )
    token = login_response.json()["access_token"]
    return {"Authorization": f"Bearer {token}"}


class TestGetDataRequestsEndpoint:
    """Integration tests for GET /api/v1/data-requests endpoint."""

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


class TestPostDataRequestEndpoint:
    """Integration tests for POST /api/v1/data-requests endpoint."""

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
        assert data["created_by"] == "demo@example.com"
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


class TestGetPeopleEndpoint:
    """Integration tests for GET /api/v1/people endpoint."""

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


class TestGetRequestSourcesEndpoint:
    """Integration tests for GET /api/v1/request-sources endpoint."""

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

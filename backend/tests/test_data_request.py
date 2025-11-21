from datetime import datetime

from fastapi.testclient import TestClient

from core import DataRequest, Status, get_all_data_requests
from main import app


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


class TestDataRequest:
    def test_create_data_request(self) -> None:
        created_on = datetime(2024, 1, 15, 9, 30, 0)
        data_request = DataRequest(
            id=1,
            first_name="John",
            last_name="Smith",
            status=Status.CREATED,
            created_on=created_on,
            created_by="admin@example.com",
            request_source_id="acme-corp",
        )

        assert data_request.id == 1
        assert data_request.first_name == "John"
        assert data_request.last_name == "Smith"
        assert data_request.status == Status.CREATED
        assert data_request.created_on == created_on
        assert data_request.created_by == "admin@example.com"
        assert data_request.request_source_id == "acme-corp"

    def test_data_request_status_is_int_enum(self) -> None:
        data_request = DataRequest(
            id=1,
            first_name="Test",
            last_name="User",
            status=Status.PROCESSING,
            created_on=datetime.now(),
            created_by="test@example.com",
            request_source_id="test-corp",
        )

        # Status should be usable as an int
        assert data_request.status == 2
        assert int(data_request.status) == 2


class TestGetAllDataRequests:
    def test_returns_list_of_data_requests(self) -> None:
        data_requests = get_all_data_requests()

        assert isinstance(data_requests, list)
        assert len(data_requests) > 0
        assert all(isinstance(dr, DataRequest) for dr in data_requests)

    def test_data_requests_have_correct_types(self) -> None:
        data_requests = get_all_data_requests()

        for dr in data_requests:
            assert isinstance(dr.id, int)
            assert isinstance(dr.first_name, str)
            assert isinstance(dr.last_name, str)
            assert isinstance(dr.status, Status)
            assert isinstance(dr.created_on, datetime)
            assert isinstance(dr.created_by, str)
            assert isinstance(dr.request_source_id, str)

    def test_loads_expected_test_data(self) -> None:
        data_requests = get_all_data_requests()

        # Verify we have the expected number of test records
        assert len(data_requests) == 6

        # Verify first record matches expected data
        first = data_requests[0]
        assert first.id == 1
        assert first.first_name == "John"
        assert first.last_name == "Smith"
        assert first.status == Status.CREATED
        assert first.request_source_id == "acme-corp"

    def test_contains_all_status_types(self) -> None:
        data_requests = get_all_data_requests()
        statuses = {dr.status for dr in data_requests}

        assert Status.CREATED in statuses
        assert Status.PROCESSING in statuses
        assert Status.NEEDS_REVIEW in statuses
        assert Status.COMPLETE in statuses


class TestGetDataRequestsEndpoint:
    def setup_method(self) -> None:
        self.client = TestClient(app)

    def test_get_all_data_requests(self) -> None:
        response = self.client.get("/api/v1/data-requests")

        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)
        assert len(data) == 6

    def test_filter_by_status_created(self) -> None:
        response = self.client.get("/api/v1/data-requests?status=1")

        assert response.status_code == 200
        data = response.json()
        assert all(item["status"] == 1 for item in data)

    def test_filter_by_status_processing(self) -> None:
        response = self.client.get("/api/v1/data-requests?status=2")

        assert response.status_code == 200
        data = response.json()
        assert all(item["status"] == 2 for item in data)

    def test_filter_by_status_needs_review(self) -> None:
        response = self.client.get("/api/v1/data-requests?status=3")

        assert response.status_code == 200
        data = response.json()
        assert all(item["status"] == 3 for item in data)

    def test_filter_by_status_complete(self) -> None:
        response = self.client.get("/api/v1/data-requests?status=99")

        assert response.status_code == 200
        data = response.json()
        assert all(item["status"] == 99 for item in data)

    def test_filter_by_invalid_status_returns_empty(self) -> None:
        response = self.client.get("/api/v1/data-requests?status=999")

        assert response.status_code == 200
        data = response.json()
        assert data == []

    def test_filter_returns_correct_count(self) -> None:
        # Get counts for each status from unfiltered data
        all_response = self.client.get("/api/v1/data-requests")
        all_data = all_response.json()

        for status_value in [1, 2, 3, 99]:
            expected_count = sum(1 for item in all_data if item["status"] == status_value)
            filtered_response = self.client.get(f"/api/v1/data-requests?status={status_value}")
            filtered_data = filtered_response.json()
            assert len(filtered_data) == expected_count

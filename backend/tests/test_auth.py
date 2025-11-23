import os

import pytest
from dotenv import load_dotenv
from httpx import ASGITransport, AsyncClient

from main import app

load_dotenv()


class TestAuthLogin:
    """Tests for JWT login endpoint."""

    @pytest.mark.asyncio
    async def test_login_with_valid_credentials(self) -> None:
        async with AsyncClient(
            transport=ASGITransport(app=app), base_url="http://test"
        ) as client:
            demo_password = os.getenv("DEMO_USER_PASSWORD")
            response = await client.post(
                "/api/v1/auth/jwt/login",
                data={
                    "username": "demo@example.com",
                    "password": demo_password,
                },
            )

        assert response.status_code == 200
        data = response.json()
        assert "access_token" in data
        assert data["token_type"] == "bearer"

    @pytest.mark.asyncio
    async def test_login_with_invalid_password_fails(self) -> None:
        async with AsyncClient(
            transport=ASGITransport(app=app), base_url="http://test"
        ) as client:
            response = await client.post(
                "/api/v1/auth/jwt/login",
                data={
                    "username": "demo@example.com",
                    "password": "wrongpassword",
                },
            )

        assert response.status_code == 400

    @pytest.mark.asyncio
    async def test_login_with_nonexistent_user_fails(self) -> None:
        async with AsyncClient(
            transport=ASGITransport(app=app), base_url="http://test"
        ) as client:
            response = await client.post(
                "/api/v1/auth/jwt/login",
                data={
                    "username": "nonexistent@example.com",
                    "password": "anypassword",
                },
            )

        assert response.status_code == 400


class TestAuthenticatedEndpoints:
    """Tests for endpoints that require authentication."""

    @pytest.mark.asyncio
    async def test_get_current_user(self) -> None:
        async with AsyncClient(
            transport=ASGITransport(app=app), base_url="http://test"
        ) as client:
            demo_password = os.getenv("DEMO_USER_PASSWORD")
            login_response = await client.post(
                "/api/v1/auth/jwt/login",
                data={
                    "username": "demo@example.com",
                    "password": demo_password,
                },
            )
            token = login_response.json()["access_token"]

            # Get current user
            response = await client.get(
                "/api/v1/users/me",
                headers={"Authorization": f"Bearer {token}"},
            )

        assert response.status_code == 200
        data = response.json()
        assert data["email"] == "demo@example.com"

    @pytest.mark.asyncio
    async def test_protected_endpoint_without_token_fails(self) -> None:
        async with AsyncClient(
            transport=ASGITransport(app=app), base_url="http://test"
        ) as client:
            response = await client.get("/api/v1/data-requests")

        assert response.status_code == 401

    @pytest.mark.asyncio
    async def test_protected_endpoint_with_invalid_token_fails(self) -> None:
        async with AsyncClient(
            transport=ASGITransport(app=app), base_url="http://test"
        ) as client:
            response = await client.get(
                "/api/v1/data-requests",
                headers={"Authorization": "Bearer invalid-token"},
            )

        assert response.status_code == 401

    @pytest.mark.asyncio
    async def test_data_requests_endpoint_with_valid_token(self) -> None:
        async with AsyncClient(
            transport=ASGITransport(app=app), base_url="http://test"
        ) as client:
            demo_password = os.getenv("DEMO_USER_PASSWORD")
            login_response = await client.post(
                "/api/v1/auth/jwt/login",
                data={
                    "username": "demo@example.com",
                    "password": demo_password,
                },
            )
            token = login_response.json()["access_token"]

            # Access protected endpoint
            response = await client.get(
                "/api/v1/data-requests",
                headers={"Authorization": f"Bearer {token}"},
            )

        assert response.status_code == 200
        assert isinstance(response.json(), list)

import uuid

import pytest
from httpx import ASGITransport, AsyncClient

from main import app


class TestAuthRegistration:
    """Tests for user registration endpoint."""

    @pytest.mark.asyncio
    async def test_register_new_user(self) -> None:
        # Use unique email to avoid conflicts with other tests in session
        unique_email = f"newuser_{uuid.uuid4().hex[:8]}@example.com"
        async with AsyncClient(
            transport=ASGITransport(app=app), base_url="http://test"
        ) as client:
            response = await client.post(
                "/api/v1/auth/register",
                json={
                    "email": unique_email,
                    "password": "securepassword123",
                },
            )

        assert response.status_code == 201
        data = response.json()
        assert data["email"] == unique_email
        assert "id" in data
        assert data["is_active"] is True
        assert data["is_superuser"] is False
        assert data["is_verified"] is False
        assert "hashed_password" not in data

    @pytest.mark.asyncio
    async def test_register_duplicate_email_fails(self) -> None:
        async with AsyncClient(
            transport=ASGITransport(app=app), base_url="http://test"
        ) as client:
            # Register first user
            await client.post(
                "/api/v1/auth/register",
                json={
                    "email": "duplicate@example.com",
                    "password": "securepassword123",
                },
            )

            # Try to register with same email
            response = await client.post(
                "/api/v1/auth/register",
                json={
                    "email": "duplicate@example.com",
                    "password": "differentpassword",
                },
            )

        assert response.status_code == 400

    @pytest.mark.asyncio
    async def test_register_invalid_email_fails(self) -> None:
        async with AsyncClient(
            transport=ASGITransport(app=app), base_url="http://test"
        ) as client:
            response = await client.post(
                "/api/v1/auth/register",
                json={
                    "email": "not-an-email",
                    "password": "securepassword123",
                },
            )

        assert response.status_code == 422


class TestAuthLogin:
    """Tests for JWT login endpoint."""

    @pytest.mark.asyncio
    async def test_login_with_valid_credentials(self) -> None:
        async with AsyncClient(
            transport=ASGITransport(app=app), base_url="http://test"
        ) as client:
            # Register a user first
            await client.post(
                "/api/v1/auth/register",
                json={
                    "email": "logintest@example.com",
                    "password": "securepassword123",
                },
            )

            # Login with form data (OAuth2 password flow)
            response = await client.post(
                "/api/v1/auth/jwt/login",
                data={
                    "username": "logintest@example.com",
                    "password": "securepassword123",
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
            # Register a user first
            await client.post(
                "/api/v1/auth/register",
                json={
                    "email": "wrongpass@example.com",
                    "password": "correctpassword",
                },
            )

            # Try to login with wrong password
            response = await client.post(
                "/api/v1/auth/jwt/login",
                data={
                    "username": "wrongpass@example.com",
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
            # Register and login
            await client.post(
                "/api/v1/auth/register",
                json={
                    "email": "currentuser@example.com",
                    "password": "securepassword123",
                },
            )
            login_response = await client.post(
                "/api/v1/auth/jwt/login",
                data={
                    "username": "currentuser@example.com",
                    "password": "securepassword123",
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
        assert data["email"] == "currentuser@example.com"

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
            # Register and login
            await client.post(
                "/api/v1/auth/register",
                json={
                    "email": "datarequest@example.com",
                    "password": "securepassword123",
                },
            )
            login_response = await client.post(
                "/api/v1/auth/jwt/login",
                data={
                    "username": "datarequest@example.com",
                    "password": "securepassword123",
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

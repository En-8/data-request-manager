import uuid
from typing import Optional

from fastapi import Depends, Request
from fastapi_users import BaseUserManager, UUIDIDMixin

from .models import User
from .database import get_async_session
from fastapi_users.db import SQLAlchemyUserDatabase
from sqlalchemy.ext.asyncio import AsyncSession


async def get_user_db(session: AsyncSession = Depends(get_async_session)):
    """Dependency for getting the user database adapter."""
    yield SQLAlchemyUserDatabase(session, User)


class UserManager(UUIDIDMixin, BaseUserManager[User, uuid.UUID]):
    """Custom user manager for handling user operations."""

    reset_password_token_secret = "RESET_SECRET"  # Will be overridden
    verification_token_secret = "VERIFY_SECRET"  # Will be overridden

    async def on_after_register(self, user: User, request: Optional[Request] = None):
        """Called after a user registers."""
        print(f"User {user.id} has registered.")

    async def on_after_forgot_password(
        self, user: User, token: str, request: Optional[Request] = None
    ):
        """Called after a password reset is requested."""
        print(f"User {user.id} has forgot their password. Reset token: {token}")

    async def on_after_request_verify(
        self, user: User, token: str, request: Optional[Request] = None
    ):
        """Called after email verification is requested."""
        print(f"Verification requested for user {user.id}. Verification token: {token}")


async def get_user_manager(user_db=Depends(get_user_db)):
    """Dependency for getting the user manager."""
    yield UserManager(user_db)

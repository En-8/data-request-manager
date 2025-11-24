import os
from typing import AsyncGenerator
from urllib.parse import quote_plus

import psycopg
from dotenv import load_dotenv
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy.orm import DeclarativeBase

load_dotenv()


class Base(DeclarativeBase):
    """Base class for all SQLAlchemy models."""

    pass


def get_connection_string() -> str:
    """Build connection string from environment variables."""
    host = os.getenv("DB_HOST", "localhost")
    port = os.getenv("DB_PORT", "5432")
    dbname = os.getenv("DB_NAME", "data_request_manager")
    user = os.getenv("DB_USER", "postgres")
    password = os.getenv("DB_PASSWORD", "postgres")
    encoded_password = quote_plus(password)
    return f"postgresql://{user}:{encoded_password}@{host}:{port}/{dbname}"


def get_async_database_url() -> str:
    """Build async database URL for SQLAlchemy from environment variables."""
    host = os.getenv("DB_HOST", "localhost")
    port = os.getenv("DB_PORT", "5432")
    dbname = os.getenv("DB_NAME", "data_request_manager")
    user = os.getenv("DB_USER", "postgres")
    password = os.getenv("DB_PASSWORD", "postgres")
    encoded_password = quote_plus(password)
    return f"postgresql+asyncpg://{user}:{encoded_password}@{host}:{port}/{dbname}"


engine = create_async_engine(
    get_async_database_url(),
    pool_pre_ping=True,
    pool_size=5,
    max_overflow=10,
)
async_session_maker = async_sessionmaker(engine, expire_on_commit=False)


async def get_async_session() -> AsyncGenerator[AsyncSession, None]:
    """Dependency for getting async database sessions."""
    async with async_session_maker() as session:
        try:
            yield session
            await session.commit()
        except Exception:
            await session.rollback()
            raise


def get_sync_connection() -> psycopg.Connection:
    """Get a sync database connection (for scripts like seed.py)."""
    return psycopg.connect(get_connection_string())

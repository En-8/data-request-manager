import os
from urllib.parse import quote_plus

import psycopg
from dotenv import load_dotenv

load_dotenv()


def get_connection_string() -> str:
    """Build connection string from environment variables."""
    host = os.getenv("DB_HOST", "localhost")
    port = os.getenv("DB_PORT", "5432")
    dbname = os.getenv("DB_NAME", "data_request_manager")
    user = os.getenv("DB_USER", "postgres")
    password = os.getenv("DB_PASSWORD", "postgres")
    encoded_password = quote_plus(password)
    return f"postgresql://{user}:{encoded_password}@{host}:{port}/{dbname}"


async def get_connection() -> psycopg.AsyncConnection:
    """Get an async database connection."""
    return await psycopg.AsyncConnection.connect(get_connection_string())


def get_sync_connection() -> psycopg.Connection:
    """Get a sync database connection (for scripts like seed.py)."""
    return psycopg.connect(get_connection_string())

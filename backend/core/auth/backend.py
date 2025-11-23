import os

from dotenv import load_dotenv
from fastapi_users.authentication import (
    AuthenticationBackend,
    BearerTransport,
    JWTStrategy,
)

load_dotenv()

# JWT configuration
SECRET = os.getenv("JWT_SECRET", "CHANGE_ME_IN_PRODUCTION")
LIFETIME_SECONDS = 3600  # 1 hour


bearer_transport = BearerTransport(tokenUrl="auth/jwt/login")


def get_jwt_strategy() -> JWTStrategy:
    """Get JWT strategy with configured secret and lifetime."""
    return JWTStrategy(secret=SECRET, lifetime_seconds=LIFETIME_SECONDS)


auth_backend = AuthenticationBackend(
    name="jwt",
    transport=bearer_transport,
    get_strategy=get_jwt_strategy,
)

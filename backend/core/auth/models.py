from fastapi_users.db import SQLAlchemyBaseUserTableUUID

from core.database import Base


class User(SQLAlchemyBaseUserTableUUID, Base):
    """User model for authentication.

    Inherits from SQLAlchemyBaseUserTableUUID which provides:
    - id: UUID primary key
    - email: unique email address
    - hashed_password: bcrypt hashed password
    - is_active: whether user can login
    - is_superuser: admin privileges
    - is_verified: email verification status
    """

    pass

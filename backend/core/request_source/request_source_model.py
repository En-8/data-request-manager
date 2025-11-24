from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column

from core.database import Base


class RequestSourceModel(Base):
    """SQLAlchemy model for the request_source table."""

    __tablename__ = "request_source"

    id: Mapped[str] = mapped_column(String(100), primary_key=True)
    name: Mapped[str] = mapped_column(String(255))

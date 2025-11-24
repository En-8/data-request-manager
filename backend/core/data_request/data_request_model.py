from datetime import date, datetime

from sqlalchemy import Date, DateTime, ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column

from core.database import Base


class DataRequestModel(Base):
    """SQLAlchemy model for the data_request table."""

    __tablename__ = "data_request"

    id: Mapped[int] = mapped_column(primary_key=True)
    person_id: Mapped[int] = mapped_column(Integer, ForeignKey("people.id"))
    first_name: Mapped[str] = mapped_column(String(100))
    last_name: Mapped[str] = mapped_column(String(100))
    date_of_birth: Mapped[date] = mapped_column(Date)
    status: Mapped[int] = mapped_column(Integer)
    created_on: Mapped[datetime] = mapped_column(DateTime)
    created_by: Mapped[str] = mapped_column(String(255))
    request_source_id: Mapped[str] = mapped_column(
        String(100), ForeignKey("request_source.id")
    )

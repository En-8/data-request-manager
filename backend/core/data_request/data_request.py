from dataclasses import dataclass
from datetime import date, datetime
from enum import IntEnum


class Status(IntEnum):
    """Status values for data requests."""

    CREATED = 1
    PROCESSING = 2
    NEEDS_REVIEW = 3
    COMPLETE = 99


@dataclass
class DataRequest:
    """Data transfer object for a data request."""

    id: int
    person_id: int
    first_name: str
    last_name: str
    date_of_birth: date
    status: Status
    created_on: datetime
    created_by: str
    request_source_id: str

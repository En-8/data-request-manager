from dataclasses import dataclass
from datetime import date


@dataclass
class Person:
    """Data transfer object for a person."""

    id: int
    first_name: str
    last_name: str
    date_of_birth: date

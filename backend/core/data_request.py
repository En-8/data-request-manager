from dataclasses import dataclass
from datetime import date, datetime
from enum import IntEnum

from core.database import get_connection


class Status(IntEnum):
    CREATED = 1
    PROCESSING = 2
    NEEDS_REVIEW = 3
    COMPLETE = 99


@dataclass
class Person:
    id: int
    first_name: str
    last_name: str
    date_of_birth: date


@dataclass
class DataRequest:
    id: int
    person_id: int
    first_name: str
    last_name: str
    date_of_birth: date
    status: Status
    created_on: datetime
    created_by: str
    request_source_id: str


@dataclass
class RequestSource:
    id: str
    name: str


async def get_all_people() -> list[Person]:
    """Load all people from the database."""
    async with await get_connection() as conn:
        async with conn.cursor() as cur:
            await cur.execute(
                """
                SELECT id, first_name, last_name, date_of_birth
                FROM people
                ORDER BY last_name, first_name
                """
            )
            rows = await cur.fetchall()

    people: list[Person] = []
    for row in rows:
        person = Person(
            id=row[0],
            first_name=row[1],
            last_name=row[2],
            date_of_birth=row[3],
        )
        people.append(person)

    return people


async def get_person_by_id(person_id: int) -> Person | None:
    """Get a person by their ID."""
    async with await get_connection() as conn:
        async with conn.cursor() as cur:
            await cur.execute(
                """
                SELECT id, first_name, last_name, date_of_birth
                FROM people
                WHERE id = %s
                """,
                (person_id,),
            )
            row = await cur.fetchone()

    if row is None:
        return None

    return Person(
        id=row[0],
        first_name=row[1],
        last_name=row[2],
        date_of_birth=row[3],
    )


async def get_all_data_requests() -> list[DataRequest]:
    """Load all data requests from the database."""
    async with await get_connection() as conn:
        async with conn.cursor() as cur:
            await cur.execute(
                """
                SELECT id, person_id, first_name, last_name, date_of_birth, status, created_on, created_by, request_source_id
                FROM data_request
                ORDER BY id
                """
            )
            rows = await cur.fetchall()

    data_requests: list[DataRequest] = []
    for row in rows:
        data_request = DataRequest(
            id=row[0],
            person_id=row[1],
            first_name=row[2],
            last_name=row[3],
            date_of_birth=row[4],
            status=Status(row[5]),
            created_on=row[6],
            created_by=row[7],
            request_source_id=row[8],
        )
        data_requests.append(data_request)

    return data_requests


async def get_all_request_sources() -> list[RequestSource]:
    """Load all request sources from the database."""
    async with await get_connection() as conn:
        async with conn.cursor() as cur:
            await cur.execute(
                """
                SELECT id, name
                FROM request_source
                ORDER BY name
                """
            )
            rows = await cur.fetchall()

    request_sources: list[RequestSource] = []
    for row in rows:
        request_source = RequestSource(
            id=row[0],
            name=row[1],
        )
        request_sources.append(request_source)

    return request_sources


async def create_data_request(
    person_id: int,
    request_source_id: str,
) -> DataRequest:
    """Create a new data request in the database."""
    # First, get the person's details
    person = await get_person_by_id(person_id)
    if person is None:
        raise ValueError(f"Person with id {person_id} not found")

    async with await get_connection() as conn:
        async with conn.cursor() as cur:
            await cur.execute(
                """
                INSERT INTO data_request (person_id, first_name, last_name, date_of_birth, status, created_on, created_by, request_source_id)
                VALUES (%s, %s, %s, %s, %s, NOW(), %s, %s)
                RETURNING id, person_id, first_name, last_name, date_of_birth, status, created_on, created_by, request_source_id
                """,
                (
                    person_id,
                    person.first_name,
                    person.last_name,
                    person.date_of_birth,
                    Status.PROCESSING,
                    "demo_user",
                    request_source_id,
                ),
            )
            row = await cur.fetchone()
            await conn.commit()

    if row is None:
        raise Exception("Failed to create data request")

    return DataRequest(
        id=row[0],
        person_id=row[1],
        first_name=row[2],
        last_name=row[3],
        date_of_birth=row[4],
        status=Status(row[5]),
        created_on=row[6],
        created_by=row[7],
        request_source_id=row[8],
    )

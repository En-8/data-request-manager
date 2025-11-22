from dataclasses import dataclass
from datetime import datetime
from enum import IntEnum

from core.database import get_connection


class Status(IntEnum):
    CREATED = 1
    PROCESSING = 2
    NEEDS_REVIEW = 3
    COMPLETE = 99


@dataclass
class DataRequest:
    id: int
    first_name: str
    last_name: str
    status: Status
    created_on: datetime
    created_by: str
    request_source_id: str


async def get_all_data_requests() -> list[DataRequest]:
    """Load all data requests from the database."""
    async with await get_connection() as conn:
        async with conn.cursor() as cur:
            await cur.execute(
                """
                SELECT id, first_name, last_name, status, created_on, created_by, request_source_id
                FROM data_request
                ORDER BY id
                """
            )
            rows = await cur.fetchall()

    data_requests: list[DataRequest] = []
    for row in rows:
        data_request = DataRequest(
            id=row[0],
            first_name=row[1],
            last_name=row[2],
            status=Status(row[3]),
            created_on=row[4],
            created_by=row[5],
            request_source_id=row[6],
        )
        data_requests.append(data_request)

    return data_requests

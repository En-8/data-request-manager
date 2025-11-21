import json
from dataclasses import dataclass
from datetime import datetime
from enum import IntEnum
from pathlib import Path


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


def get_all_data_requests() -> list[DataRequest]:
    """Load all data requests from the JSON data file."""
    data_path = Path(__file__).parent.parent / "data" / "data_requests.json"

    with open(data_path) as f:
        raw_data = json.load(f)

    data_requests: list[DataRequest] = []
    for item in raw_data:
        data_request = DataRequest(
            id=item["id"],
            first_name=item["firstName"],
            last_name=item["lastName"],
            status=Status(item["status"]),
            created_on=datetime.fromisoformat(item["createdOn"]),
            created_by=item["createdBy"],
            request_source_id=item["requestSourceId"],
        )
        data_requests.append(data_request)

    return data_requests

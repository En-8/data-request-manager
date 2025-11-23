from dataclasses import asdict
from typing import Any

from core import get_all_data_requests, get_all_request_sources, get_all_people, create_data_request
from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel


class CreateDataRequestBody(BaseModel):
    person_id: int
    request_source_id: str

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def read_root() -> dict[str, str]:
    return {"Hello": "World"}


@app.get("/api/v1/data-requests")
async def get_data_requests(status: int | None = Query(None)) -> list[dict[str, Any]]:
    """Get all data requests, optionally filtered by status."""
    data_requests = await get_all_data_requests()
    if status is not None:
        data_requests = [dr for dr in data_requests if dr.status == status]
    return [asdict(dr) for dr in data_requests]


@app.post("/api/v1/data-requests")
async def post_data_request(body: CreateDataRequestBody) -> dict[str, Any]:
    """Create a new data request."""
    data_request = await create_data_request(
        person_id=body.person_id,
        request_source_id=body.request_source_id,
    )
    return asdict(data_request)


@app.get("/api/v1/request-sources")
async def get_request_sources() -> list[dict[str, Any]]:
    """Get all request sources."""
    request_sources = await get_all_request_sources()
    return [asdict(rs) for rs in request_sources]


@app.get("/api/v1/people")
async def get_people() -> list[dict[str, Any]]:
    """Get all people."""
    people = await get_all_people()
    return [asdict(p) for p in people]

from dataclasses import asdict
from typing import Any

from core import get_all_data_requests
from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware

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

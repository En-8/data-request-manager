from dataclasses import asdict
from typing import Any

from core import get_all_data_requests
from fastapi import FastAPI
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
def get_data_requests() -> list[dict[str, Any]]:
    """Get all data requests."""
    data_requests = get_all_data_requests()
    return [asdict(dr) for dr in data_requests]

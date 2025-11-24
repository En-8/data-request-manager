import os
from dataclasses import asdict
from typing import Any

from fastapi import Depends, FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from sqlalchemy.ext.asyncio import AsyncSession

from core.auth import (
    User,
    UserRead,
    UserUpdate,
    auth_backend,
    current_active_user,
    fastapi_users,
)
from core.data_request import (
    DataRequestRepository,
    DataRequestService,
    PersonNotFoundError,
)
from core.database import get_async_session
from core.person import PersonRepository
from core.request_source import RequestSourceRepository


class CreateDataRequestBody(BaseModel):
    person_id: int
    request_source_id: str


app = FastAPI()

# Parse CORS origins from environment variable (comma-separated)
cors_origins_env = os.getenv("CORS_ORIGINS", "http://localhost:5173")
cors_origins = [origin.strip() for origin in cors_origins_env.split(",")]

app.add_middleware(
    CORSMiddleware,
    allow_origins=cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Auth routers
app.include_router(
    fastapi_users.get_auth_router(auth_backend),
    prefix="/api/v1/auth/jwt",
    tags=["auth"],
)
app.include_router(
    fastapi_users.get_users_router(UserRead, UserUpdate),
    prefix="/api/v1/users",
    tags=["users"],
)


@app.get("/")
def read_root() -> dict[str, str]:
    return {"Hello": "World"}


@app.get("/api/v1/data-requests")
async def get_data_requests(
    status: int | None = Query(None),
    user: User = Depends(current_active_user),
    session: AsyncSession = Depends(get_async_session),
) -> list[dict[str, Any]]:
    """Get all data requests, optionally filtered by status."""
    repo = DataRequestRepository(session)
    data_requests = await repo.get_all()
    if status is not None:
        data_requests = [dr for dr in data_requests if dr.status == status]
    return [asdict(dr) for dr in data_requests]


@app.post("/api/v1/data-requests")
async def post_data_request(
    body: CreateDataRequestBody,
    user: User = Depends(current_active_user),
    session: AsyncSession = Depends(get_async_session),
) -> dict[str, Any]:
    """Create a new data request."""
    person_repo = PersonRepository(session)
    data_request_repo = DataRequestRepository(session)
    service = DataRequestService(data_request_repo, person_repo)

    try:
        data_request = await service.create_data_request(
            person_id=body.person_id,
            request_source_id=body.request_source_id,
            created_by=user.email,
        )
    except PersonNotFoundError as e:
        from fastapi import HTTPException

        raise HTTPException(status_code=404, detail=str(e))

    return asdict(data_request)


@app.get("/api/v1/request-sources")
async def get_request_sources(
    user: User = Depends(current_active_user),
    session: AsyncSession = Depends(get_async_session),
) -> list[dict[str, Any]]:
    """Get all request sources."""
    repo = RequestSourceRepository(session)
    request_sources = await repo.get_all()
    return [asdict(rs) for rs in request_sources]


@app.get("/api/v1/people")
async def get_people(
    user: User = Depends(current_active_user),
    session: AsyncSession = Depends(get_async_session),
) -> list[dict[str, Any]]:
    """Get all people."""
    repo = PersonRepository(session)
    people = await repo.get_all()
    return [asdict(p) for p in people]

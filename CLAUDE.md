# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Full-stack case management application with React frontend and FastAPI backend.

## Commands

### Frontend (ui/)

```bash
pnpm install          # Install dependencies
pnpm dev              # Start dev server (http://localhost:5173)
pnpm build            # Production build (runs tsc first)
pnpm preview          # Preview production build
pnpm typecheck        # Run TypeScript type checking
```

### Backend (backend/)

```bash
uv sync                           # Install dependencies
python -m fastapi dev main.py     # Start dev server (http://localhost:8000)
ruff check .                      # Lint Python code
ruff format .                     # Format Python code
```

### Database

```bash
python rebuild-db.py --initialize # First-time setup: create database, migrate, and seed
python rebuild-db.py              # Rebuild: clean, migrate, and seed
```

Flyway commands (run from `backend/db/`):
```bash
flyway -configFiles=flyway.conf info      # Show migration status
```

API docs available at http://localhost:8000/docs when backend is running.

## Architecture

### Frontend (ui/)
- **React 19** with **React Router v7** (library mode, client-side routing only)
- **TypeScript** with strict mode
- **Tailwind CSS v4** for styling
- **Vite** for dev server and bundling
- Path alias: `~/` maps to `./app/`
- Entry point: `app/main.tsx`
- Routes defined in `app/App.tsx`, pages in `app/pages/`
- API calls made directly to backend (no proxy) - requires CORS on backend

### Backend (backend/)
- **FastAPI** with Python 3.12
- **uv** for package management
- **PostgreSQL** database (`data_request_manager`)
- **psycopg3** for async database access
- **Flyway** for database migrations (date-based versioning: `V20251121001__`)
- Migrations in `db/migrations/`, seed data in `db/seed.py`
- Single entry point in `main.py`

## Database Setup

### First-time setup

1. Install PostgreSQL (e.g., `brew install postgresql@17`) and start it
2. Create the postgres role:
   ```bash
   psql postgres
   CREATE ROLE postgres WITH LOGIN PASSWORD 'postgres' SUPERUSER CREATEDB;
   \q
   ```
3. Create `.env` file in `backend/`:
   ```
   DB_HOST=localhost
   DB_PORT=5432
   DB_NAME=data_request_manager
   DB_USER=postgres
   DB_PASSWORD=postgres
   ```
4. Initialize the database:
   ```bash
   cd backend
   python rebuild-db.py --initialize
   ```

### Environment variables

Database configuration uses environment variables (loaded from `backend/.env`):
- `DB_HOST` - Database host (default: localhost)
- `DB_PORT` - Database port (default: 5432)
- `DB_NAME` - Database name (default: data_request_manager)
- `DB_USER` - Database user (default: postgres)
- `DB_PASSWORD` - Database password (default: postgres)

## Development

Run both frontend and backend simultaneously for local development:
- Frontend at http://localhost:5173
- Backend API at http://localhost:8000

## Testing

**Always write unit tests when adding new backend functionality.** Tests should be added to `backend/tests/` using pytest.

Run backend tests:
```bash
cd backend
uv run pytest
```

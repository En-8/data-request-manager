# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Full-stack case management application with React frontend and FastAPI backend.

## Commands

### Frontend (ui/)

```bash
pnpm install          # Install dependencies
pnpm dev              # Start dev server (http://localhost:5173)
pnpm build            # Production build
pnpm typecheck        # Run TypeScript type checking
```

### Backend (backend/)

```bash
uv sync                           # Install dependencies
python -m fastapi dev main.py     # Start dev server (http://localhost:8000)
ruff check .                      # Lint Python code
ruff format .                     # Format Python code
```

API docs available at http://localhost:8000/docs when backend is running.

## Architecture

### Frontend (ui/)
- **React 19** with **React Router v7** configured as SPA (no SSR)
- **TypeScript** with strict mode
- **Tailwind CSS v4** for styling
- **Vite** for bundling
- Path alias: `~/` maps to `./app/`
- Routes defined in `app/routes.ts`, pages in `app/routes/`
- React Router generates types automatically in `.react-router/types/`

### Backend (backend/)
- **FastAPI** with Python 3.12
- **uv** for package management
- Single entry point in `main.py`

## Development

Run both frontend and backend simultaneously for local development:
- Frontend at http://localhost:5173
- Backend API at http://localhost:8000

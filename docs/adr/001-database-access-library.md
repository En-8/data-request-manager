# ADR 001: Database Access Library

## Status

Accepted

## Date

2025-11-21

## Context

We need to connect our FastAPI backend to a PostgreSQL database. The choice of database access library affects type safety, performance, code complexity, and future maintainability.

FastAPI is async-native, so we should consider async database drivers to avoid blocking the event loop under load.

## Options Considered

### 1. psycopg2
- **Pros**: Most widely used PostgreSQL adapter, extensive documentation, battle-tested
- **Cons**: Synchronous only, blocks event loop in async applications, older API

### 2. psycopg3 (psycopg)
- **Pros**: Native async support, better typing, modern API, maintained by same team as psycopg2
- **Cons**: Newer (less community examples), slightly different API from psycopg2

### 3. asyncpg
- **Pros**: Fastest PostgreSQL driver, pure async
- **Cons**: Async-only (no sync fallback for scripts), different API paradigm

### 4. SQLAlchemy 2.0
- **Pros**: Full ORM, type-safe queries, database-agnostic, extensive features
- **Cons**: Added complexity, learning curve, overhead for simple use cases

### 5. SQLModel
- **Pros**: Combines Pydantic + SQLAlchemy, great FastAPI integration, less boilerplate
- **Cons**: Couples database models to API models, newer/less mature

### 6. Prisma Python
- **Pros**: Schema-first, strongest type generation, built-in migrations
- **Cons**: Unofficial Python client, extra build step, less mature ecosystem

## Decision

Use **psycopg3** with async connections for application code.

## Rationale

1. **Async support**: Native async/await integration works well with FastAPI's async architecture without blocking the event loop

2. **Type safety**: psycopg3 has improved typing over psycopg2, providing better IDE support and catch errors earlier

3. **Simplicity**: No ORM overhead - we write SQL directly, which is transparent and performant. We can add an ORM later if needed

4. **Loose coupling**: By not using an ORM, our database access code is separate from our API response models. These can evolve independently

5. **Flexibility**: psycopg3 provides both async and sync APIs, useful for scripts like database seeding

6. **Maturity path**: Same maintainers as psycopg2, so it's a natural upgrade path with production-ready stability

## Consequences

### Positive
- Non-blocking database operations in async endpoints
- Clear separation between database queries and API models
- Simple, understandable code with direct SQL
- Good typing support for IDE autocomplete and error detection

### Negative
- Must write raw SQL (no query builder)
- Manual mapping between database rows and Python objects
- Less abstraction means more boilerplate for complex queries

### Risks
- May need to add an ORM later for complex querying needs
- Team must be comfortable writing SQL

# ADR 002: SQLAlchemy Standardization

## Status

Accepted

Supersedes [ADR 001: Database Access Library](001-database-access-library.md)

## Date

2024-11-24

## Context

Our initial decision to use psycopg3 for direct SQL queries (ADR 001) served us well for simple data access, but we encountered challenges as the application evolved:

1. **Authentication library dependency**: We adopted fastapi-users for authentication, which requires SQLAlchemy for its User model and session management
2. **Inconsistent patterns**: The codebase had two different database access patterns - SQLAlchemy for auth and raw psycopg3 for business data
3. **Maintenance burden**: Manual row-to-object mapping was duplicated across functions and prone to errors when schema changed
4. **Type safety gaps**: Raw SQL strings provided no compile-time checking of column names or types

## Decision

Standardize on **SQLAlchemy 2.0 ORM** for all database access, replacing raw psycopg3 queries.

## Rationale

### 1. Authentication library requirement

The fastapi-users library we selected for authentication requires SQLAlchemy models. Rather than maintain two parallel database access patterns, we consolidate on SQLAlchemy throughout the application.

### 2. Consistent data access patterns

A single approach reduces cognitive load for developers. All repositories now follow the same pattern:
- Inject AsyncSession via dependency injection
- Use SQLAlchemy select/insert statements
- Return domain dataclasses (DTOs)

### 3. Type-safe queries

SQLAlchemy 2.0's mapped columns provide IDE autocomplete and type checking:
```python
# Type-safe - IDE catches typos, wrong types
stmt = select(PersonModel).where(PersonModel.id == person_id)

# vs raw SQL - errors only at runtime
await cur.execute("SELECT * FROM people WHERE id = %s", (person_id,))
```

### 4. Elimination of manual mapping

ORM models automatically map to Python objects, removing repeated row-to-dataclass conversion code that violated DRY and was fragile to schema changes.

### 5. Query composition

SQLAlchemy's query builder enables composable, reusable query logic that raw SQL cannot provide.

## Implementation

### Architecture

```
core/
├── database.py           # Shared engine, Base, session factory
├── repository.py         # Base repository class
├── person/
│   ├── person_model.py   # SQLAlchemy ORM model
│   ├── person_repo.py    # Repository with typed queries
│   └── person.py         # DTO dataclass
├── data_request/
│   └── ...               # Same pattern
└── request_source/
    └── ...               # Same pattern
```

### Key components

- **Single Base class**: Shared across all models including auth User
- **Async engine**: Uses asyncpg driver for non-blocking operations
- **Repository pattern**: Data access encapsulated in repository classes
- **Service layer**: Business logic uses repositories, not direct database access

## Consequences

### Positive

- Single database access pattern throughout codebase
- Type-safe queries with IDE support
- No manual row mapping - less code, fewer bugs
- Better testability - repositories can be mocked
- Query composition for complex filtering/joins

### Negative

- Slightly more overhead than raw SQL for simple queries
- Team needs SQLAlchemy 2.0 knowledge
- More boilerplate for simple CRUD operations

### Migration notes

- Existing psycopg3 sync connection retained for database scripts (seed.py)
- All application code now uses SQLAlchemy async sessions
- Tests restructured into unit (mocked repos) and integration (HTTP API)

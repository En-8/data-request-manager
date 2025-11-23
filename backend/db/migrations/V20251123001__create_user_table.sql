-- Create user table for authentication
-- Uses UUID primary key to match FastAPI Users SQLAlchemyBaseUserTableUUID

CREATE TABLE "user" (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    email VARCHAR(320) NOT NULL UNIQUE,
    hashed_password VARCHAR(1024) NOT NULL,
    is_active BOOLEAN NOT NULL DEFAULT TRUE,
    is_superuser BOOLEAN NOT NULL DEFAULT FALSE,
    is_verified BOOLEAN NOT NULL DEFAULT FALSE
);

-- Index for email lookups during login
CREATE INDEX idx_user_email ON "user" (email);

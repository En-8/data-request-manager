# Data Request Management Application

Full-stack data request management application with React frontend and FastAPI backend.

[See the live demo](http://data-request-manager-frontend.s3-website-us-east-1.amazonaws.com/)

## Prerequisites

- **Node.js** >= 20 with **pnpm** 10.15.0
- **Python** >= 3.12 with **uv** package manager
- **PostgreSQL** 17
- **Flyway** >= 10.20.0 (for migrations)

## Local Development Setup

### 1. Install Dependencies

**Frontend:**
```bash
cd ui
pnpm install
```

**Backend:**
```bash
cd backend
uv sync
```

### 2. Database Setup

Install PostgreSQL and create the postgres role:
```bash
psql postgres
CREATE ROLE postgres WITH LOGIN PASSWORD 'postgres' SUPERUSER CREATEDB;
\q
```

Create `backend/.env`:
```
DB_HOST=localhost
DB_PORT=5432
DB_NAME=data_request_manager
DB_USER=postgres
DB_PASSWORD=postgres
```

Initialize the database:
```bash
cd backend
uv run python rebuild-db.py --initialize
```

This creates the database, runs migrations, and seeds initial data.

### 3. Run the Application

**Backend** (http://localhost:8000):
```bash
cd backend
uv run fastapi dev main.py
```

**Frontend** (http://localhost:5173):
```bash
cd ui
pnpm dev
```

API documentation is available at http://localhost:8000/docs

## Running Tests

**Backend tests:**
```bash
cd backend
uv run pytest
```

**Backend linting:**
```bash
cd backend
uv run ruff check .    # Lint
uv run ruff format .   # Format
```

**Frontend linting:**
```bash
cd ui
pnpm lint
```

## CI/CD Pipeline

The project uses GitHub Actions (`.github/workflows/ci.yml`) with two jobs that run on push/PR to `main`:

**Frontend Job:**
1. Install dependencies (pnpm, frozen lockfile)
2. Run ESLint
3. Build (TypeScript compilation + Vite build)

**Backend Job:**
1. Start PostgreSQL 17 service container
2. Install dependencies (uv sync)
3. Run Ruff linting and format check
4. Initialize database with Flyway migrations
5. Run pytest

## Deployment

### Prerequisites

- Terraform >= 1.2
- Ansible (`uv tool install ansible`)
- AWS CLI configured with credentials
- SSH key pair (`~/.ssh/id_ed25519` and `~/.ssh/id_ed25519.pub`)

### Deploy Infrastructure

```bash
cd infra

# Initialize Terraform
terraform init

# Deploy infrastructure
terraform apply \
  -var="db_password=YOUR_SECURE_PASSWORD" \
  -var="ssh_public_key=$(cat ~/.ssh/id_ed25519.pub)"
```

### Run Database Migrations

Set up SSH tunnel for RDS access:
```bash
ssh -L 5432:<rds-endpoint>:5432 ec2-user@<EC2-public-IP>
```

Run migrations:
```bash
cd backend
flyway -configFiles=db/flyway.conf \
  -url="jdbc:postgresql://$(terraform -chdir=../infra output -raw rds_endpoint)/data_request_manager" \
  -user=postgres \
  -password=YOUR_SECURE_PASSWORD \
  migrate
```

### Deploy Backend

```bash
cd infra/ansible
uv tool run --from ansible ansible-playbook playbook.yml \
  -e "rds_endpoint=$(terraform -chdir=.. output -raw rds_endpoint | cut -d: -f1)" \
  -e "db_password=YOUR_SECURE_PASSWORD" \
  -e "cors_origins=http://localhost:5173,$(terraform -chdir=.. output -raw frontend_url)"
```

### Deploy Frontend

```bash
./infra/deploy-frontend.sh
```

### Terraform Outputs

After deployment:
- `api_url` - API endpoint
- `frontend_url` - Frontend URL
- `ssh_command` - SSH command for EC2
- `rds_endpoint` - Database connection string

### Tear Down

```bash
cd infra
terraform destroy \
  -var="db_password=YOUR_SECURE_PASSWORD" \
  -var="ssh_public_key=$(cat ~/.ssh/id_ed25519.pub)"
```

## Troubleshooting

**Terraform provider not finding credentials after `aws login`:**

Run this to set the environment variables the Terraform provider is looking for:
```bash
eval "$(aws configure export-credentials --format env)"
```

When credentials expire, these env vars aren't automatically cleared on next `aws login`, so you need to clear them first:
```bash
source infra/clean_aws_env.sh
aws login
```

This might be less of an issue if AWS Identity Center and AWS SSO are set up.

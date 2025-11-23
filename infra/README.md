# Infrastructure

## Prerequisites

- Terraform >= 1.2
- Ansible, installed via `uv tool install ansible`
- AWS CLI configured with credentials
- SSH key pair (`~/.ssh/id_ed25519` and `~/.ssh/id_ed25519.pub`)

## Deploy

```bash
cd infra

# Initialize Terraform
terraform init

# Deploy infrastructure
terraform apply \
  -var="db_password=YOUR_SECURE_PASSWORD" \
  -var="ssh_public_key=$(cat ~/.ssh/id_ed25519.pub)"

# setup SSH tunnel for RDS access via EC2
# NOTE: make sure postgres isn't already running locally before running this (or choose a different port binding)
ssh -L 5432:data-request-manager-db.cap62a4aqo82.us-east-1.rds.amazonaws.com:5432 ec2-user@EC2-public-IP

# Run database migrations (from backend directory)
cd ../backend
flyway -configFiles=db/flyway.conf \
  -url="jdbc:postgresql://$(terraform -chdir=../infra output -raw rds_endpoint)/data_request_manager" \
  -user=postgres \
  -password=YOUR_SECURE_PASSWORD \
  migrate

# Alternatively, rebuild the database
# NOTE: your .env file @ backend/.env must have the right remote DB connection info
uv run python rebuild-db.py

# Deploy application with Ansible
cd ../infra/ansible
uv tool run --from ansible ansible-playbook playbook.yml \
-e "rds_endpoint=$(terraform -chdir=.. output -raw rds_endpoint | cut -d: -f1)" \
-e "db_password=YOUR_SECURE_PASSWORD"
```

## Outputs

After deployment, Terraform outputs:
- `api_url` - API endpoint (http://IP:8000)
- `ssh_command` - SSH into EC2 instance
- `rds_endpoint` - Database connection string

## Redeploy Application

To deploy code changes (deploys local `backend/` directory):

```bash
cd infra/ansible
ansible-playbook playbook.yml \
  -e "rds_endpoint=..." \
  -e "db_password=..."
```

## Tear Down

```bash
cd infra
terraform destroy \
  -var="db_password=YOUR_SECURE_PASSWORD" \
  -var="ssh_public_key=$(cat ~/.ssh/id_ed25519.pub)"
```

## Troubleshooting
- Terrform provider not finding credentials after `aws login`
  - Run `eval "$(aws configure export-credentials --format env)"` to set the env vars the terraform provider is looking for
  - When doing this, these env vars aren't automatically cleared on next `aws login`, so you have to run `source clean_aws_env.sh` then run `aws login` again
  - This might be less of an issue if AWS Identity Center and AWS SSO are setup

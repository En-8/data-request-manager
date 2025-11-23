#!/bin/bash
set -e

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
UI_DIR="$SCRIPT_DIR/../ui"

# Get bucket name from Terraform output if not provided
if [ -z "$BUCKET_NAME" ]; then
  BUCKET_NAME=$(terraform -chdir="$SCRIPT_DIR" output -raw frontend_bucket 2>/dev/null || echo "")
  if [ -z "$BUCKET_NAME" ]; then
    echo "Error: Could not get bucket name from Terraform. Run 'terraform apply' first or set BUCKET_NAME env var."
    exit 1
  fi
fi

echo "Building frontend..."
cd "$UI_DIR"
pnpm build

echo "Deploying to S3 bucket: $BUCKET_NAME"

# Sync with appropriate cache headers
# HTML files: no cache (always fetch latest)
aws s3 sync dist/ "s3://$BUCKET_NAME" \
  --delete \
  --exclude "*" \
  --include "*.html" \
  --cache-control "no-cache, no-store, must-revalidate"

# JS and CSS files: long cache (hashed filenames)
aws s3 sync dist/ "s3://$BUCKET_NAME" \
  --delete \
  --exclude "*" \
  --include "*.js" \
  --include "*.css" \
  --cache-control "public, max-age=31536000, immutable"

# Other assets: moderate cache
aws s3 sync dist/ "s3://$BUCKET_NAME" \
  --delete \
  --exclude "*.html" \
  --exclude "*.js" \
  --exclude "*.css" \
  --cache-control "public, max-age=86400"

echo "Deployment complete!"
echo "Website URL: $(terraform -chdir="$SCRIPT_DIR" output -raw frontend_url)"

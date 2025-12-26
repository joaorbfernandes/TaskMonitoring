#!/usr/bin/env bash
set -e

echo "Starting TEST environment..."

PROJECT_NAME="test-infra-$(uuidgen | tr '[:upper:]' '[:lower:]')"

docker compose \
  -f docker/docker-compose.test-infra.yml \
  -p "$PROJECT_NAME" \
  up -d

echo "TEST infrastructure started with project name: $PROJECT_NAME"

echo "Waiting for PostgreSQL (TEST-INFRA) to be ready..."

until docker compose \
  -p "$PROJECT_NAME" \
  exec -T postgres pg_isready -U task_user > /dev/null 2>&1
do
  sleep 1
done

echo "PostgreSQL (TEST-INFRA) is ready."

POSTGRES_PORT=$(docker compose \
  -p "$PROJECT_NAME" \
  port postgres 5432 | cut -d: -f2)

export DATABASE_URL="postgresql://task_user:task_pass@localhost:${POSTGRES_PORT}/task_core_test"

echo "DATABASE_URL set to $DATABASE_URL"

psql "$DATABASE_URL" -f db/ci/bootstrap.sql

echo "Applying migrations..."
for migration in db/migration/*.sql; do
  psql "$DATABASE_URL" -f "$migration"
done

echo "Running infrastructure tests..."

RUN_INFRA_TESTS=1 uv run pytest -m infrastructure -v

trap 'docker compose -p "$PROJECT_NAME" down -v' EXIT
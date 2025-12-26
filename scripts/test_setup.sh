#!/bin/bash
set -e

echo "Starting TEST environment..."

docker compose \
  -p test \
  -f docker/docker-compose.test.yml \
  up -d

echo "Waiting for PostgreSQL (TEST) to be ready..."

until pg_isready -h localhost -p 5434 -U task_user > /dev/null 2>&1; do
  sleep 1
done

export DATABASE_URL="postgresql://task_user:task_pass@localhost:5434/task_core_test"
echo "DATABASE_URL set to $DATABASE_URL"

echo "Bootstrapping TEST database..."

psql "$DATABASE_URL" -f db/ci/bootstrap.sql

echo "Applying migrations..."

for migration in db/migration/*.sql; do
  psql "$DATABASE_URL" -f "$migration"
done

echo "TEST environment ready."
#!/bin/bash
set -e

echo "Starting TEST environment..."

docker compose -f docker/docker-compose.test.yml up -d

echo "Waiting for PostgreSQL (TEST) to be ready..."

until psql -h localhost -p 5434 -U task_user -d task_core_test -c "SELECT 1" >/dev/null 2>&1; do
  echo "Postgres not ready yet... waiting"
  sleep 1
done

echo "Bootstrapping TEST database..."

psql -h localhost -p 5434 -U task_user -d task_core_test \
  -f db/ci/bootstrap.sql

echo "Applying migrations..."

for file in db/migration/*.sql; do
  psql -h localhost -p 5434 -U task_user -d task_core_test -f "$file"
done

echo "TEST environment ready."
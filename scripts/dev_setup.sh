#!/bin/bash
set -e

echo "Starting DEV environment..."

docker compose \
  -p dev \
  -f docker/docker-compose.dev.yml \
  up -d

echo "Waiting for PostgreSQL (DEV) to be ready..."

until psql -h localhost -p 5433 -U task_user -d task_core_dev -c "SELECT 1" >/dev/null 2>&1; do
  echo "Postgres not ready yet... waiting"
  sleep 1
done

echo "Initializing DEV database..."

psql -h localhost -p 5433 -U task_user -d task_core_dev \
  -f db/init/dev/001_create_schema.sql

psql -h localhost -p 5433 -U task_user -d task_core_dev \
  -f db/init/dev/002_create_tasks_table.sql

psql -h localhost -p 5433 -U task_user -d task_core_dev \
  -f db/init/dev/003_seed_dev_data.sql

echo "DEV environment ready."
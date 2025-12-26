-- V001 - Initial creation of tasks table

CREATE SCHEMA IF NOT EXISTS task_core;

CREATE TABLE IF NOT EXISTS task_core.tasks (
    id BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    title TEXT NOT NULL,
    description TEXT,
    due_date DATE NOT NULL,

    status TEXT NOT NULL,
    priority TEXT NOT NULL,

    active BOOLEAN NOT NULL DEFAULT TRUE,

    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS idx_tasks_due_date
    ON task_core.tasks (due_date);

CREATE INDEX IF NOT EXISTS idx_tasks_status
    ON task_core.tasks (status);
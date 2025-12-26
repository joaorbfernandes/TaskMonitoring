CREATE TABLE tasks (
    id INTEGER PRIMARY KEY,

    title TEXT NOT NULL,
    description TEXT NOT NULL,

    due_date DATE NOT NULL,

    status TEXT NOT NULL,
    priority TEXT NOT NULL,

    active BOOLEAN NOT NULL,

    created_at TIMESTAMPTZ NOT NULL,
    updated_at TIMESTAMPTZ NOT NULL
);
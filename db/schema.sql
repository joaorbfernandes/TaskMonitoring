CREATE TABLE tasks (
    iid BIGSERIAL PRIMARY KEY,

    title TEXT NOT NULL,
    description TEXT NULL,

    due_date DATE NOT NULL,

    status TEXT NOT NULL CHECK (status IN ('TODO', 'DONE', 'BLOCKED')),
    priority TEXT NOT NULL CHECK (priority IN ('UNSPECIFIED', 'LOW', 'MEDIUM', 'HIGH')),

    active BOOLEAN NOT NULL,

    created_at TIMESTAMPTZ NOT NULL,
    updated_at TIMESTAMPTZ NOT NULL
);
-- Development seed data
-- Used only for local development and manual inspection

INSERT INTO task_core.tasks (
    id,
    title,
    description,
    due_date,
    status,
    priority,
    active
) VALUES
(
    1,
    'Setup project structure',
    'Initial task to validate persistence',
    CURRENT_DATE + INTERVAL '7 days',
    'OPEN',
    'MEDIUM',
    TRUE
),
(
    2,
    'Review domain rules',
    'Check invariants and business rules',
    CURRENT_DATE + INTERVAL '3 days',
    'OPEN',
    'HIGH',
    TRUE
);
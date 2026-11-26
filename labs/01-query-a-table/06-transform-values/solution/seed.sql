-- The data of lab 1.6. The tests run this script on a new, empty database
-- before each test, so every test starts from these same 10 rows.
-- Do not change it: CREATE TABLE and INSERT are taught in block 3.
-- The text is messy on purpose (spaces, capital letters, two ways of writing
-- a code), as it arrives from a web form. NULL means the data is missing.

CREATE TABLE applications (
    id              INTEGER PRIMARY KEY,
    first_name      TEXT,
    last_name       TEXT,
    email           TEXT,
    job_code        TEXT,      -- area and number of the job offer
    applied_at      TEXT,      -- date and time, ISO-8601: 'YYYY-MM-DD HH:MM'
    expected_salary INTEGER    -- in soles per month
);

INSERT INTO applications (id, first_name, last_name, email, job_code, applied_at, expected_salary) VALUES
    (1,  'Ana',     'Torres',    ' Ana.Torres@Example.com',    'DAT-104', '2026-03-12 10:30', 1800),
    (2,  'Luis',    'Quispe',    'luis.quispe@example.net ', 'DEV 310', '2026-02-28 23:50', 2500),
    (3,  'Rosa',    'Mamani',    'ROSA.MAMANI@EXAMPLE.COM',    'SOP-007', '2026-03-01 08:15', 1200),
    (4,  'Diego',   NULL,        'diego.r@example.com',        'DAT 221', '2026-04-01 00:05', NULL),
    (5,  'Carla',   'Huamán',    'carla.huaman@example.org', 'DEV-118', '2026-03-31 18:20', 3200),
    (6,  'Jorge',   'Salazar',   NULL,                       'SOP 015', '2025-03-20 09:00', 1500),
    (7,  'Valeria', 'Ríos',      ' vale.rios@example.com ',    'DAT-104', '2026-01-15 14:00', 1450),
    (8,  'Miguel',  'Paredes',   'Miguel.Paredes@example.com', 'DEV-310', '2026-03-20 16:45', 2200),
    (9,  'Lucía',   'Fernández', 'lucia.fdz@example.org',      'DAT-221', '2026-03-05 09:10', 1000),
    (10, 'Pedro',   'Vargas',    'pedro.vargas@example.com ',  'SOP-007', '2026-02-10 11:00', 2800);

-- The data of lab 1.4. The tests run this script on a new, empty database
-- before each test, so every test starts from these same 10 rows.
-- Do not change it: CREATE TABLE and INSERT are taught in block 3.
-- NULL means "no data". '' is an empty text, which is not the same thing.

CREATE TABLE members (
    id          INTEGER PRIMARY KEY,
    name        TEXT,
    district    TEXT,      -- where the member lives, if they said
    phone       TEXT,
    email       TEXT,
    monthly_fee INTEGER,   -- in soles
    discount    INTEGER    -- soles off the monthly fee, if any
);

INSERT INTO members (id, name, district, phone, email, monthly_fee, discount) VALUES
    (1,  'Rosa Mendoza',    'Miraflores', '900 000 101', 'rosa.mendoza@example.com',  120, 20),
    (2,  'Carlos Vega',     'Surquillo',  NULL,          'carlos.vega@example.com',   120, NULL),
    (3,  'Lucía Paredes',   NULL,         '900 000 103', '',                          100, 0),
    (4,  'Miguel Ccori',    'Miraflores', NULL,          NULL,                        100, NULL),
    (5,  'Valeria Ríos',    'Barranco',   '900 000 105', 'valeria.rios@example.com',  150, 30),
    (6,  'Diego Salas',     NULL,         NULL,          'diego.salas@example.com',   120, 10),
    (7,  'Fiorella Chávez', 'San Isidro', '900 000 107', '',                          150, NULL),
    (8,  'Renzo Quispe',    'Miraflores', '900 000 108', 'renzo.quispe@example.com',  100, 15),
    (9,  'Camila Torres',   'Surquillo',  '900 000 109', NULL,                        120, 0),
    (10, 'Andrés Huamán',   'Barranco',   '900 000 110', 'andres.huaman@example.com', 150, NULL);

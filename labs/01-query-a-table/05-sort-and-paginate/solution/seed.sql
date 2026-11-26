-- The data of lab 1.5. The tests run this script on a new, empty database
-- before each test, so every test starts from these same 12 rows.
-- Do not change it: CREATE TABLE and INSERT are taught in block 3.
-- NULL in rating means the course has no reviews yet.

CREATE TABLE courses (
    id       INTEGER PRIMARY KEY,
    title    TEXT,
    category TEXT,
    level    TEXT,
    price    INTEGER,   -- in soles
    year     INTEGER,   -- the year the course was published
    students INTEGER,
    rating   REAL       -- average of the reviews, from 1 to 5
);

INSERT INTO courses (id, title, category, level, price, year, students, rating) VALUES
    (1,  'SQL desde cero',                   'Datos',        'básico',     49, 2023, 1250, 4.8),
    (2,  'JavaScript moderno',               'Programación', 'intermedio', 69, 2024,  760, 4.6),
    (3,  'Excel avanzado',                   'Negocios',     'avanzado',   39, 2024, 1250, 4.5),
    (4,  'Figma para principiantes',         'Diseño',       'básico',     49, 2025,  430, 4.2),
    (5,  'Python para análisis de datos',    'Datos',        'intermedio', 89, 2023,  980, 4.6),
    (6,  'Power BI en la práctica',          'Datos',        'intermedio', 69, 2026,  120, NULL),
    (7,  'Git y GitHub',                     'Programación', 'básico',     29, 2023, 1530, 4.9),
    (8,  'Finanzas personales',              'Negocios',     'básico',     29, 2026,   85, NULL),
    (9,  'Diseño de logos',                  'Diseño',       'intermedio', 59, 2024,  310, 3.9),
    (10, 'Django para la web',               'Programación', 'avanzado',   99, 2025,  540, 4.4),
    (11, 'Estadística para no estadísticos', 'Datos',        'básico',     59, 2026,  210, NULL),
    (12, 'Marketing digital',                'Negocios',     'intermedio', 49, 2025,  760, 4.1);

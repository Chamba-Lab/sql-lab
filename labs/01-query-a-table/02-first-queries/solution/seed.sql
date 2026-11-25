-- The data of lab 1.2. The tests run this script on a new, empty database
-- before each test, so every test starts from these same 8 rows.
-- Do not change it: CREATE TABLE and INSERT are taught in block 3.

CREATE TABLE menu_items (
    id       INTEGER PRIMARY KEY,
    name     TEXT,
    category TEXT,
    price    REAL,   -- sale price before tax, in soles
    cost     REAL    -- what the café pays to make it, in soles
);

INSERT INTO menu_items (id, name, category, price, cost) VALUES
    (1, 'Café americano',     'bebida', 6.0,  1.5),
    (2, 'Capuchino',          'bebida', 8.5,  2.25),
    (3, 'Té de manzanilla',   'bebida', 5.0,  0.75),
    (4, 'Jugo de naranja',    'bebida', 9.5,  3.5),
    (5, 'Sándwich de pollo',  'comida', 14.0, 6.25),
    (6, 'Empanada de carne',  'comida', 7.5,  3.0),
    (7, 'Torta de chocolate', 'postre', 11.0, 4.5),
    (8, 'Alfajor',            'postre', 3.5,  1.25);

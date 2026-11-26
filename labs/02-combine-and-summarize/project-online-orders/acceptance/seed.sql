-- The orders of Tinta Viva, a small online stationery shop in Arequipa.
-- The acceptance tests run this script on a new, empty database before each
-- test, so every test starts from these same rows.
-- Do not change it: CREATE TABLE and INSERT are taught in block 3.
-- Prices are in soles. See BRIEF.md for what each column and status means.

CREATE TABLE customers (
    id      INTEGER PRIMARY KEY,
    name    TEXT,
    email   TEXT,
    city    TEXT
);

CREATE TABLE products (
    id        INTEGER PRIMARY KEY,
    name      TEXT,
    category  TEXT,
    price     REAL
);

CREATE TABLE orders (
    id            INTEGER PRIMARY KEY,
    customer_id   INTEGER REFERENCES customers (id),
    ordered_at    TEXT,
    status        TEXT,
    shipping_fee  REAL
);

CREATE TABLE order_items (
    order_id    INTEGER REFERENCES orders (id),
    product_id  INTEGER REFERENCES products (id),
    quantity    INTEGER,
    unit_price  REAL,
    PRIMARY KEY (order_id, product_id)
);

INSERT INTO customers (id, name, email, city) VALUES
    (1, 'Lucía Torres',  'lucia.torres@example.com',  'Arequipa'),
    (2, 'María López',   'maria.lopez@example.com',   'Lima'),
    (3, 'Jorge Ríos',    'jorge.rios@example.com',    'Cusco'),
    (4, 'María López',   'mlopez.trujillo@example.com', 'Trujillo'),
    (5, 'Rosa Huamán',   'rosa.huaman@example.com',   'Arequipa'),
    (6, 'Pedro Salas',   'pedro.salas@example.com',   'Puno'),
    (7, 'Andrés Vega',   'andres.vega@example.com',   'Lima'),
    (8, 'Carla Mendoza', 'carla.mendoza@example.com', 'Tacna');

INSERT INTO products (id, name, category, price) VALUES
    (1, 'Cuaderno A4 cuadriculado', 'Cuadernos',  12.50),
    (2, 'Agenda 2027',              'Cuadernos',  39.90),
    (3, 'Lapicero gel azul x12',    'Escritura',  18.00),
    (4, 'Resaltadores x6',          'Escritura',  15.90),
    (5, 'Mochila escolar',          'Mochilas',  129.00),
    (6, 'Cartuchera doble',         'Mochilas',   34.75),
    (7, 'Papel bond A4 x500',       'Papel',      28.00),
    (8, 'Calculadora científica',   'Tecnología', 79.00),
    (9, 'Pizarra acrílica',         'Oficina',    65.00);

INSERT INTO orders (id, customer_id, ordered_at, status, shipping_fee) VALUES
    (101, 1,    '2026-09-05 10:20', 'entregado', 10.00),
    (102, 2,    '2026-09-18 16:45', 'entregado',  0.00),
    (103, 3,    '2026-10-02 09:00', 'entregado', 12.00),
    (104, 5,    '2026-10-10 18:30', 'cancelado', 10.00),
    (105, NULL, '2026-10-30 12:00', 'entregado', 15.00),
    (106, 4,    '2026-10-31 20:15', 'entregado', 10.00),
    (107, 1,    '2026-11-08 11:10', 'pagado',    10.00),
    (108, 8,    '2026-11-15 15:40', 'entregado', 12.00),
    (109, 7,    '2026-11-22 10:00', 'pendiente', 10.00),
    (110, 2,    '2026-11-30 09:30', 'pagado',     0.00),
    (111, 3,    '2026-11-26 19:05', 'cancelado', 12.00);

INSERT INTO order_items (order_id, product_id, quantity, unit_price) VALUES
    (101, 1, 4,  12.50),
    (101, 3, 1,  18.00),
    (102, 5, 1, 119.00),
    (102, 6, 1,  34.75),
    (103, 8, 1,  79.00),
    (104, 5, 3, 119.00),
    (105, 7, 3,  28.00),
    (105, 4, 2,  16.00),
    (106, 2, 2,  45.00),
    (106, 1, 2,  12.50),
    (107, 3, 2,  18.00),
    (107, 4, 1,  14.00),
    (108, 5, 2, 129.00),
    (109, 7, 2,  28.00),
    (110, 6, 2,  34.75),
    (110, 1, 1,  12.50),
    (111, 8, 1,  79.00);

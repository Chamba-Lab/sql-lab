-- The catalog of Conecta, a small online technology shop in Lima.
-- The acceptance tests run this script on a new, empty database before each
-- test, so every test starts from these same 17 products.
-- Do not change it: CREATE TABLE and INSERT are taught in block 3.
-- Brands are written as each supplier sent them (spaces, capital letters).
-- NULL means the data is missing; see BRIEF.md for what it means in each column.

CREATE TABLE products (
    id          INTEGER PRIMARY KEY,
    name        TEXT,
    brand       TEXT,
    category    TEXT,
    price       REAL,      -- list price, in soles
    promo_price REAL,      -- price during a promotion; NULL if it has none
    promo_ends  TEXT,      -- last day of the promotion, 'YYYY-MM-DD'; NULL if it has no end
    stock       INTEGER,   -- units in the warehouse; NULL if nobody counted them
    status      TEXT,      -- 'activo', 'pausado' or 'descontinuado'
    added_at    TEXT       -- when it entered the catalog, 'YYYY-MM-DD HH:MM'
);

INSERT INTO products (id, name, brand, category, price, promo_price, promo_ends, stock, status, added_at) VALUES
    (1,  'Audífonos Bluetooth AX2',     'Sony',     'Audio',      199.9,  149.9, '2026-11-30', 12,   'activo',        '2026-06-10 11:00'),
    (2,  'Parlante portátil bluetooth', 'sony ',    'Audio',      159.0,  NULL,  NULL,         0,    'activo',        '2026-11-02 16:30'),
    (3,  'Hub USB 4 puertos',           ' Anker',   'Accesorios', 79.9,   69.9,  '2026-11-19', 3,    'activo',        '2026-09-15 10:00'),
    (4,  'Adaptador USB-C a HDMI',      'Anker',    'Accesorios', 79.9,   NULL,  NULL,         40,   'activo',        '2026-10-21 09:00'),
    (5,  'Memoria USB 64 GB',           'Kingston', 'Accesorios', 39.9,   34.9,  '2026-11-20', 25,   'pausado',       '2026-11-10 12:00'),
    (6,  'Mouse inalámbrico M3',        'Logitech', 'Cómputo',    89.9,   79.9,  NULL,         8,    'activo',        '2026-11-12 18:40'),
    (7,  'Teclado mecánico K8',         'LOGITECH', 'Cómputo',    249.0,  NULL,  NULL,         6,    'activo',        '2026-10-20 23:00'),
    (8,  'Monitor 24 pulgadas',         'Samsung',  'Cómputo',    649.0,  577.0, '2026-12-15', NULL, 'activo',        '2026-08-01 09:30'),
    (9,  'Laptop 14 Ryzen 5',           'Lenovo',   'Cómputo',    2499.0, NULL,  NULL,         2,    'activo',        '2026-07-20 15:00'),
    (10, 'Funda para laptop 14',        NULL,       '',           49.9,   NULL,  NULL,         15,   'activo',        '2026-11-20 10:15'),
    (11, 'Soporte para celular',        NULL,       NULL,         24.9,   19.9,  '2026-11-25', 30,   'activo',        '2026-11-05 08:00'),
    (12, 'Cargador rápido 20 W',        'Xiaomi',   'Celulares',  59.9,   NULL,  NULL,         0,    'activo',        '2026-05-02 10:00'),
    (13, 'Celular Redmi 13',            'xiaomi',   'Celulares',  899.0,  849.0, '2026-11-20', 5,    'activo',        '2026-09-01 11:00'),
    (14, 'Smartwatch Band 9',           'Xiaomi ',  'Celulares',  179.0,  NULL,  NULL,         4,    'activo',        '2026-11-16 20:00'),
    (15, 'Cámara web HD',               'Logitech', 'Cómputo',    159.9,  129.9, '2026-12-31', NULL, 'descontinuado', '2026-03-03 10:00'),
    (16, 'Lámpara LED USB',             'Philips',  'Hogar',      34.9,   NULL,  NULL,         9,    'activo',        '2026-04-18 13:00'),
    (17, 'Audífonos con cable',         'Sony',     'Audio',      159.0,  NULL,  NULL,         20,   'activo',        '2026-02-14 10:00');

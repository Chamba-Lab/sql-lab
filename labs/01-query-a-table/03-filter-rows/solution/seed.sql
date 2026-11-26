-- The data of lab 1.3. The tests run this script on a new, empty database
-- before each test, so every test starts from these same 14 rows.
-- Do not change it: CREATE TABLE and INSERT are taught in block 3.

CREATE TABLE apartments (
    id       INTEGER PRIMARY KEY,
    district TEXT,
    title    TEXT,      -- the headline of the listing
    rent     INTEGER    -- monthly rent, in soles
);

INSERT INTO apartments (id, district, title, rent) VALUES
    (1,  'Miraflores',        'Departamento con vista al mar',    2600),
    (2,  'Miraflores',        'Cochera y depósito incluidos',     1800),
    (3,  'Miraflores',        'A dos cuadras del parque Kennedy', 1500),
    (4,  'Barranco',          'Loft con terraza',                 2000),
    (5,  'Barranco',          'Cerca al malecón, con cochera',    1750),
    (6,  'San Isidro',        'Con cochera para dos autos',       3100),
    (7,  'San Isidro',        'Frente al centro financiero',      2200),
    (8,  'San Borja',         'Amplio y con cochera techada',     1900),
    (9,  'San Miguel',        'Cerca a la universidad',           1200),
    (10, 'Santiago de Surco', 'Casa con jardín',                  2400),
    (11, 'Santiago de Surco', 'Condominio con piscina',           1650),
    (12, 'Jesús María',       'Frente al Campo de Marte',         1350),
    (13, 'Lince',             'Minidepartamento amoblado',        1100),
    (14, 'Pueblo Libre',      'Primer piso, con patio',           1250);

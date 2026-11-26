-- The job board of block 2 (the data of lab 2.1 plus job 11): companies, their job offers, the candidates and their applications.
-- Every test builds a fresh database from this file. Do not change it.

CREATE TABLE companies (
    id     INTEGER PRIMARY KEY,
    name   TEXT,
    city   TEXT,
    sector TEXT
);

CREATE TABLE jobs (
    id         INTEGER PRIMARY KEY,
    company_id INTEGER REFERENCES companies (id),
    title      TEXT,
    mode       TEXT,
    salary_usd INTEGER,
    posted_on  TEXT
);

CREATE TABLE candidates (
    id               INTEGER PRIMARY KEY,
    name             TEXT,
    city             TEXT,
    years_experience REAL,
    referred_by      INTEGER REFERENCES candidates (id)
);

CREATE TABLE applications (
    id           INTEGER PRIMARY KEY,
    candidate_id INTEGER REFERENCES candidates (id),
    job_id       INTEGER REFERENCES jobs (id),
    applied_on   TEXT,
    status       TEXT
);

INSERT INTO companies VALUES
    (1, 'Andes Retail', 'Lima', 'retail'),
    (2, 'Pago Fácil', 'Bogotá', 'fintech'),
    (3, 'Clínica Central', 'Arequipa', 'salud'),
    (4, 'Agro Norte', 'Trujillo', 'agroindustria'),
    (5, 'Banco Sur', 'Santiago', 'banca'),
    (6, 'Nube Andina', 'Lima', 'tecnología');

INSERT INTO jobs VALUES
    (1, 1, 'Analista de datos júnior', 'híbrido', 1200, '2026-11-03'),
    (2, 2, 'Desarrollador backend', 'remoto', 1800, '2026-11-05'),
    (3, 3, 'Soporte de TI', 'presencial', 825, '2026-11-06'),
    (4, 1, 'Analista de BI', 'presencial', 1500, '2026-11-10'),
    (5, 4, 'Practicante de datos', 'presencial', 600, '2026-11-12'),
    (6, 2, 'Desarrolladora full stack', 'remoto', 2000, '2026-11-14'),
    (7, 5, 'Administrador de bases de datos', 'híbrido', 2400, '2026-11-18'),
    (8, 3, 'Analista de calidad (QA)', 'remoto', 1150, '2026-11-20'),
    (9, 1, 'Practicante de marketing digital', 'presencial', NULL, '2026-11-21'),
    (10, 5, 'Analista de riesgos', 'híbrido', 1750, '2026-11-24'),
    (11, 4, 'Practicante de operaciones', 'presencial', 600, '2026-11-25');

INSERT INTO candidates VALUES
    (1, 'Ana Quispe', 'Lima', 0.5, NULL),
    (2, 'Luis Ramírez', 'Bogotá', 2.0, NULL),
    (3, 'María Torres', 'Arequipa', 1.0, 1),
    (4, 'Jorge Huamán', 'Lima', 0.0, 1),
    (5, 'Sofía Castro', 'Santiago', 3.5, NULL),
    (6, 'Luis Ramírez', 'Lima', 0.5, 4),
    (7, 'Carmen Rojas', 'Trujillo', 1.5, 3),
    (8, 'Diego Flores', 'Cusco', 4.0, NULL),
    (9, 'Valeria Paredes', 'Lima', 2.5, 5);

INSERT INTO applications VALUES
    (1, 1, 1, '2026-11-04', 'entrevista'),
    (2, 1, 4, '2026-11-11', 'enviada'),
    (3, 1, 5, '2026-11-13', 'rechazada'),
    (4, 2, 2, '2026-11-06', 'entrevista'),
    (5, 2, 6, '2026-11-15', 'enviada'),
    (6, 3, 3, '2026-11-07', 'contratada'),
    (7, 3, 8, '2026-11-21', 'enviada'),
    (8, 4, 1, '2026-11-05', 'enviada'),
    (9, 4, 5, '2026-11-12', 'entrevista'),
    (10, 5, 7, '2026-11-19', 'entrevista'),
    (11, 6, 1, '2026-11-06', 'rechazada'),
    (12, 6, 9, '2026-11-22', 'enviada'),
    (13, 7, 5, '2026-11-14', 'enviada'),
    (14, 9, 4, '2026-11-12', 'entrevista'),
    (15, 9, 7, '2026-11-20', 'enviada'),
    (16, 5, 6, '2026-11-16', 'rechazada');

"""Build the demo database of lab 1.1 next to this script.

Run it from this folder with:  python build_db.py
Running it again deletes jobs.db and builds it from scratch.
"""
import sqlite3
from pathlib import Path

DB_PATH = Path(__file__).parent / "jobs.db"

SCHEMA = """
CREATE TABLE jobs (
    id         INTEGER PRIMARY KEY,
    title      TEXT,
    company    TEXT,
    city       TEXT,
    mode       TEXT,
    salary_usd INTEGER,
    posted_on  TEXT
);

CREATE TABLE candidates (
    id               INTEGER PRIMARY KEY,
    name             TEXT,
    city             TEXT,
    years_experience REAL
);
"""

JOBS = [
    (1, "Analista de datos júnior", "Andes Retail", "Lima", "híbrido", 1200, "2026-11-03"),
    (2, "Desarrollador backend", "Pago Fácil", "Bogotá", "remoto", 1800, "2026-11-05"),
    (3, "Soporte de TI", "Clínica Central", "Arequipa", "presencial", 800, "2026-11-06"),
    (4, "Analista de BI", "Andes Retail", "Lima", "presencial", 1500, "2026-11-10"),
    (5, "Practicante de datos", "Agro Norte", "Trujillo", "presencial", 600, "2026-11-12"),
    (6, "Desarrolladora full stack", "Pago Fácil", "Ciudad de México", "remoto", 2000, "2026-11-14"),
    (7, "Administrador de bases de datos", "Banco Sur", "Santiago", "híbrido", 2400, "2026-11-18"),
    (8, "Analista de calidad (QA)", "Clínica Central", "Lima", "remoto", 1100, "2026-11-20"),
]

CANDIDATES = [
    (1, "Ana Quispe", "Lima", 0.5),
    (2, "Luis Ramírez", "Bogotá", 2.0),
    (3, "María Torres", "Arequipa", 1.0),
    (4, "Jorge Huamán", "Lima", 0.0),
    (5, "Sofía Castro", "Santiago", 3.5),
]


def build(path: Path = DB_PATH) -> None:
    """Create the database at `path`, replacing any previous file."""
    path.unlink(missing_ok=True)
    con = sqlite3.connect(path)
    try:
        con.executescript(SCHEMA)
        con.executemany("INSERT INTO jobs VALUES (?, ?, ?, ?, ?, ?, ?)", JOBS)
        con.executemany("INSERT INTO candidates VALUES (?, ?, ?, ?)", CANDIDATES)
        con.commit()
    finally:
        con.close()


if __name__ == "__main__":
    build()
    print(f"Listo: {DB_PATH.name} creado con 2 tablas.")

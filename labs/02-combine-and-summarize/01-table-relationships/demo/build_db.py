"""Build the demo database of lab 2.1 next to this script.

Run it from this folder with:  python build_db.py
Running it again deletes jobs.db and builds it from scratch, from seed.sql.
"""
import sqlite3
from pathlib import Path

HERE = Path(__file__).parent
DB_PATH = HERE / "jobs.db"
SEED_PATH = HERE / "seed.sql"


def build(path: Path = DB_PATH) -> None:
    """Create the database at `path` from seed.sql, replacing any previous file."""
    path.unlink(missing_ok=True)
    con = sqlite3.connect(path)
    try:
        con.executescript(SEED_PATH.read_text(encoding="utf-8"))
        con.commit()
    finally:
        con.close()


if __name__ == "__main__":
    build()
    print(f"Listo: {DB_PATH.name} creado.")

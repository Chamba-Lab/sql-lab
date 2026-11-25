"""Test harness of the course's SQL labs: run a .sql file on fresh data and compare its result.

Every test gets a new in-memory database built from ../seed.sql, runs one file of
../queries/ and compares the columns (names and order) and the rows (in any order)
with the expected result. Failure messages are in Spanish: learners read them.
"""
import codecs
import sqlite3
import sys
from collections import Counter
from pathlib import Path

import pytest

VARIANT = Path(__file__).resolve().parent.parent
SEED = VARIANT / "seed.sql"
QUERIES = VARIANT / "queries"

# Python 3.12 to 3.14 on Windows write to a pipe or a file (an agent, a CI log, > out.txt)
# in the ANSI code page, which garbles accents. UTF-8 reads well everywhere.
if hasattr(sys.__stdout__, "reconfigure"):
    sys.__stdout__.reconfigure(encoding="utf-8", errors="replace")


@pytest.fixture
def db():
    """A new database in memory, with the lab's data, for one test."""
    con = sqlite3.connect(":memory:")
    con.executescript(SEED.read_text(encoding="utf-8"))
    yield con
    con.close()


def read_sql(filename):
    """The text of one file of queries/, whatever encoding a Windows editor or shell used."""
    data = (QUERIES / filename).read_bytes()
    if data.startswith((codecs.BOM_UTF16_LE, codecs.BOM_UTF16_BE)):
        return data.decode("utf-16")  # PowerShell 5.1 writes `>` and Out-File in UTF-16
    try:
        return data.decode("utf-8-sig")  # UTF-8, with or without a byte-order mark
    except UnicodeDecodeError:
        pass  # fail outside the except block, or pytest also prints the decoding traceback
    pytest.fail(f"{filename}: no se pudo leer tu archivo porque no está guardado en UTF-8.\n"
                "  Vuelve a guardarlo como UTF-8 (en VS Code, haz clic en la codificación "
                "que aparece abajo a la derecha).", pytrace=False)


def run_file(con, filename):
    """Run one file of queries/ and return (column names, rows)."""
    sql = read_sql(filename)
    try:
        cursor = con.execute(sql)
    except sqlite3.Error as error:
        if isinstance(error, sqlite3.ProgrammingError) and "one statement" in str(error):
            # Typical when the query of a prediction stays above the query of the task.
            problem = ("Tu archivo tiene más de una consulta: deja solo una "
                       "(¿quedó arriba la de la predicción?).")
        else:
            problem = f"{type(error).__name__}: {error}"
    else:
        problem = None
    if problem:
        pytest.fail(f"{filename}: tu consulta dio un error.\n  {problem}", pytrace=False)
    columns = [d[0] for d in cursor.description] if cursor.description else []
    return columns, cursor.fetchall()


def show(rows, indent="    "):
    return "\n".join(f"{indent}{row!r}" for row in rows) or f"{indent}(ninguna)"


@pytest.fixture
def check(db):
    """check("01_x.sql", columns=[...], rows=[...]) fails with a readable message."""
    def check(filename, columns, rows):
        got_columns, got_rows = run_file(db, filename)
        if not got_columns:
            pytest.fail(f"{filename}: tu archivo no devolvió ningún resultado "
                        "(¿todavía tiene solo el TODO?).\n"
                        f"  Columnas esperadas: {', '.join(columns)}", pytrace=False)
        if got_columns != columns:
            pytest.fail(f"{filename}: las columnas no coinciden (importan el nombre y el orden).\n"
                        f"  Esperadas: {', '.join(columns)}\n"
                        f"  Obtenidas: {', '.join(got_columns)}\n"
                        f"  Tus primeras filas:\n{show(got_rows[:3])}", pytrace=False)
        expected, got = Counter(rows), Counter(got_rows)
        if got != expected:
            missing = list((expected - got).elements())
            extra = list((got - expected).elements())
            pytest.fail(f"{filename}: las columnas están bien, pero las filas no coinciden "
                        "(el orden de las filas no importa).\n"
                        f"  Filas esperadas: {len(rows)}; obtenidas: {len(got_rows)}\n"
                        f"  Esperadas que no salieron:\n{show(missing)}\n"
                        f"  Obtenidas que no se esperaban:\n{show(extra)}", pytrace=False)
    return check

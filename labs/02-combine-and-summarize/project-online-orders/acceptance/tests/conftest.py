"""Acceptance harness of project 2.P: run any folder of .sql files on the shop's orders.

Every test gets a new in-memory database built from ../seed.sql, runs one file of the
folder under test and compares the columns (names and order) and the rows (in the
expected order) with the result the brief asks for. The folder under test is
../my-queries by default; --queries=<folder> points at another one, such as the
reference: python -m pytest --queries=../reference/queries
Failure messages are in Spanish: learners read them.
"""
import codecs
import sqlite3
import sys
from collections import Counter
from pathlib import Path

import pytest

ACCEPTANCE = Path(__file__).resolve().parent.parent
SEED = ACCEPTANCE / "seed.sql"
DEFAULT_QUERIES = ACCEPTANCE.parent / "my-queries"

# Python 3.12 to 3.14 on Windows write to a pipe or a file (an agent, a CI log, > out.txt)
# in the ANSI code page, which garbles accents. UTF-8 reads well everywhere.
if hasattr(sys.__stdout__, "reconfigure"):
    sys.__stdout__.reconfigure(encoding="utf-8", errors="replace")


def pytest_addoption(parser):
    parser.addoption("--queries", default=None,
                     help="folder with the .sql files to check (default: ../my-queries)")


def pytest_sessionstart(session):
    """Find the folder under test once, relative to where pytest was started."""
    config = session.config
    given = config.getoption("--queries")
    folder = (config.invocation_params.dir / given).resolve() if given else DEFAULT_QUERIES
    if not folder.is_dir():
        pytest.exit(f"no encuentro la carpeta con tus consultas: {folder}\n"
                    "  Créala (ver el README del proyecto) o indica otra con --queries=<carpeta>.",
                    returncode=4)
    config.queries_folder = folder


@pytest.fixture
def queries(request):
    """The folder under test."""
    return request.config.queries_folder


@pytest.fixture
def db():
    """A new database in memory, with the shop's orders, for one test."""
    con = sqlite3.connect(":memory:")
    # Double quotes name a column ("name") and single quotes write a text ('Lima').
    # SQLite takes an unknown "Lima" as the text 'Lima', so a wrong query would pass;
    # the tests switch that quirk off and answer "no such column" instead.
    con.setconfig(sqlite3.SQLITE_DBCONFIG_DQS_DML, False)
    con.setconfig(sqlite3.SQLITE_DBCONFIG_DQS_DDL, False)
    con.executescript(SEED.read_text(encoding="utf-8"))
    yield con
    con.close()


def read_sql(path):
    """The text of one .sql file, whatever encoding a Windows editor or shell used."""
    if not path.is_file():
        pytest.fail(f"{path.name}: no existe en {path.parent}\n"
                    "  Crea el archivo con este nombre exacto (la lista está en BRIEF.md).",
                    pytrace=False)
    data = path.read_bytes()
    if data.startswith((codecs.BOM_UTF16_LE, codecs.BOM_UTF16_BE)):
        return data.decode("utf-16")  # PowerShell 5.1 writes `>` and Out-File in UTF-16
    try:
        return data.decode("utf-8-sig")  # UTF-8, with or without a byte-order mark
    except UnicodeDecodeError:
        pass  # fail outside the except block, or pytest also prints the decoding traceback
    pytest.fail(f"{path.name}: no se pudo leer tu archivo porque no está guardado en UTF-8.\n"
                "  Vuelve a guardarlo como UTF-8 (en VS Code, haz clic en la codificación "
                "que aparece abajo a la derecha).", pytrace=False)


NOW_HINT = ("\n  Recuerda: hoy es '2026-11-30', escrito como texto en la consulta; "
            "DATE('now') da el día real.")


def run_file(con, path):
    """Run one .sql file and return (column names, rows)."""
    sql = read_sql(path)
    hint = NOW_HINT if "'now'" in sql.lower() else ""
    try:
        cursor = con.execute(sql)
    except sqlite3.Error as error:
        if isinstance(error, sqlite3.ProgrammingError) and "one statement" in str(error):
            problem = "Tu archivo tiene más de una consulta: deja solo una."
        else:
            problem = f"{type(error).__name__}: {error}"
    else:
        problem = None
    if problem:
        pytest.fail(f"{path.name}: tu consulta dio un error.\n  {problem}", pytrace=False)
    columns = [d[0] for d in cursor.description] if cursor.description else []
    return columns, cursor.fetchall(), hint


def show(rows, indent="    "):
    return "\n".join(f"{indent}{row!r}" for row in rows) or f"{indent}(ninguna)"


def numbered(rows, indent="    "):
    return "\n".join(f"{indent}{n:>2}. {row!r}" for n, row in enumerate(rows, start=1))


@pytest.fixture
def check_ordered(db, queries):
    """check_ordered("01_x.sql", columns=[...], rows=[...]): columns, then rows, then their order."""
    def check_ordered(filename, columns, rows):
        path = queries / filename
        got_columns, got_rows, hint = run_file(db, path)
        if not got_columns:
            pytest.fail(f"{filename}: tu archivo no devolvió ningún resultado "
                        "(¿tiene solo comentarios?).\n"
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
                        "(sin mirar el orden).\n"
                        f"  Filas esperadas: {len(rows)}; obtenidas: {len(got_rows)}\n"
                        f"  Esperadas que no salieron:\n{show(missing)}\n"
                        f"  Obtenidas que no se esperaban:\n{show(extra)}{hint}", pytrace=False)
        if got_rows != rows:
            first = next(n for n, (a, b) in enumerate(zip(rows, got_rows), start=1) if a != b)
            pytest.fail(f"{filename}: las filas son las correctas, pero no están en el orden pedido.\n"
                        f"  La primera fila fuera de lugar es la {first}.\n"
                        f"  Orden esperado:\n{numbered(rows)}\n"
                        f"  Orden obtenido:\n{numbered(got_rows)}{hint}", pytrace=False)
    return check_ordered

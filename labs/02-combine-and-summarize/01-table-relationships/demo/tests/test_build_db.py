"""Guards for the guide of lab 2.1: the database and the console behave as the README quotes."""
import os
import sqlite3
import subprocess
import sys

import pytest

from build_db import build


@pytest.fixture
def db(tmp_path):
    path = tmp_path / "jobs.db"
    build(path)
    return path


def query(path, sql):
    con = sqlite3.connect(path)
    try:
        return con.execute(sql).fetchall()
    finally:
        con.close()


def run_console(*args):
    """Run `python -m sqlite3 <args>` the way the guide does, and return the finished process."""
    env = {**os.environ, "PYTHONIOENCODING": "utf-8"}
    return subprocess.run(
        [sys.executable, "-m", "sqlite3", *map(str, args)],
        capture_output=True, text=True, encoding="utf-8", errors="replace", env=env, timeout=60,
    )


class TestDatabase:
    def test_schema_lists_the_four_tables(self, db):
        assert query(db, "SELECT type, name FROM sqlite_schema;") == [
            ("table", "companies"), ("table", "jobs"), ("table", "candidates"), ("table", "applications"),
        ]

    def test_columns_match_the_diagram(self, db):
        columns = {
            table: query(db, f"SELECT name, type, pk FROM pragma_table_info('{table}');")
            for table in ("companies", "jobs", "candidates", "applications")
        }
        assert columns == {
            "companies": [("id", "INTEGER", 1), ("name", "TEXT", 0), ("city", "TEXT", 0), ("sector", "TEXT", 0)],
            "jobs": [("id", "INTEGER", 1), ("company_id", "INTEGER", 0), ("title", "TEXT", 0),
                     ("mode", "TEXT", 0), ("salary_usd", "INTEGER", 0), ("posted_on", "TEXT", 0)],
            "candidates": [("id", "INTEGER", 1), ("name", "TEXT", 0), ("city", "TEXT", 0),
                           ("years_experience", "REAL", 0), ("referred_by", "INTEGER", 0)],
            "applications": [("id", "INTEGER", 1), ("candidate_id", "INTEGER", 0), ("job_id", "INTEGER", 0),
                             ("applied_on", "TEXT", 0), ("status", "TEXT", 0)],
        }

    def test_foreign_keys_match_the_diagram(self, db):
        fks = 'SELECT "table", "from", "to" FROM pragma_foreign_key_list(\'{}\');'
        assert query(db, fks.format("companies")) == []
        assert query(db, fks.format("jobs")) == [("companies", "company_id", "id")]
        assert query(db, fks.format("candidates")) == [("candidates", "referred_by", "id")]
        assert query(db, fks.format("applications")) == [
            ("jobs", "job_id", "id"), ("candidates", "candidate_id", "id"),
        ]

    def test_no_orphans_in_the_seed(self, db):
        assert query(db, "PRAGMA foreign_key_check;") == []

    def test_row_counts(self, db):
        counts = [query(db, f"SELECT count(*) FROM {t};")[0][0]
                  for t in ("companies", "jobs", "candidates", "applications")]
        assert counts == [6, 10, 9, 16]

    def test_rows_quoted_in_the_guide(self, db):
        assert query(db, "SELECT * FROM jobs WHERE id = 4;") == [
            (4, 1, "Analista de BI", "presencial", 1500, "2026-11-10")]
        assert query(db, "SELECT * FROM companies WHERE id = 1;") == [(1, "Andes Retail", "Lima", "retail")]
        assert query(db, "SELECT id, title FROM jobs WHERE company_id = 1;") == [
            (1, "Analista de datos júnior"), (4, "Analista de BI"), (9, "Practicante de marketing digital")]
        assert query(db, "SELECT id, title FROM jobs WHERE company_id = 6;") == []
        assert query(db, "SELECT * FROM candidates WHERE name = 'Luis Ramírez';") == [
            (2, "Luis Ramírez", "Bogotá", 2.0, None), (6, "Luis Ramírez", "Lima", 0.5, 4)]
        assert query(db, "SELECT * FROM applications WHERE candidate_id = 6;") == [
            (11, 6, 1, "2026-11-06", "rechazada"), (12, 6, 9, "2026-11-22", "enviada")]
        assert query(db, "SELECT * FROM candidates WHERE id = 4;") == [(4, "Jorge Huamán", "Lima", 0.0, 1)]
        assert query(db, "SELECT * FROM applications WHERE job_id = 1;") == [
            (1, 1, 1, "2026-11-04", "entrevista"), (8, 4, 1, "2026-11-05", "enviada"),
            (11, 6, 1, "2026-11-06", "rechazada")]
        assert query(db, "SELECT * FROM applications WHERE candidate_id = 1;") == [
            (1, 1, 1, "2026-11-04", "entrevista"), (2, 1, 4, "2026-11-11", "enviada"),
            (3, 1, 5, "2026-11-13", "rechazada")]

    def test_extra_challenge_chain_ends_after_three_people(self, db):
        chain, current = [], 7
        while current is not None:
            chain.append(current)
            current = query(db, f"SELECT referred_by FROM candidates WHERE id = {current};")[0][0]
        assert chain == [7, 3, 1]

    def test_building_again_replaces_the_file(self, db):
        con = sqlite3.connect(db)
        con.execute("INSERT INTO applications VALUES (17, 1, 99, '2026-11-25', 'enviada');")
        con.commit()
        con.close()
        build(db)
        assert query(db, "SELECT count(*) FROM applications;") == [(16,)]


class TestScript:
    def test_build_prints_the_quoted_message(self, tmp_path):
        import shutil
        from pathlib import Path
        demo = Path(__file__).resolve().parent.parent
        for name in ("build_db.py", "seed.sql"):
            shutil.copy(demo / name, tmp_path / name)
        result = subprocess.run([sys.executable, "build_db.py"], cwd=tmp_path, capture_output=True,
                                text=True, encoding="utf-8", timeout=60)
        assert result.returncode == 0, result.stderr
        assert result.stdout.splitlines() == ["Listo: jobs.db creado."]
        assert (tmp_path / "jobs.db").exists()


class TestConsole:
    def test_one_shot_query_prints_one_tuple_per_row(self, db):
        result = run_console(db, "SELECT * FROM candidates WHERE name = 'Luis Ramírez';")
        assert result.returncode == 0, result.stderr
        assert result.stdout.splitlines() == [
            "(2, 'Luis Ramírez', 'Bogotá', 2.0, None)",
            "(6, 'Luis Ramírez', 'Lima', 0.5, 4)",
        ]

    def test_repeated_primary_key_is_rejected(self, db):
        result = run_console(db, "INSERT INTO candidates VALUES (6, 'Rosa Medina', 'Cusco', 1.0, NULL);")
        assert result.returncode == 1
        assert "IntegrityError (SQLITE_CONSTRAINT_PRIMARYKEY): UNIQUE constraint failed: candidates.id" in result.stderr
        assert query(db, "SELECT name FROM candidates WHERE id = 6;") == [("Luis Ramírez",)]
        assert query(db, "SELECT count(*) FROM candidates;") == [(9,)]

    def test_orphan_reference_is_accepted_and_kept(self, db):
        result = run_console(db, "INSERT INTO applications VALUES (17, 1, 99, '2026-11-25', 'enviada');")
        assert result.returncode == 0, result.stderr
        assert result.stdout == ""
        assert query(db, "SELECT * FROM applications WHERE job_id = 99;") == [
            (17, 1, 99, "2026-11-25", "enviada")]
        assert query(db, "SELECT * FROM jobs WHERE id = 99;") == []

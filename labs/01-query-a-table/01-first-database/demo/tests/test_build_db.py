"""Guards for the guide of lab 1.1: the database and the console behave as the README quotes."""
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
    def test_schema_lists_only_the_two_tables(self, db):
        assert query(db, "SELECT type, name FROM sqlite_schema;") == [
            ("table", "jobs"), ("table", "candidates"),
        ]

    def test_jobs_columns_and_types(self, db):
        assert query(db, "SELECT name, type FROM pragma_table_info('jobs');") == [
            ("id", "INTEGER"), ("title", "TEXT"), ("company", "TEXT"), ("city", "TEXT"),
            ("mode", "TEXT"), ("salary_usd", "INTEGER"), ("posted_on", "TEXT"),
        ]

    def test_candidates_columns_and_types(self, db):
        assert query(db, "SELECT name, type FROM pragma_table_info('candidates');") == [
            ("id", "INTEGER"), ("name", "TEXT"), ("city", "TEXT"), ("years_experience", "REAL"),
        ]

    def test_row_counts(self, db):
        assert query(db, "SELECT count(*) FROM jobs;") == [(8,)]
        assert query(db, "SELECT count(*) FROM candidates;") == [(5,)]

    def test_building_again_replaces_the_file(self, db):
        build(db)
        assert query(db, "SELECT count(*) FROM jobs;") == [(8,)]


class TestConsole:
    def test_one_shot_query_prints_one_tuple_per_row(self, db):
        result = run_console(db, "SELECT * FROM candidates;")
        assert result.returncode == 0, result.stderr
        lines = result.stdout.splitlines()
        assert len(lines) == 5
        assert lines[0] == "(1, 'Ana Quispe', 'Lima', 0.5)"
        assert lines[1] == "(2, 'Luis Ramírez', 'Bogotá', 2.0)"

    def test_misspelled_file_is_created_empty(self, db):
        typo = db.with_name("job.db")
        assert not typo.exists()
        result = run_console(typo, "SELECT * FROM jobs;")
        assert result.returncode == 1
        assert "no such table: jobs" in result.stderr
        assert typo.exists() and typo.stat().st_size == 0

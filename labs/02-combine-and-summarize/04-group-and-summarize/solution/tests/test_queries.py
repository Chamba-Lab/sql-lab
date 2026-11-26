"""Tests of lab 2.4: one class per task, each one runs a file of queries/.

No task asks for an order, so the tests use check: the rows may come in any order.
"""


class TestSeed:
    """Guard: green from the start. It fails only if seed.sql was changed."""

    def test_rows_of_each_table(self, db):
        counts = [db.execute(f"SELECT count(*) FROM {table};").fetchone()[0]
                  for table in ("companies", "jobs", "candidates", "applications")]
        assert counts == [6, 10, 9, 16]


class TestTask1ApplicationSummary:
    def test_summary_of_all_applications(self, check):
        check("01_application_summary.sql",
              columns=["applications", "candidates", "jobs", "first_applied", "last_applied"],
              rows=[(16, 8, 9, "2026-11-04", "2026-11-22")])


class TestTask2SalaryByCompany:
    def test_jobs_and_average_salary_of_each_company(self, check):
        check("02_salary_by_company.sql", columns=["company", "jobs", "avg_salary"], rows=[
            ("Andes Retail", 3, 1350.0),
            ("Pago Fácil", 2, 1900.0),
            ("Clínica Central", 2, 987.5),
            ("Agro Norte", 1, 600.0),
            ("Banco Sur", 2, 2075.0),
        ])


class TestTask3ApplicationsByCandidate:
    def test_applications_of_each_candidate(self, check):
        check("03_applications_by_candidate.sql", columns=["id", "name", "applications"], rows=[
            (1, "Ana Quispe", 3),
            (2, "Luis Ramírez", 2),
            (3, "María Torres", 2),
            (4, "Jorge Huamán", 2),
            (5, "Sofía Castro", 2),
            (6, "Luis Ramírez", 2),
            (7, "Carmen Rojas", 1),
            (9, "Valeria Paredes", 2),
        ])


class TestTask4ApplicationsByCompany:
    def test_applications_received_by_every_company(self, check):
        check("04_applications_by_company.sql", columns=["company", "applications"], rows=[
            ("Andes Retail", 6),
            ("Pago Fácil", 3),
            ("Clínica Central", 2),
            ("Agro Norte", 3),
            ("Banco Sur", 2),
            ("Nube Andina", 0),
        ])

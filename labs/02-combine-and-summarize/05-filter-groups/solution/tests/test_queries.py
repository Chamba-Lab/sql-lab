"""Tests of lab 2.5: one class per task, each one runs a file of queries/.

No task asks for an order, so the tests use check: the rows may come in any order.
"""


class TestSeed:
    """Guard: green from the start. It fails only if seed.sql was changed."""

    def test_rows_of_each_table(self, db):
        counts = [db.execute(f"SELECT count(*) FROM {table};").fetchone()[0]
                  for table in ("companies", "jobs", "candidates", "applications")]
        assert counts == [6, 11, 9, 16]


class TestTask1PopularJobs:
    def test_jobs_with_two_or_more_applications(self, check):
        check("01_popular_jobs.sql", columns=["id", "title", "applications"], rows=[
            (1, "Analista de datos júnior", 3),
            (4, "Analista de BI", 2),
            (5, "Practicante de datos", 3),
            (6, "Desarrolladora full stack", 2),
            (7, "Administrador de bases de datos", 2),
        ])


class TestTask2ActiveCandidates:
    def test_candidates_with_two_or_more_applications_not_rejected(self, check):
        check("02_active_candidates.sql", columns=["id", "name", "applications"], rows=[
            (1, "Ana Quispe", 2),
            (2, "Luis Ramírez", 2),
            (3, "María Torres", 2),
            (4, "Jorge Huamán", 2),
            (9, "Valeria Paredes", 2),
        ])


class TestTask3JobsAndApplicationsByCompany:
    def test_jobs_and_applications_of_every_company(self, check):
        check("03_jobs_and_applications_by_company.sql",
              columns=["company", "jobs", "applications"], rows=[
                  ("Andes Retail", 3, 6),
                  ("Pago Fácil", 2, 3),
                  ("Clínica Central", 2, 2),
                  ("Agro Norte", 2, 3),
                  ("Banco Sur", 2, 2),
                  ("Nube Andina", 0, 0),
              ])


class TestTask4SalaryAndApplicationsByCompany:
    def test_total_salary_and_applications_of_each_company(self, check):
        check("04_salary_and_applications_by_company.sql",
              columns=["company", "total_salary", "applications"], rows=[
                  ("Andes Retail", 2700, 6),
                  ("Pago Fácil", 3800, 3),
                  ("Clínica Central", 1975, 2),
                  ("Agro Norte", 1200, 3),
                  ("Banco Sur", 4150, 2),
              ])

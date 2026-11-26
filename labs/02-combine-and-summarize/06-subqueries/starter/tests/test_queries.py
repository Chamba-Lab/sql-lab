"""Tests of lab 2.6: one class per task, each one runs a file of queries/.

No task asks for an order, so the tests use check: the rows may come in any order.
"""


class TestSeed:
    """Guard: green from the start. It fails only if seed.sql was changed."""

    def test_rows_of_each_table(self, db):
        counts = [db.execute(f"SELECT count(*) FROM {table};").fetchone()[0]
                  for table in ("companies", "jobs", "candidates", "applications")]
        assert counts == [6, 10, 9, 16]


class TestTask1JobsAboveAndesRetail:
    def test_jobs_paying_more_than_the_best_paid_andes_retail_job(self, check):
        check("01_jobs_above_andes_retail.sql", columns=["id", "title", "salary_usd"], rows=[
            (2, "Desarrollador backend", 1800),
            (6, "Desarrolladora full stack", 2000),
            (7, "Administrador de bases de datos", 2400),
            (10, "Analista de riesgos", 1750),
        ])


class TestTask2RemoteApplicants:
    def test_candidates_who_applied_to_a_remote_job(self, check):
        check("02_remote_applicants.sql", columns=["id", "name"], rows=[
            (2, "Luis Ramírez"),
            (3, "María Torres"),
            (5, "Sofía Castro"),
        ])


class TestTask3JobsAboveCompanyAverage:
    def test_jobs_paying_more_than_the_average_of_their_company(self, check):
        check("03_jobs_above_company_average.sql", columns=["id", "title", "salary_usd"], rows=[
            (4, "Analista de BI", 1500),
            (6, "Desarrolladora full stack", 2000),
            (7, "Administrador de bases de datos", 2400),
            (8, "Analista de calidad (QA)", 1150),
        ])


class TestTask4CandidatesWhoReferredNobody:
    def test_candidates_who_referred_nobody(self, check):
        check("04_candidates_who_referred_nobody.sql", columns=["id", "name"], rows=[
            (2, "Luis Ramírez"),
            (6, "Luis Ramírez"),
            (7, "Carmen Rojas"),
            (8, "Diego Flores"),
            (9, "Valeria Paredes"),
        ])

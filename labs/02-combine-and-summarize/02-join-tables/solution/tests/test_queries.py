"""Tests of lab 2.2: one class per task, each one runs a file of queries/.

No task asks for an order, so the tests use check: the rows may come in any order.
"""


class TestSeed:
    """Guard: green from the start. It fails only if seed.sql was changed."""

    def test_rows_of_each_table(self, db):
        counts = [db.execute(f"SELECT count(*) FROM {table};").fetchone()[0]
                  for table in ("companies", "jobs", "candidates", "applications")]
        assert counts == [6, 10, 9, 16]


class TestTask1JobsWithCompany:
    def test_every_job_with_its_company(self, check):
        check("01_jobs_with_company.sql", columns=["id", "title", "company", "sector"], rows=[
            (1, "Analista de datos júnior", "Andes Retail", "retail"),
            (2, "Desarrollador backend", "Pago Fácil", "fintech"),
            (3, "Soporte de TI", "Clínica Central", "salud"),
            (4, "Analista de BI", "Andes Retail", "retail"),
            (5, "Practicante de datos", "Agro Norte", "agroindustria"),
            (6, "Desarrolladora full stack", "Pago Fácil", "fintech"),
            (7, "Administrador de bases de datos", "Banco Sur", "banca"),
            (8, "Analista de calidad (QA)", "Clínica Central", "salud"),
            (9, "Practicante de marketing digital", "Andes Retail", "retail"),
            (10, "Analista de riesgos", "Banco Sur", "banca"),
        ])


class TestTask2Interviews:
    def test_interviews_with_person_and_job(self, check):
        check("02_interviews.sql", columns=["candidate", "title", "applied_on"], rows=[
            ("Ana Quispe", "Analista de datos júnior", "2026-11-04"),
            ("Luis Ramírez", "Desarrollador backend", "2026-11-06"),
            ("Jorge Huamán", "Practicante de datos", "2026-11-12"),
            ("Sofía Castro", "Administrador de bases de datos", "2026-11-19"),
            ("Valeria Paredes", "Analista de BI", "2026-11-12"),
        ])


class TestTask3CandidateHistory:
    def test_history_of_candidate_6(self, check):
        check("03_candidate_history.sql", columns=["title", "company", "status"], rows=[
            ("Analista de datos júnior", "Andes Retail", "rechazada"),
            ("Practicante de marketing digital", "Andes Retail", "enviada"),
        ])


class TestTask4Referrals:
    def test_who_recommended_each_candidate(self, check):
        check("04_referrals.sql", columns=["candidate", "recommender"], rows=[
            ("María Torres", "Ana Quispe"),
            ("Jorge Huamán", "Ana Quispe"),
            ("Luis Ramírez", "Jorge Huamán"),
            ("Carmen Rojas", "María Torres"),
            ("Valeria Paredes", "Sofía Castro"),
        ])

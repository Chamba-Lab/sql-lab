"""Tests of lab 2.3: one class per task, each one runs a file of queries/.

No task asks for an order, so the tests use check: the rows may come in any order.
None stands for NULL: a row with no match has NULL in the columns of the other table.
"""


class TestSeed:
    """Guard: green from the start. It fails only if seed.sql was changed."""

    def test_rows_of_each_table(self, db):
        counts = [db.execute(f"SELECT count(*) FROM {table};").fetchone()[0]
                  for table in ("companies", "jobs", "candidates", "applications")]
        assert counts == [6, 10, 9, 16]


class TestTask1CompaniesWithJobs:
    def test_every_company_with_its_jobs(self, check):
        check("01_companies_with_jobs.sql", columns=["company", "title"], rows=[
            ("Andes Retail", "Analista de datos júnior"),
            ("Andes Retail", "Analista de BI"),
            ("Andes Retail", "Practicante de marketing digital"),
            ("Pago Fácil", "Desarrollador backend"),
            ("Pago Fácil", "Desarrolladora full stack"),
            ("Clínica Central", "Soporte de TI"),
            ("Clínica Central", "Analista de calidad (QA)"),
            ("Agro Norte", "Practicante de datos"),
            ("Banco Sur", "Administrador de bases de datos"),
            ("Banco Sur", "Analista de riesgos"),
            ("Nube Andina", None),
        ])


class TestTask2CandidatesWithJobs:
    def test_every_candidate_with_the_jobs_they_applied_to(self, check):
        check("02_candidates_with_jobs.sql", columns=["id", "name", "title"], rows=[
            (1, "Ana Quispe", "Analista de datos júnior"),
            (1, "Ana Quispe", "Analista de BI"),
            (1, "Ana Quispe", "Practicante de datos"),
            (2, "Luis Ramírez", "Desarrollador backend"),
            (2, "Luis Ramírez", "Desarrolladora full stack"),
            (3, "María Torres", "Soporte de TI"),
            (3, "María Torres", "Analista de calidad (QA)"),
            (4, "Jorge Huamán", "Analista de datos júnior"),
            (4, "Jorge Huamán", "Practicante de datos"),
            (5, "Sofía Castro", "Administrador de bases de datos"),
            (5, "Sofía Castro", "Desarrolladora full stack"),
            (6, "Luis Ramírez", "Analista de datos júnior"),
            (6, "Luis Ramírez", "Practicante de marketing digital"),
            (7, "Carmen Rojas", "Practicante de datos"),
            (8, "Diego Flores", None),
            (9, "Valeria Paredes", "Analista de BI"),
            (9, "Valeria Paredes", "Administrador de bases de datos"),
        ])


class TestTask3CompaniesWithoutJobs:
    def test_companies_with_no_jobs(self, check):
        check("03_companies_without_jobs.sql", columns=["id", "name"], rows=[
            (6, "Nube Andina"),
        ])


class TestTask4RemoteJobsByCompany:
    def test_every_company_with_its_remote_jobs(self, check):
        check("04_remote_jobs_by_company.sql", columns=["company", "title"], rows=[
            ("Andes Retail", None),
            ("Pago Fácil", "Desarrollador backend"),
            ("Pago Fácil", "Desarrolladora full stack"),
            ("Clínica Central", "Analista de calidad (QA)"),
            ("Agro Norte", None),
            ("Banco Sur", None),
            ("Nube Andina", None),
        ])

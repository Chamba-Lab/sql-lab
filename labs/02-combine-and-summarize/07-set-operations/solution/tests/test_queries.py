"""Tests of lab 2.7: one class per task, each one runs a file of queries/.

No task asks for an order, so the tests use check: the rows may come in any order.
"""


class TestSeed:
    """Guard: green from the start. It fails only if seed.sql was changed."""

    def test_rows_of_each_table(self, db):
        counts = [db.execute(f"SELECT count(*) FROM {table};").fetchone()[0]
                  for table in ("companies", "jobs", "candidates", "applications")]
        assert counts == [6, 10, 9, 16]


class TestTask1ContactDirectory:
    def test_name_and_city_of_every_company_and_candidate(self, check):
        check("01_contact_directory.sql", columns=["name", "city"], rows=[
            ("Andes Retail", "Lima"),
            ("Pago Fácil", "Bogotá"),
            ("Clínica Central", "Arequipa"),
            ("Agro Norte", "Trujillo"),
            ("Banco Sur", "Santiago"),
            ("Nube Andina", "Lima"),
            ("Ana Quispe", "Lima"),
            ("Luis Ramírez", "Bogotá"),
            ("María Torres", "Arequipa"),
            ("Jorge Huamán", "Lima"),
            ("Sofía Castro", "Santiago"),
            ("Luis Ramírez", "Lima"),
            ("Carmen Rojas", "Trujillo"),
            ("Diego Flores", "Cusco"),
            ("Valeria Paredes", "Lima"),
        ])


class TestTask2TotalEvents:
    def test_jobs_posted_plus_applications(self, check):
        check("02_total_events.sql", columns=["events"], rows=[(26,)])


class TestTask3SharedCities:
    def test_cities_with_a_company_and_a_candidate(self, check):
        check("03_shared_cities.sql", columns=["city"], rows=[
            ("Arequipa",),
            ("Bogotá",),
            ("Lima",),
            ("Santiago",),
            ("Trujillo",),
        ])


class TestTask4CandidateOnlyCities:
    def test_cities_with_candidates_and_no_company(self, check):
        check("04_candidate_only_cities.sql", columns=["city"], rows=[
            ("Cusco",),
        ])

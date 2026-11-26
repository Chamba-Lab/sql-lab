"""Tests of lab 1.3: one class per task, each one runs a file of queries/."""


class TestSeed:
    """Guard: green from the start. It fails only if seed.sql was changed."""

    def test_fourteen_apartments(self, db):
        assert db.execute("SELECT count(*) FROM apartments;").fetchone() == (14,)


class TestTask1Miraflores:
    def test_apartments_in_miraflores(self, check):
        check("01_miraflores.sql", columns=["id", "title", "rent"], rows=[
            (1, "Departamento con vista al mar", 2600),
            (2, "Cochera y depósito incluidos", 1800),
            (3, "A dos cuadras del parque Kennedy", 1500),
        ])


class TestTask2RentRange:
    def test_rent_from_1200_to_1800_both_included(self, check):
        check("02_rent_range.sql", columns=["id", "district", "rent"], rows=[
            (2, "Miraflores", 1800),
            (3, "Miraflores", 1500),
            (5, "Barranco", 1750),
            (9, "San Miguel", 1200),
            (11, "Santiago de Surco", 1650),
            (12, "Jesús María", 1350),
            (14, "Pueblo Libre", 1250),
        ])


class TestTask3TwoDistricts:
    def test_miraflores_or_barranco_under_2000(self, check):
        check("03_two_districts.sql", columns=["id", "district", "rent"], rows=[
            (2, "Miraflores", 1800),
            (3, "Miraflores", 1500),
            (5, "Barranco", 1750),
        ])


class TestTask4Parking:
    def test_listings_that_mention_cochera(self, check):
        check("04_parking.sql", columns=["id", "district", "title"], rows=[
            (2, "Miraflores", "Cochera y depósito incluidos"),
            (5, "Barranco", "Cerca al malecón, con cochera"),
            (6, "San Isidro", "Con cochera para dos autos"),
            (8, "San Borja", "Amplio y con cochera techada"),
        ])


class TestTask5OtherBranch:
    def test_districts_of_the_other_branch(self, check):
        check("05_other_branch.sql", columns=["id", "district"], rows=[
            (1, "Miraflores"),
            (2, "Miraflores"),
            (3, "Miraflores"),
            (4, "Barranco"),
            (5, "Barranco"),
            (10, "Santiago de Surco"),
            (11, "Santiago de Surco"),
            (12, "Jesús María"),
            (13, "Lince"),
            (14, "Pueblo Libre"),
        ])

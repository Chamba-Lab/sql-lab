"""Tests of lab 1.6: one class per task, each one runs a file of queries/.

No task asks for an order, so every test uses check (rows in any order).
"""


class TestSeed:
    """Guard: green from the start. It fails only if seed.sql was changed."""

    def test_ten_applications(self, db):
        assert db.execute("SELECT count(*) FROM applications;").fetchone() == (10,)


class TestTask1FullName:
    def test_full_names(self, check):
        check("01_full_name.sql", columns=["id", "full_name"], rows=[
            (1, "Ana Torres"),
            (2, "Luis Quispe"),
            (3, "Rosa Mamani"),
            (4, "Diego"),
            (5, "Carla Huamán"),
            (6, "Jorge Salazar"),
            (7, "Valeria Ríos"),
            (8, "Miguel Paredes"),
            (9, "Lucía Fernández"),
            (10, "Pedro Vargas"),
        ])


class TestTask2CleanEmails:
    def test_clean_emails(self, check):
        check("02_clean_emails.sql", columns=["id", "email"], rows=[
            (1, "ana.torres@gmail.com"),
            (2, "luis.quispe@hotmail.com"),
            (3, "rosa.mamani@gmail.com"),
            (4, "diego.r@gmail.com"),
            (5, "carla.huaman@outlook.com"),
            (6, None),
            (7, "vale.rios@gmail.com"),
            (8, "miguel.paredes@gmail.com"),
            (9, "lucia.fdz@yahoo.com"),
            (10, "pedro.vargas@gmail.com"),
        ])


class TestTask3JobArea:
    def test_codes_and_areas(self, check):
        check("03_job_area.sql", columns=["id", "job_code", "area"], rows=[
            (1, "DAT-104", "DAT"),
            (2, "DEV-310", "DEV"),
            (3, "SOP-007", "SOP"),
            (4, "DAT-221", "DAT"),
            (5, "DEV-118", "DEV"),
            (6, "SOP-015", "SOP"),
            (7, "DAT-104", "DAT"),
            (8, "DEV-310", "DEV"),
            (9, "DAT-221", "DAT"),
            (10, "SOP-007", "SOP"),
        ])


class TestTask4March:
    def test_applications_of_march_2026(self, check):
        check("04_march.sql", columns=["id", "applied_at"], rows=[
            (1, "2026-03-12 10:30"),
            (3, "2026-03-01 08:15"),
            (5, "2026-03-31 18:20"),
            (8, "2026-03-20 16:45"),
            (9, "2026-03-05 09:10"),
        ])


class TestTask5ReplyBy:
    def test_reply_deadlines(self, check):
        check("05_reply_by.sql", columns=["id", "applied_on", "reply_by"], rows=[
            (1, "2026-03-12", "2026-03-19"),
            (2, "2026-02-28", "2026-03-07"),
            (3, "2026-03-01", "2026-03-08"),
            (4, "2026-04-01", "2026-04-08"),
            (5, "2026-03-31", "2026-04-07"),
            (6, "2025-03-20", "2025-03-27"),
            (7, "2026-01-15", "2026-01-22"),
            (8, "2026-03-20", "2026-03-27"),
            (9, "2026-03-05", "2026-03-12"),
            (10, "2026-02-10", "2026-02-17"),
        ])


class TestTask6SalaryBand:
    def test_salary_bands(self, check):
        check("06_salary_band.sql", columns=["id", "expected_salary", "salary_band"], rows=[
            (1, 1800, "medio"),
            (2, 2500, "alto"),
            (3, 1200, "bajo"),
            (4, None, "sin dato"),
            (5, 3200, "alto"),
            (6, 1500, "medio"),
            (7, 1450, "bajo"),
            (8, 2200, "medio"),
            (9, 1000, "bajo"),
            (10, 2800, "alto"),
        ])

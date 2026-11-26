"""Tests of lab 1.5: one class per task, each one runs a file of queries/.

Every task asks for an order, so the tests use check_ordered: the rows must be
the expected ones and come in the expected order.
"""


class TestSeed:
    """Guard: green from the start. It fails only if seed.sql was changed."""

    def test_twelve_courses(self, db):
        assert db.execute("SELECT count(*) FROM courses;").fetchone() == (12,)


class TestTask1MostPopular:
    def test_courses_by_students(self, check_ordered):
        check_ordered("01_most_popular.sql", columns=["title", "students", "year"], rows=[
            ("Git y GitHub", 1530, 2023),
            ("Excel avanzado", 1250, 2024),
            ("SQL desde cero", 1250, 2023),
            ("Python para análisis de datos", 980, 2023),
            ("Marketing digital", 760, 2025),
            ("JavaScript moderno", 760, 2024),
            ("Django para la web", 540, 2025),
            ("Figma para principiantes", 430, 2025),
            ("Diseño de logos", 310, 2024),
            ("Estadística para no estadísticos", 210, 2026),
            ("Power BI en la práctica", 120, 2026),
            ("Finanzas personales", 85, 2026),
        ])


class TestTask2ToReview:
    def test_courses_from_the_lowest_rating(self, check_ordered):
        check_ordered("02_to_review.sql", columns=["title", "rating", "students"], rows=[
            ("Diseño de logos", 3.9, 310),
            ("Marketing digital", 4.1, 760),
            ("Figma para principiantes", 4.2, 430),
            ("Django para la web", 4.4, 540),
            ("Excel avanzado", 4.5, 1250),
            ("Python para análisis de datos", 4.6, 980),
            ("JavaScript moderno", 4.6, 760),
            ("SQL desde cero", 4.8, 1250),
            ("Git y GitHub", 4.9, 1530),
            ("Estadística para no estadísticos", None, 210),
            ("Power BI en la práctica", None, 120),
            ("Finanzas personales", None, 85),
        ])


class TestTask3Categories:
    def test_category_menu(self, check_ordered):
        check_ordered("03_categories.sql", columns=["category"], rows=[
            ("Datos",),
            ("Diseño",),
            ("Negocios",),
            ("Programación",),
        ])


class TestTask4TopRated:
    def test_three_best_rated(self, check_ordered):
        check_ordered("04_top_rated.sql", columns=["title", "rating", "students"], rows=[
            ("Git y GitHub", 4.9, 1530),
            ("SQL desde cero", 4.8, 1250),
            ("Python para análisis de datos", 4.6, 980),
        ])


class TestTask5SecondPage:
    def test_second_page(self, check_ordered):
        check_ordered("05_second_page.sql", columns=["title", "price"], rows=[
            ("Marketing digital", 49),
            ("SQL desde cero", 49),
            ("Diseño de logos", 59),
            ("Estadística para no estadísticos", 59),
        ])

"""Tests of lab 1.2: one class per task, each one runs a file of queries/."""


class TestSeed:
    """Guard: green from the start. It fails only if seed.sql was changed."""

    def test_menu_has_eight_items(self, db):
        assert db.execute("SELECT count(*) FROM menu_items;").fetchone() == (8,)


class TestTask1Menu:
    def test_name_category_and_price(self, check):
        check("01_menu.sql", columns=["name", "category", "price"], rows=[
            ("Café americano", "bebida", 6.0),
            ("Capuchino", "bebida", 8.5),
            ("Té de manzanilla", "bebida", 5.0),
            ("Jugo de naranja", "bebida", 9.5),
            ("Sándwich de pollo", "comida", 14.0),
            ("Empanada de carne", "comida", 7.5),
            ("Torta de chocolate", "postre", 11.0),
            ("Alfajor", "postre", 3.7),
        ])


class TestTask2Profit:
    def test_profit_per_item(self, check):
        check("02_profit.sql", columns=["name", "profit"], rows=[
            ("Café americano", 4.5),
            ("Capuchino", 6.25),
            ("Té de manzanilla", 4.25),
            ("Jugo de naranja", 6.0),
            ("Sándwich de pollo", 7.75),
            ("Empanada de carne", 4.5),
            ("Torta de chocolate", 6.5),
            ("Alfajor", 2.45),
        ])


class TestTask3PriceWithTax:
    def test_price_with_tax_rounded_to_cents(self, check):
        check("03_price_with_tax.sql", columns=["name", "price_with_tax"], rows=[
            ("Café americano", 7.08),
            ("Capuchino", 10.03),
            ("Té de manzanilla", 5.9),
            ("Jugo de naranja", 11.21),
            ("Sándwich de pollo", 16.52),
            ("Empanada de carne", 8.85),
            ("Torta de chocolate", 12.98),
            ("Alfajor", 4.37),
        ])


class TestTask4Margin:
    def test_margin_percentage_with_one_decimal(self, check):
        check("04_margin.sql", columns=["name", "margin_pct"], rows=[
            ("Café americano", 75.0),
            ("Capuchino", 73.5),
            ("Té de manzanilla", 85.0),
            ("Jugo de naranja", 63.2),
            ("Sándwich de pollo", 55.4),
            ("Empanada de carne", 60.0),
            ("Torta de chocolate", 59.1),
            ("Alfajor", 66.2),
        ])

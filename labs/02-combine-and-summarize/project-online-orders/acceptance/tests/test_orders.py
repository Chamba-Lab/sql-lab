"""Acceptance tests of project 2.P: one class per question of the shop's team.

Every question asks for an order, so every test uses check_ordered. "Today" is
2026-11-30 in every question (see BRIEF.md).
"""


class TestSeed:
    """Guard: green whatever the folder under test holds. It fails only if seed.sql was changed."""

    def test_rows_per_table(self, db):
        counts = db.execute(
            "SELECT (SELECT count(*) FROM customers), (SELECT count(*) FROM products),"
            " (SELECT count(*) FROM orders), (SELECT count(*) FROM order_items);").fetchone()
        assert counts == (8, 9, 11, 17)


class TestTask1OrderTotals:
    def test_total_of_every_sale(self, check_ordered):
        check_ordered("01_order_totals.sql", columns=["order_id", "customer", "total"], rows=[
            (101, "Lucía Torres", 78.0),
            (102, "María López", 153.75),
            (103, "Jorge Ríos", 91.0),
            (105, "Invitado", 131.0),
            (106, "María López", 125.0),
            (107, "Lucía Torres", 60.0),
            (108, "Carla Mendoza", 270.0),
            (110, "María López", 82.0),
        ])


class TestTask2NoPurchases:
    def test_registered_customers_with_no_sale(self, check_ordered):
        check_ordered("02_no_purchases.sql", columns=["id", "name", "email"], rows=[
            (5, "Rosa Huamán", "rosa.huaman@example.com"),
            (6, "Pedro Salas", "pedro.salas@example.com"),
            (7, "Andrés Vega", "andres.vega@example.com"),
        ])


class TestTask3Categories:
    def test_categories_that_sold_at_least_100_soles(self, check_ordered):
        check_ordered("03_categories.sql", columns=["category", "orders", "units", "revenue"], rows=[
            ("Mochilas", 3, 6, 481.25),
            ("Cuadernos", 3, 9, 177.5),
            ("Escritura", 3, 6, 100.0),
        ])


class TestTask4BigOrders:
    def test_sales_above_the_average_sale(self, check_ordered):
        check_ordered("04_big_orders.sql", columns=["order_id", "subtotal"], rows=[
            (108, 258.0),
            (102, 153.75),
            (105, 116.0),
        ])


class TestTask5BestSellers:
    def test_second_page_of_the_best_sellers(self, check_ordered):
        check_ordered("05_best_sellers.sql", columns=["product_id", "name", "units"], rows=[
            (5, "Mochila escolar", 2),
            (4, "Resaltadores x6", 1),
        ])


class TestTask6Customers:
    def test_what_each_customer_really_bought(self, check_ordered):
        check_ordered("06_customers.sql", columns=["customer_id", "name", "orders", "spent"], rows=[
            (8, "Carla Mendoza", 1, 270.0),
            (2, "María López", 2, 235.75),
            (1, "Lucía Torres", 2, 138.0),
            (4, "María López", 1, 125.0),
            (3, "Jorge Ríos", 1, 91.0),
            (7, "Andrés Vega", 0, 0.0),
            (6, "Pedro Salas", 0, 0.0),
            (5, "Rosa Huamán", 0, 0.0),
        ])

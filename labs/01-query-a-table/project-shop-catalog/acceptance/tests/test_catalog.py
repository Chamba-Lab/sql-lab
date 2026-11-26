"""Acceptance tests of project 1.P: one class per question of the sales team.

Every question asks for an order, so every test uses check_ordered. "Today" is
2026-11-20 in every question (see BRIEF.md).
"""


class TestSeed:
    """Guard: green whatever the folder under test holds. It fails only if seed.sql was changed."""

    def test_seventeen_products(self, db):
        assert db.execute("SELECT count(*) FROM products;").fetchone() == (17,)


class TestTask1Search:
    def test_sellable_products_that_mention_usb_or_bluetooth(self, check_ordered):
        check_ordered("01_search.sql", columns=["id", "name"], rows=[
            (4, "Adaptador USB-C a HDMI"),
            (1, "Audífonos Bluetooth AX2"),
            (3, "Hub USB 4 puertos"),
            (16, "Lámpara LED USB"),
        ])


class TestTask2Brands:
    def test_brands_on_sale_today(self, check_ordered):
        check_ordered("02_brands.sql", columns=["brand"], rows=[
            ("anker",),
            ("lenovo",),
            ("logitech",),
            ("philips",),
            ("sony",),
            ("xiaomi",),
        ])


class TestTask3Restock:
    def test_products_to_restock(self, check_ordered):
        check_ordered("03_restock.sql", columns=["id", "name", "stock", "stock_status"], rows=[
            (12, "Cargador rápido 20 W", 0, "agotado"),
            (2, "Parlante portátil bluetooth", 0, "agotado"),
            (9, "Laptop 14 Ryzen 5", 2, "bajo"),
            (3, "Hub USB 4 puertos", 3, "bajo"),
            (14, "Smartwatch Band 9", 4, "bajo"),
            (8, "Monitor 24 pulgadas", None, "sin contar"),
        ])


class TestTask4Promotions:
    def test_promotions_running_today(self, check_ordered):
        check_ordered("04_promotions.sql",
                      columns=["id", "name", "price", "promo_price", "discount_pct"], rows=[
            (1, "Audífonos Bluetooth AX2", 199.9, 149.9, 25.0),
            (11, "Soporte para celular", 24.9, 19.9, 20.1),
            (15, "Cámara web HD", 159.9, 129.9, 18.8),
            (5, "Memoria USB 64 GB", 39.9, 34.9, 12.5),
            (8, "Monitor 24 pulgadas", 649.0, 577.0, 11.1),
            (6, "Mouse inalámbrico M3", 89.9, 79.9, 11.1),
            (13, "Celular Redmi 13", 899.0, 849.0, 5.6),
        ])


class TestTask5NewArrivals:
    def test_second_page_of_new_arrivals(self, check_ordered):
        check_ordered("05_new_arrivals.sql", columns=["id", "name", "added_on"], rows=[
            (11, "Soporte para celular", "2026-11-05"),
            (4, "Adaptador USB-C a HDMI", "2026-10-21"),
        ])


class TestTask6Catalog:
    def test_what_a_customer_can_buy_today_and_at_what_price(self, check_ordered):
        check_ordered("06_catalog.sql", columns=["id", "name", "category", "final_price"], rows=[
            (4, "Adaptador USB-C a HDMI", "Accesorios", 79.9),
            (3, "Hub USB 4 puertos", "Accesorios", 79.9),
            (1, "Audífonos Bluetooth AX2", "Audio", 149.9),
            (17, "Audífonos con cable", "Audio", 159.0),
            (14, "Smartwatch Band 9", "Celulares", 179.0),
            (13, "Celular Redmi 13", "Celulares", 849.0),
            (6, "Mouse inalámbrico M3", "Cómputo", 79.9),
            (7, "Teclado mecánico K8", "Cómputo", 249.0),
            (9, "Laptop 14 Ryzen 5", "Cómputo", 2499.0),
            (16, "Lámpara LED USB", "Hogar", 34.9),
            (11, "Soporte para celular", "Otros", 19.9),
            (10, "Funda para laptop 14", "Otros", 49.9),
        ])
